import sqlite3

def inicializar_bd():
    # 1. Conexión y creación del archivo de base de datos
    # Si el archivo no existe, SQLite lo crea automáticamente en tu carpeta
    conexion = sqlite3.connect('17_expertech_inventario.db')
    cursor = conexion.cursor()

    # 2. Tabla del Catálogo (Inventario de Productos)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL,
            detalles TEXT,
            imagen_url TEXT
        )
    ''')

    # 3. Tabla del Historial de Compras (Para el panel de Administrador)
    # Aquí guardaremos el total y las reglas que la IA usó para justificar la venta
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historial_compras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            articulos_comprados TEXT NOT NULL,
            total REAL NOT NULL,
            justificacion_ia TEXT
        )
    ''')

    # 4. Inserción de los datos de prueba de tu Mockup
    # Solo insertamos si la tabla de productos está completamente vacía
    cursor.execute("SELECT COUNT(*) FROM productos")
    if cursor.fetchone()[0] == 0:
        productos_demo = [
            ("AMD Ryzen 7 5700X", "CPU", 3200.0, 10, "Procesador de 8 núcleos y 16 hilos. Ideal para virtualización y productividad pesada.", "cpu_icon"),
            ("32GB (2x16) DDR4 3200MHz", "RAM", 1600.0, 15, "Memoria de alto rendimiento para multitarea sin cuellos de botella.", "ram_icon"),
            ("NVIDIA RTX 4060 8GB", "GPU", 6500.0, 5, "Tarjeta gráfica moderna. Optimiza plataformas con socket AM4 y gaming medio.", "gpu_icon"),
            ("Fuente 600W 80+ Bronze", "PSU", 1200.0, 8, "Soporta consumo TDP estimado de 380W con margen del 30%.", "psu_icon"),
            ("Kit AM4 Micro-ATX", "Motherboard", 2100.0, 12, "Gabinete y placa base con compatibilidad física verificada para serie 5000.", "case_icon")
        ]
        
        cursor.executemany('''
            INSERT INTO productos (nombre, categoria, precio, stock, detalles, imagen_url)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', productos_demo)
        print("✅ Catálogo de prueba inyectado en la base de datos.")

    # Guardar los cambios y cerrar la conexión
    conexion.commit()
    conexion.close()
    print("✅ Base de datos '17_expertech_inventario.db' lista y estructurada.")

# Bloque de ejecución principal
if __name__ == "__main__":
    inicializar_bd()