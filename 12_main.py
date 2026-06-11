import flet as ft

def main(page: ft.Page):
    # 1. Configuración de la Ventana
    page.title = "Expertech AI - Asesor"
    page.window.width = 400
    page.window.height = 800
    page.bgcolor = ft.Colors.BLACK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # 2. Componentes
    logo_grafico = ft.Icon(
        icon=ft.Icons.COMPUTER,   # ← 'icon' es el keyword correcto en 0.85
        size=180,
        color="#1976D2"
    )

    titulo = ft.Text(
        value="Bienvenido",
        size=40,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.WHITE
    )

    subtitulo = ft.Text(
        value="EXPERTECH - AI",
        size=16,
        color=ft.Colors.GREY
    )

    boton_entrar = ft.Button(
        content=ft.Text("Entrar", size=16, weight=ft.FontWeight.BOLD),
        style=ft.ButtonStyle(
            bgcolor="#29B6F6",
            color=ft.Colors.BLACK,
            shape=ft.RoundedRectangleBorder(radius=15),
        ),
        width=200,
        height=55,
        on_click=lambda e: print("Iniciando motor de inferencia...")
    )

    # 3. Layout
    page.add(
        ft.Column(
            controls=[
                logo_grafico,
                ft.Container(height=50),
                titulo,
                subtitulo,
                ft.Container(height=80),
                boton_entrar
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True
        )
    )

if __name__ == "__main__":
    ft.run(main)