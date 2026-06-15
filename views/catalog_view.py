import flet as ft
import sqlite3
import os

DB_PATH = "17_expertech_inventario.db"

def obtener_productos(categoria=None, busqueda=None):
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()

    query = "SELECT id, nombre, categoria, subcategoria, precio, stock, detalles, imagen_url FROM productos WHERE 1=1"
    params = []

    if categoria and categoria != "Todos":
        query += " AND categoria = ?"
        params.append(categoria)

    if busqueda:
        query += " AND nombre LIKE ?"
        params.append(f"%{busqueda}%")

    query += " ORDER BY categoria, nombre"
    cursor.execute(query, params)
    filas = cursor.fetchall()
    conexion.close()

    return [
        {
            "id": f[0],
            "nombre": f[1],
            "categoria": f[2],
            "subcategoria": f[3],
            "precio": f[4],
            "stock": f[5],
            "detalles": f[6],
            "imagen_url": f[7],
        }
        for f in filas
    ]

def obtener_categorias():
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    cursor.execute("SELECT DISTINCT categoria FROM productos ORDER BY categoria")
    filas = cursor.fetchall()
    conexion.close()
    return ["Todos"] + [f[0] for f in filas]

def icono_categoria(categoria):
    iconos = {
        "Procesadores": ft.icons.MEMORY,
        "Tarjetas de Video": ft.icons.VIDEOCAM,
        "Memorias RAM": ft.icons.STORAGE,
        "Discos Duros": ft.icons.SAVE,
        "Tarjetas Madre": ft.icons.DEVELOPER_BOARD,
        "Fuentes de Poder": ft.icons.BOLT,
        "Gabinetes": ft.icons.COMPUTER,
        "Enfriamiento y Ventilación": ft.icons.AC_UNIT,
        "Laptops": ft.icons.LAPTOP,
        "Mouse": ft.icons.MOUSE,
        "Teclados": ft.icons.KEYBOARD,
        "Kits de Teclado y Mouse": ft.icons.DEVICES,
        "Monitores": ft.icons.MONITOR,
        "Audífonos": ft.icons.HEADPHONES,
        "Mousepads": ft.icons.GRID_ON,
        "Routers": ft.icons.ROUTER,
        "Sillas Gamer": ft.icons.CHAIR,
        "Escritorios Gamer": ft.icons.DESK,
        "Controles de Juego": ft.icons.SPORTS_ESPORTS,
        "Tarjetas de Expansión": ft.icons.EXTENSION,
        "PC All in One": ft.icons.DESKTOP_WINDOWS,
        "PC ya armadas": ft.icons.DESKTOP_MAC,
    }
    return iconos.get(categoria, ft.icons.DEVICES_OTHER)

def imagen_o_icono_catalogo(producto):
    if producto["imagen_url"] and os.path.exists(producto["imagen_url"]):
        return ft.Container(
            content=ft.Image(
                src=producto["imagen_url"],
                width=65,
                height=65,
                fit=ft.ImageFit.CONTAIN,
            ),
            bgcolor="#1A1A2E",
            border_radius=10,
            width=65,
            height=65,
            padding=ft.padding.all(4),
        )
    else:
        return ft.Container(
            content=ft.Icon(
                icono_categoria(producto["categoria"]),
                color="#3D5AFE",
                size=36,
            ),
            bgcolor="#1A1A2E",
            border_radius=10,
            width=65,
            height=65,
            alignment=ft.alignment.center,
        )

def catalog_view(page: ft.Page):
    page.clean()
    page.bgcolor = "black"
    page.padding = 0

    from views.chat_view import chat_view

    categorias = obtener_categorias()
    categoria_seleccionada = [categorias[0]]
    busqueda_actual = [""]

    lista_productos = ft.Column(
        controls=[],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        spacing=0,
    )

    def abrir_detalle(producto):
        from views.product_detail_view import product_detail_view
        product_detail_view(page, producto)

    def tarjeta_producto(producto):
        color_stock = "green" if producto["stock"] > 5 else "orange" if producto["stock"] > 0 else "red"
        badge_color = "#3D5AFE" if producto["subcategoria"] == "Gamer" else "#1E1E1E"

        return ft.Container(
            content=ft.Row(
                controls=[
                    imagen_o_icono_catalogo(producto),
                    ft.Container(width=10),
                    ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        producto["nombre"],
                                        color="white",
                                        size=13,
                                        weight=ft.FontWeight.BOLD,
                                        expand=True,
                                    ),
                                    ft.Container(
                                        content=ft.Text(
                                            producto["subcategoria"],
                                            color="white",
                                            size=10,
                                        ),
                                        bgcolor=badge_color,
                                        border_radius=10,
                                        padding=ft.padding.symmetric(horizontal=6, vertical=2),
                                    ),
                                ],
                            ),
                            ft.Text(
                                producto["categoria"],
                                color="grey",
                                size=11,
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        f"${producto['precio']:,.0f} MXN",
                                        color="#29B6F6",
                                        size=13,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    ft.Container(width=8),
                                    ft.Text(
                                        f"Stock: {producto['stock']}",
                                        color=color_stock,
                                        size=11,
                                    ),
                                ]
                            ),
                        ],
                        spacing=3,
                        expand=True,
                    ),
                    ft.Icon(ft.icons.ARROW_FORWARD_IOS, color="grey", size=14),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor="#1E1E1E",
            border_radius=12,
            padding=ft.padding.all(10),
            margin=ft.margin.symmetric(horizontal=12, vertical=5),
            on_click=lambda e, p=producto: abrir_detalle(p),
            on_hover=lambda e: setattr(e.control, 'bgcolor',
                "#2A2A2A" if e.data == "true" else "#1E1E1E") or page.update(),
        )

    def actualizar_lista():
        productos = obtener_productos(
            categoria=categoria_seleccionada[0],
            busqueda=busqueda_actual[0]
        )
        lista_productos.controls.clear()

        if not productos:
            lista_productos.controls.append(
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Icon(ft.icons.SEARCH_OFF, color="grey", size=60),
                            ft.Text("Sin resultados", color="grey", size=16),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=12,
                    ),
                    alignment=ft.alignment.center,
                    expand=True,
                    padding=ft.padding.all(40),
                )
            )
        else:
            for p in productos:
                lista_productos.controls.append(tarjeta_producto(p))

        page.update()

    def on_busqueda(e):
        busqueda_actual[0] = e.control.value.strip()
        actualizar_lista()

    def on_categoria(cat, boton):
        categoria_seleccionada[0] = cat
        for btn in tabs_row.controls:
            btn.bgcolor = "#3D5AFE" if btn == boton else "#1E1E1E"
            btn.border = ft.border.all(1, "#3D5AFE" if btn == boton else "#2A2A2A")
        actualizar_lista()

    tabs_row = ft.Row(
        controls=[],
        scroll=ft.ScrollMode.AUTO,
        spacing=8,
    )

    for cat in categorias:
        es_seleccionada = cat == categoria_seleccionada[0]
        btn = ft.Container(
            content=ft.Text(
                cat,
                color="white",
                size=12,
                weight=ft.FontWeight.BOLD if es_seleccionada else ft.FontWeight.NORMAL,
            ),
            bgcolor="#3D5AFE" if es_seleccionada else "#1E1E1E",
            border_radius=20,
            padding=ft.padding.symmetric(horizontal=14, vertical=8),
            border=ft.border.all(1, "#3D5AFE" if es_seleccionada else "#2A2A2A"),
        )
        btn.on_click = lambda e, c=cat, b=btn: on_categoria(c, b)
        tabs_row.controls.append(btn)

    barra_busqueda = ft.TextField(
        hint_text="Buscar producto...",
        hint_style=ft.TextStyle(color="grey"),
        bgcolor="#1E1E1E",
        border_radius=12,
        border_color="#3D5AFE",
        color="white",
        prefix_icon=ft.icons.SEARCH,
        on_change=on_busqueda,
        height=45,
        text_size=13,
        content_padding=ft.padding.symmetric(horizontal=12, vertical=8),
    )

    header = ft.Container(
        content=ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    icon_color="white",
                    on_click=lambda e: chat_view(page),
                ),
                ft.Text(
                    "Catálogo",
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

    actualizar_lista()

    page.add(
        ft.Column(
            controls=[
                header,
                ft.Container(
                    content=barra_busqueda,
                    margin=ft.margin.symmetric(horizontal=12, vertical=8),
                ),
                ft.Container(
                    content=tabs_row,
                    margin=ft.margin.only(left=12, right=12, bottom=8),
                ),
                lista_productos,
            ],
            expand=True,
            spacing=0,
        )
    )