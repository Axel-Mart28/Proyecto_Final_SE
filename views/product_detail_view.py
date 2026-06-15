import flet as ft
import os
from views.catalog_view import icono_categoria

def product_detail_view(page: ft.Page, producto: dict):
    page.clean()
    page.bgcolor = "black"
    page.padding = 0

    from views.catalog_view import catalog_view
    from views.cart_manager import agregar_al_carrito

    def añadir_carrito(e):
        agregar_al_carrito(producto)
        page.snack_bar = ft.SnackBar(
            content=ft.Text(
                f"✅ {producto['nombre']} añadido al carrito",
                color="white"
            ),
            bgcolor="#1A1A2E",
            duration=2000,
        )
        page.snack_bar.open = True
        page.update()

    header = ft.Container(
        content=ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    icon_color="white",
                    on_click=lambda e: catalog_view(page),
                ),
                ft.Text(
                    "Detalle del Producto",
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

    # Imagen o ícono
    if producto.get("imagen_url") and os.path.exists(producto["imagen_url"]):
        imagen_producto = ft.Container(
            content=ft.Image(
                src=producto["imagen_url"],
                width=180,
                height=180,
                fit=ft.ImageFit.CONTAIN,
            ),
            bgcolor="#1A1A2E",
            border_radius=20,
            width=180,
            height=180,
            padding=ft.padding.all(8),
            margin=ft.margin.symmetric(vertical=20),
        )
    else:
        imagen_producto = ft.Container(
            content=ft.Icon(
                icono_categoria(producto.get("categoria", "")),
                color="#3D5AFE",
                size=100,
            ),
            bgcolor="#1A1A2E",
            border_radius=20,
            width=180,
            height=180,
            alignment=ft.alignment.center,
            margin=ft.margin.symmetric(vertical=20),
        )

    # Badge categoría
    badge_categoria = ft.Container(
        content=ft.Text(
            f"{producto.get('categoria', '')} · {producto.get('subcategoria', 'Normal')}",
            color="#3D5AFE",
            size=12,
            weight=ft.FontWeight.BOLD,
        ),
        bgcolor="#1A1A2E",
        border_radius=20,
        padding=ft.padding.symmetric(horizontal=12, vertical=4),
    )

    # Stock
    stock = producto.get("stock", 0)
    if stock > 5:
        stock_color = "green"
        stock_texto = f"✅ En stock ({stock} disponibles)"
    elif stock > 0:
        stock_color = "orange"
        stock_texto = f"⚠️ Últimas unidades ({stock} disponibles)"
    else:
        stock_color = "red"
        stock_texto = "❌ Sin stock"

    boton_carrito = ft.ElevatedButton(
        text="Añadir al carrito",
        bgcolor="#3D5AFE",
        color="white",
        width=250,
        height=50,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=15),
        ),
        icon=ft.icons.SHOPPING_CART,
        disabled=stock == 0,
        on_click=añadir_carrito,
    )

    page.add(
        ft.Column(
            controls=[
                header,
                ft.Column(
                    controls=[
                        ft.Row(
                            controls=[imagen_producto],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Row(
                            controls=[badge_categoria],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Container(height=8),
                        ft.Text(
                            producto.get("nombre", ""),
                            color="white",
                            size=22,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Container(height=4),
                        ft.Text(
                            f"${producto.get('precio', 0):,.0f} MXN",
                            color="#29B6F6",
                            size=26,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Container(height=4),
                        ft.Text(
                            stock_texto,
                            color=stock_color,
                            size=13,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Divider(color="#2A2A2A", height=24),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text(
                                        "Especificaciones",
                                        color="grey",
                                        size=13,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    ft.Container(height=6),
                                    ft.Text(
                                        producto.get("detalles") or "Sin descripción disponible.",
                                        color="white",
                                        size=14,
                                    ),
                                ],
                            ),
                            bgcolor="#1E1E1E",
                            border_radius=12,
                            padding=ft.padding.all(16),
                            margin=ft.margin.symmetric(horizontal=16),
                        ),
                        ft.Container(height=24),
                        ft.Row(
                            controls=[boton_carrito],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Container(height=24),
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8,
                ),
            ],
            expand=True,
            spacing=0,
        )
    )