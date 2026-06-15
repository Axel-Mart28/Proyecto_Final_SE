import flet as ft

def justification_view(page: ft.Page, articulos: str, total: float, justificacion: str):
    page.clean()
    page.bgcolor = "black"
    page.padding = 0

    from views.chat_view import chat_view

    header = ft.Container(
        content=ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    icon_color="white",
                    on_click=lambda e: chat_view(page),
                ),
                ft.Text(
                    "Justificación del Sistema",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color="white",
                    expand=True,
                ),
            ],
        ),
        bgcolor="#1E1E1E",
        padding=ft.padding.symmetric(horizontal=8, vertical=4),
    )

    page.add(
        ft.Column(
            controls=[
                header,
                ft.Column(
                    controls=[
                        ft.Container(height=16),
                        # Resumen de compra
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text(
                                        "Resumen de compras:",
                                        color="white",
                                        size=16,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    ft.Container(height=8),
                                    *[
                                        ft.Text(
                                            f"- {a.strip()}",
                                            color="white",
                                            size=14,
                                        )
                                        for a in articulos.split(",")
                                    ],
                                    ft.Container(height=12),
                                    ft.Text(
                                        f"Total: ${total:,.0f} MXN",
                                        color="#29B6F6",
                                        size=18,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                ],
                                spacing=4,
                            ),
                            bgcolor="#1E1E1E",
                            border_radius=12,
                            padding=ft.padding.all(16),
                            margin=ft.margin.symmetric(horizontal=16),
                        ),
                        ft.Container(height=16),
                        # Justificación del sistema experto
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text(
                                        "Justificación del Sistema Experto:",
                                        color="white",
                                        size=16,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    ft.Container(height=8),
                                    *[
                                        ft.Text(
                                            linea,
                                            color="white" if not linea.startswith("[END]") else "#29B6F6",
                                            size=13,
                                        )
                                        for linea in justificacion.split("\n")
                                    ],
                                ],
                                spacing=8,
                            ),
                            bgcolor="#1E1E1E",
                            border_radius=12,
                            padding=ft.padding.all(16),
                            margin=ft.margin.symmetric(horizontal=16),
                        ),
                        ft.Container(height=24),
                        # Botón volver al chat
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    text="Volver al inicio",
                                    bgcolor="#3D5AFE",
                                    color="white",
                                    width=200,
                                    height=50,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=15),
                                    ),
                                    on_click=lambda e: chat_view(page),
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                    spacing=0,
                ),
            ],
            expand=True,
            spacing=0,
        )
    )