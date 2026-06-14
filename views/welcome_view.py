import flet as ft

def welcome_view(page: ft.Page):
    page.clean()
    page.bgcolor = "black"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    from views.chat_view import chat_view

    logo_grafico = ft.Icon(
        name=ft.icons.COMPUTER,
        size=180,
        color="#1976D2"
    )

    titulo = ft.Text(
        value="Bienvenido",
        size=40,
        weight=ft.FontWeight.BOLD,
        color="white"
    )

    subtitulo = ft.Text(
        value="EXPERTECH - AI",
        size=16,
        color="grey"
    )

    boton_entrar = ft.ElevatedButton(
        text="Entrar",
        bgcolor="#29B6F6",
        color="black",
        width=200,
        height=55,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=15),
        ),
        on_click=lambda e: chat_view(page)
    )

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