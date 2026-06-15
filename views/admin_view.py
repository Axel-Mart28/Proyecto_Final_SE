import flet as ft
import sqlite3
import shutil
import os

DB_PATH = "17_expertech_inventario.db"
ADMIN_PASSWORD = "Expertech_2026"
ASSETS_PATH = "assets"

# ============================================================
# PANEL DE ADMINISTRADOR
# ============================================================
def admin_panel(page: ft.Page):
    page.clean()
    page.bgcolor = "black"
    page.padding = 0

    from views.chat_view import chat_view

    # Crear carpeta assets si no existe
    if not os.path.exists(ASSETS_PATH):
        os.makedirs(ASSETS_PATH)

    def obtener_historial():
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        cursor.execute("SELECT id, fecha, articulos_comprados, total FROM historial_compras ORDER BY fecha DESC")
        filas = cursor.fetchall()
        conexion.close()
        return filas

    def obtener_productos():
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre, categoria, precio, stock FROM productos")
        filas = cursor.fetchall()
        conexion.close()
        return filas

    def eliminar_producto(producto_id):
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM productos WHERE id = ?", (producto_id,))
        conexion.commit()
        conexion.close()
        admin_panel(page)

    # Ruta de imagen seleccionada
    imagen_seleccionada = [""]

    texto_imagen = ft.Text(
        "Sin imagen seleccionada",
        color="grey",
        size=12,
        italic=True,
    )

    def on_imagen_seleccionada(e: ft.FilePickerResultEvent):
        if e.files:
            archivo = e.files[0]
            nombre_archivo = os.path.basename(archivo.path)
            destino = os.path.join(ASSETS_PATH, nombre_archivo)

            # Copiar imagen a assets/
            shutil.copy(archivo.path, destino)
            imagen_seleccionada[0] = destino

            texto_imagen.value = f"✅ {nombre_archivo}"
            texto_imagen.color = "green"
            page.update()

    file_picker = ft.FilePicker(on_result=on_imagen_seleccionada)
    page.overlay.append(file_picker)

    def agregar_producto(e):
        if not campo_nombre.value or not campo_categoria.value or not campo_precio.value or not campo_stock.value:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Por favor llena todos los campos obligatorios", color="white"),
                bgcolor="red",
                duration=2000,
            )
            page.snack_bar.open = True
            page.update()
            return

        try:
            precio = float(campo_precio.value)
            stock = int(campo_stock.value)
        except ValueError:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Precio y stock deben ser números", color="white"),
                bgcolor="red",
                duration=2000,
            )
            page.snack_bar.open = True
            page.update()
            return

        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        cursor.execute('''
            INSERT INTO productos (nombre, categoria, subcategoria, precio, stock, detalles, imagen_url)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            campo_nombre.value,
            campo_categoria.value,
            campo_subcategoria.value or "Normal",
            precio,
            stock,
            campo_detalles.value or "",
            imagen_seleccionada[0],
        ))
        conexion.commit()
        conexion.close()

        page.snack_bar = ft.SnackBar(
            content=ft.Text("✅ Producto agregado exitosamente", color="white"),
            bgcolor="#1A1A2E",
            duration=2000,
        )
        page.snack_bar.open = True
        page.update()
        admin_panel(page)

    # Campos
    campo_nombre = ft.TextField(
        hint_text="Nombre del producto",
        bgcolor="#1E1E1E",
        border_radius=10,
        border_color="#3D5AFE",
        color="white",
        hint_style=ft.TextStyle(color="grey"),
    )
    campo_categoria = ft.TextField(
        hint_text="Categoría (CPU, GPU, RAM...)",
        bgcolor="#1E1E1E",
        border_radius=10,
        border_color="#3D5AFE",
        color="white",
        hint_style=ft.TextStyle(color="grey"),
    )
    campo_subcategoria = ft.TextField(
        hint_text="Subcategoría (Gamer / Normal)",
        bgcolor="#1E1E1E",
        border_radius=10,
        border_color="#3D5AFE",
        color="white",
        hint_style=ft.TextStyle(color="grey"),
    )
    campo_precio = ft.TextField(
        hint_text="Precio (MXN)",
        bgcolor="#1E1E1E",
        border_radius=10,
        border_color="#3D5AFE",
        color="white",
        hint_style=ft.TextStyle(color="grey"),
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    campo_stock = ft.TextField(
        hint_text="Stock",
        bgcolor="#1E1E1E",
        border_radius=10,
        border_color="#3D5AFE",
        color="white",
        hint_style=ft.TextStyle(color="grey"),
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    campo_detalles = ft.TextField(
        hint_text="Detalles/especificaciones (opcional)",
        bgcolor="#1E1E1E",
        border_radius=10,
        border_color="#3D5AFE",
        color="white",
        hint_style=ft.TextStyle(color="grey"),
        multiline=True,
        min_lines=2,
        max_lines=4,
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
                    "Panel Administrador",
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

    # Historial
    historial = obtener_historial()
    filas_historial = []
    for h in historial:
        filas_historial.append(
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(f"🗓 {h[1]}", color="grey", size=11),
                        ft.Text(h[2], color="white", size=13),
                        ft.Text(
                            f"Total: ${h[3]:,.0f} MXN",
                            color="#29B6F6",
                            size=14,
                            weight=ft.FontWeight.BOLD,
                        ),
                    ],
                    spacing=4,
                ),
                bgcolor="#1E1E1E",
                border_radius=10,
                padding=ft.padding.all(12),
                margin=ft.margin.only(bottom=8),
            )
        )

    if not filas_historial:
        filas_historial.append(
            ft.Text("Sin compras registradas aún.", color="grey", size=13)
        )

    # Productos
    productos = obtener_productos()
    filas_productos = []
    for p in productos:
        filas_productos.append(
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text(p[1], color="white", size=13, weight=ft.FontWeight.BOLD),
                                ft.Text(
                                    f"{p[2]} | ${p[3]:,.0f} MXN | Stock: {p[4]}",
                                    color="grey",
                                    size=12,
                                ),
                            ],
                            spacing=2,
                            expand=True,
                        ),
                        ft.IconButton(
                            icon=ft.icons.DELETE_OUTLINE,
                            icon_color="red",
                            icon_size=20,
                            on_click=lambda e, pid=p[0]: eliminar_producto(pid),
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                bgcolor="#1E1E1E",
                border_radius=10,
                padding=ft.padding.all(12),
                margin=ft.margin.only(bottom=8),
            )
        )

    page.add(
        ft.Column(
            controls=[
                header,
                ft.Column(
                    controls=[
                        ft.Container(height=12),

                        # Historial
                        ft.Text("📋 Historial de Compras", color="white", size=16, weight=ft.FontWeight.BOLD),
                        ft.Container(height=4),
                        *filas_historial,

                        ft.Divider(color="#2A2A2A", height=24),

                        # Productos
                        ft.Text("📦 Productos en Catálogo", color="white", size=16, weight=ft.FontWeight.BOLD),
                        ft.Container(height=4),
                        *filas_productos,

                        ft.Divider(color="#2A2A2A", height=24),

                        # Agregar producto
                        ft.Text("➕ Agregar Producto", color="white", size=16, weight=ft.FontWeight.BOLD),
                        ft.Container(height=4),
                        campo_nombre,
                        campo_categoria,
                        campo_subcategoria,
                        campo_precio,
                        campo_stock,
                        campo_detalles,

                        # Selector de imagen
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    text="Seleccionar imagen",
                                    icon=ft.icons.IMAGE,
                                    bgcolor="#1A1A2E",
                                    color="white",
                                    on_click=lambda e: file_picker.pick_files(
                                        allowed_extensions=["png", "jpg", "jpeg", "webp"],
                                        dialog_title="Selecciona la imagen del producto",
                                    ),
                                ),
                                texto_imagen,
                            ],
                            spacing=12,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),

                        ft.Container(height=8),
                        ft.ElevatedButton(
                            text="Agregar producto",
                            bgcolor="#3D5AFE",
                            color="white",
                            width=400,
                            height=48,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=12),
                            ),
                            on_click=agregar_producto,
                        ),
                        ft.Container(height=24),
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                    spacing=8,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                ),
            ],
            expand=True,
            spacing=0,
        )
    )


# ============================================================
# LOGIN
# ============================================================
def admin_view(page: ft.Page):
    page.clean()
    page.bgcolor = "black"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    from views.chat_view import chat_view

    error_texto = ft.Text("", color="red", size=13)

    def verificar_password(e):
        if campo_password.value == ADMIN_PASSWORD:
            admin_panel(page)
        else:
            error_texto.value = "❌ Contraseña incorrecta"
            campo_password.value = ""
            page.update()

    campo_password = ft.TextField(
        hint_text="Contraseña",
        password=True,
        can_reveal_password=True,
        bgcolor="#1E1E1E",
        border_radius=12,
        border_color="#3D5AFE",
        color="white",
        hint_style=ft.TextStyle(color="grey"),
        width=280,
        on_submit=verificar_password,
    )

    page.add(
        ft.Column(
            controls=[
                ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    icon_color="white",
                    on_click=lambda e: chat_view(page),
                ),
                ft.Icon(
                    ft.icons.ADMIN_PANEL_SETTINGS,
                    size=100,
                    color="#3D5AFE",
                ),
                ft.Container(height=20),
                ft.Text(
                    "Acceso Administrador",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color="white",
                ),
                ft.Text(
                    "Ingresa la contraseña para continuar",
                    size=13,
                    color="grey",
                ),
                ft.Container(height=20),
                campo_password,
                ft.Container(height=8),
                error_texto,
                ft.Container(height=8),
                ft.ElevatedButton(
                    text="Entrar",
                    bgcolor="#3D5AFE",
                    color="white",
                    width=280,
                    height=50,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=15),
                    ),
                    on_click=verificar_password,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
            spacing=8,
        )
    )