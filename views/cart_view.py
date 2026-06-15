import flet as ft
from views.cart_manager import obtener_carrito, eliminar_del_carrito, limpiar_carrito, obtener_total
import sqlite3
from datetime import datetime

DB_PATH = "17_expertech_inventario.db"

def registrar_compra(articulos, total, justificacion):
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    cursor.execute('''
        INSERT INTO historial_compras (articulos_comprados, total, justificacion_ia)
        VALUES (?, ?, ?)
    ''', (articulos, total, justificacion))
    conexion.commit()
    conexion.close()

def cart_view(page: ft.Page):
    page.clean()
    page.bgcolor = "black"
    page.padding = 0

    from views.chat_view import chat_view
    from views.justification_view import justification_view

    carrito = obtener_carrito()

    def eliminar_producto(producto_id):
        eliminar_del_carrito(producto_id)
        cart_view(page)

    def abrir_confirmacion(e):
        carrito_actual = obtener_carrito()
        if not carrito_actual:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("El carrito está vacío", color="white"),
                bgcolor="#1A1A2E",
                duration=2000,
            )
            page.snack_bar.open = True
            page.update()
            return

        # Contenido del modal
        resumen_items = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(
                            f"{item['nombre']} x{item['cantidad']}",
                            color="white",
                            size=13,
                            expand=True,
                        ),
                        ft.Text(
                            f"${item['precio'] * item['cantidad']:,.0f}",
                            color="#29B6F6",
                            size=13,
                        ),
                    ]
                )
                for item in carrito_actual
            ],
            spacing=8,
        )

        total = obtener_total()

        def confirmar_compra(e):
            # Cerrar modal
            page.dialog.open = False
            page.update()

            # Preparar datos para SQLite
            articulos_str = ", ".join(
                [f"{item['nombre']} x{item['cantidad']}" for item in carrito_actual]
            )
            justificacion_placeholder = (
                "[INIT] Sistema experto iniciado.\n"
                "[RULE 01] Productos seleccionados según perfil del usuario.\n"
                "[RULE 02] Presupuesto verificado y dentro del límite.\n"
                "[RULE 03] Compatibilidad entre componentes verificada.\n"
                "[END] Compra aprobada por el motor de inferencia."
            )

            # Registrar en SQLite
            registrar_compra(articulos_str, total, justificacion_placeholder)

            # Limpiar carrito
            limpiar_carrito()

            # Navegar a justificación
            justification_view(page, articulos_str, total, justificacion_placeholder)

        def cancelar(e):
            page.dialog.open = False
            page.update()

        page.dialog = ft.AlertDialog(
            modal=True,
            bgcolor="#1E1E1E",
            title=ft.Text(
                "Confirmar compra",
                color="white",
                weight=ft.FontWeight.BOLD,
            ),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        resumen_items,
                        ft.Divider(color="#2A2A2A"),
                        ft.Row(
                            controls=[
                                ft.Text("Total:", color="grey", size=14),
                                ft.Text(
                                    f"${total:,.0f} MXN",
                                    color="#29B6F6",
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                    ],
                    spacing=8,
                ),
                width=280,
            ),
            actions=[
                ft.TextButton(
                    "Cancelar",
                    style=ft.ButtonStyle(color="grey"),
                    on_click=cancelar,
                ),
                ft.ElevatedButton(
                    "Confirmar compra",
                    bgcolor="#3D5AFE",
                    color="white",
                    on_click=confirmar_compra,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.dialog.open = True
        page.update()

    header = ft.Container(
        content=ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    icon_color="white",
                    on_click=lambda e: chat_view(page),
                ),
                ft.Text(
                    "Carrito",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color="white",
                    expand=True,
                ),
            ],
        ),
        bgcolor="#1E1E1E",
        padding=ft.padding.symmetric(horizontal=8, vertical=4),
    )

    # Carrito vacío
    if not carrito:
        page.add(
            ft.Column(
                controls=[
                    header,
                    ft.Column(
                        controls=[
                            ft.Icon(ft.icons.SHOPPING_CART, color="grey", size=80),
                            ft.Text(
                                "Tu carrito está vacío",
                                color="grey",
                                size=18,
                            ),
                            ft.ElevatedButton(
                                text="Ver catálogo",
                                bgcolor="#3D5AFE",
                                color="white",
                                on_click=lambda e: __import__(
                                    'views.catalog_view', fromlist=['catalog_view']
                                ).catalog_view(page),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        expand=True,
                        spacing=16,
                    ),
                ],
                expand=True,
                spacing=0,
            )
        )
        return

    # Lista de productos en el carrito
    def fila_producto(item):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text(
                                item["nombre"],
                                color="white",
                                size=14,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                f"${item['precio']:,.0f} MXN c/u",
                                color="grey",
                                size=12,
                            ),
                            ft.Text(
                                f"Subtotal: ${item['precio'] * item['cantidad']:,.0f} MXN",
                                color="#29B6F6",
                                size=13,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                        spacing=4,
                        expand=True,
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(
                                f"x{item['cantidad']}",
                                color="white",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.IconButton(
                                icon=ft.icons.DELETE_OUTLINE,
                                icon_color="red",
                                icon_size=20,
                                on_click=lambda e, pid=item["id"]: eliminar_producto(pid),
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=4,
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor="#1E1E1E",
            border_radius=12,
            padding=ft.padding.all(12),
            margin=ft.margin.symmetric(horizontal=12, vertical=6),
        )

    lista = ft.Column(
        controls=[fila_producto(item) for item in carrito],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        spacing=0,
    )

    # Footer con total y botón pagar
    footer = ft.Container(
    content=ft.Column(
        controls=[
            ft.Divider(color="#2A2A2A"),
            ft.Row(
                controls=[
                    ft.Text("Total:", color="grey", size=16),
                    ft.Text(
                        f"${obtener_total():,.0f} MXN",
                        color="#29B6F6",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            ft.Container(height=8),
            ft.ElevatedButton(
                text="Pagar",
                bgcolor="#3D5AFE",
                color="white",
                width=400,
                height=50,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=15),
                ),
                on_click=abrir_confirmacion,
            ),
        ],
        spacing=8,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # ← centrar el botón
    ),
    bgcolor="black",
    padding=ft.padding.all(16),
    height=150,   # ← altura fija para el footer
)

    page.add(
    ft.Column(
        controls=[
            header,
            ft.Container(
                content=lista,
                expand=True,    # ← la lista ocupa el espacio disponible
            ),
            footer,             # ← el footer queda fijo abajo
        ],
        expand=True,
        spacing=0,
    )
)