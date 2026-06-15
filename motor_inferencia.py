import os
import sqlite3
import time
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM

# 1. Cargar la clave de seguridad desde .env
load_dotenv()
google_api_key = os.getenv("GEMINI_API_KEY")
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

# 2. Adaptador OpenAI de Google
llm_gemini = LLM(
    model="openrouter/meta-llama/llama-3.3-70b-instruct:free",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    max_tokens=4096,    # ← limitar tokens para evitar el error 400
)

# 3. Función para extraer el catálogo de SQLite
def obtener_contexto_catalogo():
    conexion = sqlite3.connect('17_expertech_inventario.db')
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre, categoria, subcategoria, precio, stock, detalles FROM productos WHERE stock > 0")
    productos = cursor.fetchall()
    conexion.close()
    
    catalogo_str = "CATÁLOGO DISPONIBLE EN TIENDA EXPERTECH:\n"
    for p in productos:
        catalogo_str += (
            f"- {p[0]} ({p[1]} - {p[2]}): "
            f"${p[3]:,.0f} MXN | Stock: {p[4]} | {p[5]}\n"
        )
    return catalogo_str

# 4. Definición de los 3 Agentes
def crear_agentes():
    # ─────────────────────────────────────────
    # AGENTE 1: Analista de Necesidades
    # ─────────────────────────────────────────
    analista = Agent(
        role="Analista de Necesidades del Cliente",
        goal=(
            "Analizar la consulta del cliente e identificar claramente: "
            "1) Uso principal del equipo (gaming, trabajo, estudio, etc.), "
            "2) Presupuesto máximo en MXN, "
            "3) Requisitos o preferencias específicas."
        ),
        backstory=(
            "Eres un especialista en entender las necesidades tecnológicas "
            "de los clientes. Tienes años de experiencia interpretando lo que "
            "los clientes realmente necesitan aunque no lo expresen técnicamente. "
            "Siempre respondes en español y de forma clara."
        ),
        verbose=True,
        allow_delegation=False,
        max_iter=3,
        llm=llm_gemini
    )

    # ─────────────────────────────────────────
    # AGENTE 2: Consultor de Inventario
    # ─────────────────────────────────────────
    consultor = Agent(
        role="Consultor de Inventario y Compatibilidad",
        goal=(
            "Seleccionar del catálogo de Expertech los productos más adecuados "
            "según las necesidades identificadas, verificando compatibilidad "
            "entre componentes y que el total no supere el presupuesto."
        ),
        backstory=(
            "Eres un experto en hardware de cómputo con profundo conocimiento "
            "de compatibilidad entre componentes. Sabes qué procesadores van con "
            "qué tarjetas madre, cuánta potencia necesita una fuente de poder, "
            "y cómo optimizar un build según el presupuesto disponible. "
            "Solo recomiendas productos que existen en el catálogo."
        ),
        verbose=True,
        allow_delegation=False,
        max_iter=3,
        llm=llm_gemini
    )

    # ─────────────────────────────────────────
    # AGENTE 3: Asesor de Recomendación Final
    # ─────────────────────────────────────────
    asesor = Agent(
        role="Asesor de Recomendación Final",
        goal=(
            "Generar una respuesta final clara, amigable y bien justificada "
            "para el cliente, incluyendo los productos recomendados, precios, "
            "total y las reglas del sistema experto aplicadas."
        ),
        backstory=(
            "Eres el asesor senior de Expertech. Tu trabajo es presentar "
            "la recomendación final al cliente de forma profesional y amigable. "
            "Siempre explicas el razonamiento detrás de cada decisión usando "
            "reglas de negocio claras en formato [RULE XX]. "
            "Respondes en español y usas formato markdown."
        ),
        verbose=True,
        allow_delegation=False,
        max_iter=3,
        llm=llm_gemini
    )

    return analista, consultor, asesor

# 5. Función principal que Flet llamará
def procesar_consulta(mensaje_usuario: str) -> str:
    catalogo_actual = obtener_contexto_catalogo()
    analista, consultor, asesor = crear_agentes()

    tarea_analisis = Task(
        description=(
            f"El cliente ha enviado el siguiente mensaje:\n"
            f"\"{mensaje_usuario}\"\n\n"
            f"Analiza su mensaje y extrae:\n"
            f"1) Uso principal del equipo\n"
            f"2) Presupuesto máximo en MXN (si lo menciona)\n"
            f"3) Requisitos específicos o preferencias\n"
            f"4) Tipo de usuario (gamer, profesional, estudiante, etc.)"
        ),
        expected_output=(
            "Un resumen estructurado con uso principal, presupuesto, "
            "requisitos específicos y tipo de usuario."
        ),
        agent=analista,
    )

    tarea_inventario = Task(
        description=(
            f"Basándote en el análisis de necesidades del cliente, "
            f"selecciona los productos más adecuados del siguiente catálogo:\n\n"
            f"{catalogo_actual}\n\n"
            f"Reglas que DEBES aplicar:\n"
            f"[RULE 01] Si el uso incluye gaming, prioriza GPU dedicada y monitor de alta tasa de refresco.\n"
            f"[RULE 02] Si el uso incluye virtualización o programación, RAM mínima 16GB y CPU con 8+ hilos.\n"
            f"[RULE 03] Verifica compatibilidad de socket entre CPU y tarjeta madre.\n"
            f"[RULE 04] La fuente de poder debe tener al menos 30% más de potencia que el TDP estimado.\n"
            f"[RULE 05] El total de productos seleccionados NO debe superar el presupuesto del cliente.\n"
            f"[RULE 06] Solo recomienda productos que estén en el catálogo con stock > 0.\n\n"
            f"Lista los productos seleccionados con nombre, precio y por qué los elegiste."
        ),
        expected_output=(
            "Lista de productos seleccionados del catálogo con nombre, "
            "precio, y justificación de cada elección. Total de la compra."
        ),
        agent=consultor,
        context=[tarea_analisis],
    )

    tarea_recomendacion = Task(
        description=(
            "Genera la respuesta final para el cliente basándote en los "
            "productos seleccionados. La respuesta debe incluir:\n\n"
            "1) Saludo amigable y resumen de lo que entendiste\n"
            "2) Lista de productos recomendados con precio de cada uno\n"
            "3) Total de la compra\n"
            "4) Justificación técnica usando este formato exacto:\n"
            "   [RULE 01] descripción → resultado aplicado\n"
            "   [RULE 02] descripción → resultado aplicado\n"
            "   (etc.)\n"
            "5) Cierre amigable invitando al cliente a agregar al carrito\n\n"
            "Responde en español, de forma clara y amigable."
        ),
        expected_output=(
            "Respuesta final completa con saludo, productos recomendados, "
            "precios, total, reglas aplicadas y cierre amigable."
        ),
        agent=asesor,
        context=[tarea_analisis, tarea_inventario],
    )

    crew = Crew(
        agents=[analista, consultor, asesor],
        tasks=[tarea_analisis, tarea_inventario, tarea_recomendacion],
        process=Process.sequential,
        verbose=True,
    )

    for intento in range(3):
        try:
            resultado = crew.kickoff()
            return str(resultado)
        except Exception as e:
            if "429" in str(e) and intento < 2:
                print(f"⏳ Rate limit. Esperando 60 segundos... (intento {intento + 1}/3)")
                time.sleep(60)
            else:
                raise e
    # ─────────────────────────────────────────
    # TAREA 2: Selección de productos
    # ─────────────────────────────────────────
    tarea_inventario = Task(
        description=(
            f"Basándote en el análisis de necesidades del cliente, "
            f"selecciona los productos más adecuados del siguiente catálogo:\n\n"
            f"{catalogo_actual}\n\n"
            f"Reglas que DEBES aplicar:\n"
            f"[RULE 01] Si el uso incluye gaming, prioriza GPU dedicada y monitor de alta tasa de refresco.\n"
            f"[RULE 02] Si el uso incluye virtualización o programación, RAM mínima 16GB y CPU con 8+ hilos.\n"
            f"[RULE 03] Verifica compatibilidad de socket entre CPU y tarjeta madre.\n"
            f"[RULE 04] La fuente de poder debe tener al menos 30% más de potencia que el TDP estimado.\n"
            f"[RULE 05] El total de productos seleccionados NO debe superar el presupuesto del cliente.\n"
            f"[RULE 06] Solo recomienda productos que estén en el catálogo con stock > 0.\n\n"
            f"Lista los productos seleccionados con nombre, precio y por qué los elegiste."
        ),
        expected_output=(
            "Lista de productos seleccionados del catálogo con nombre, "
            "precio, y justificación de cada elección. Total de la compra."
        ),
        agent=consultor,
        context=[tarea_analisis],
    )

    # ─────────────────────────────────────────
    # TAREA 3: Recomendación final
    # ─────────────────────────────────────────
    tarea_recomendacion = Task(
        description=(
            "Genera la respuesta final para el cliente basándote en los "
            "productos seleccionados. La respuesta debe incluir:\n\n"
            "1) Saludo amigable y resumen de lo que entendiste\n"
            "2) Lista de productos recomendados con precio de cada uno\n"
            "3) Total de la compra\n"
            "4) Justificación técnica usando este formato exacto:\n"
            "   [RULE 01] descripción → resultado aplicado\n"
            "   [RULE 02] descripción → resultado aplicado\n"
            "   (etc.)\n"
            "5) Cierre amigable invitando al cliente a agregar al carrito\n\n"
            "Responde en español, de forma clara y amigable."
        ),
        expected_output=(
            "Respuesta final completa con saludo, productos recomendados, "
            "precios, total, reglas aplicadas y cierre amigable."
        ),
        agent=asesor,
        context=[tarea_analisis, tarea_inventario],
    )

    # ─────────────────────────────────────────
    # CREW
    # ─────────────────────────────────────────
    crew = Crew(
        agents=[analista, consultor, asesor],
        tasks=[tarea_analisis, tarea_inventario, tarea_recomendacion],
        process=Process.sequential,
        verbose=True,
    )

    resultado = crew.kickoff()
    return str(resultado)


# Bloque de prueba
if __name__ == "__main__":
    print("Iniciando prueba del motor de inferencia...")
    prueba = procesar_consulta("Tengo 15000 pesos, ¿qué PC gamer me puedo armar?")
    print("\n--- RESPUESTA DE EXPERTECH AI ---")
    print(prueba)