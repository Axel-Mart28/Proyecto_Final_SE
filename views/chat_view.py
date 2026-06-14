import flet as ft

def chat_view(page: ft.Page):
    page.clean()
    page.bgcolor = "black"
    page.padding = 0
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    page.vertical_alignment = ft.MainAxisAlignment.START

    menu_abierto = [False]  # lista para poder modificarlo dentro de funciones

    mensajes = ft.Column(
        controls=[],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        spacing=12,
    )

    def burbuja_usuario(texto):
        return ft.Row(
            controls=[
                ft.Container(
                    content=ft.Text(texto, color="white", size=15),
                    bgcolor="#3D5AFE",
                    border_radius=ft.border_radius.all(16),
                    padding=ft.padding.all(14),
                    width=220,
                ),
            ],
            alignment=ft.MainAxisAlignment.END,
        )

    def burbuja_agente(texto):
        return ft.Row(
            controls=[
                ft.Container(
                    content=ft.Text(texto, color="white", size=15),
                    padding=ft.padding.symmetric(horizontal=8, vertical=4),
                    width=220,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
        )

    def enviar_mensaje(e):
        texto = campo_texto.value.strip()
        if not texto:
            return
        mensajes.controls.append(burbuja_usuario(texto))
        campo_texto.value = ""
        page.update()
        respuesta = "Analizando tu solicitud con el motor de inferencia..."
        mensajes.controls.append(burbuja_agente(respuesta))
        page.update()
        mensajes.scroll_to(offset=-1, duration=300)

    def limpiar_chat(e):
        mensajes.controls.clear()
        page.update()

    def toggle_menu(e):
        if menu_abierto[0]:
            panel_menu.width = 0
            menu_abierto[0] = False
        else:
            panel_menu.width = 200
            menu_abierto[0] = True
        page.update()

    def ir_catalogo(e):
        from views.catalog_view import catalog_view
        catalog_view(page)

    def ir_carrito(e):
        from views.cart_view import cart_view
        cart_view(page)

    def ir_admin(e):
        from views.admin_view import admin_view
        admin_view(page)

    # Opciones del menú
    def opcion_menu(icono, texto, accion):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(icono, color="white", size=20),
                    ft.Text(texto, color="white", size=14),
                ],
                spacing=12,
            ),
            padding=ft.padding.symmetric(horizontal=16, vertical=14),
            on_click=accion,
            on_hover=lambda e: setattr(e.control, 'bgcolor',
                "#2A2A4A" if e.data == "true" else "transparent") or page.update(),
            border_radius=8,
        )

    panel_menu = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(height=20),
                ft.Text(
                    "Menú",
                    color="white",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Divider(color="#3D5AFE", height=1),
                ft.Container(height=10),
                opcion_menu(ft.icons.GRID_VIEW, "Ver catálogo", ir_catalogo),
                opcion_menu(ft.icons.SHOPPING_CART, "Ir al carrito", ir_carrito),
                ft.Divider(color="#2A2A4A", height=1),
                opcion_menu(ft.icons.ADMIN_PANEL_SETTINGS, "Administrador", ir_admin),
            ],
            spacing=4,
        ),
        bgcolor="#1A1A2E",
        width=0,  # empieza oculto
        animate=ft.animation.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
    )

    campo_texto = ft.TextField(
        hint_text="Pregunta lo que quieras....",
        hint_style=ft.TextStyle(color="grey"),
        bgcolor="#2A2A2A",
        border_radius=20,
        border_color="transparent",
        color="white",
        multiline=True,
        min_lines=2,
        max_lines=4,
        expand=True,
        text_size=15,
        on_submit=enviar_mensaje,
    )

    boton_enviar = ft.Container(
        content=ft.Icon(ft.icons.ARROW_UPWARD, color="white", size=22),
        bgcolor="#3D5AFE",
        border_radius=50,
        width=48,
        height=48,
        alignment=ft.alignment.center,
        on_click=enviar_mensaje,
    )

    header = ft.Container(
        content=ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.icons.MENU,
                    icon_color="white",
                    on_click=toggle_menu,  # ← ya conectado
                ),
                ft.Text(
                    "Expertech",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color="white",
                    expand=True,
                ),
                ft.IconButton(
                    icon=ft.icons.REFRESH,
                    icon_color="white",
                    on_click=limpiar_chat
                ),
            ],
        ),
        bgcolor="#1E1E1E",
        padding=ft.padding.symmetric(horizontal=8, vertical=4),
    )

    input_bar = ft.Container(
        content=ft.Row(
            controls=[campo_texto, boton_enviar],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.END,
            spacing=8,
        ),
        bgcolor="#2A2A2A",
        border_radius=20,
        padding=ft.padding.symmetric(horizontal=12, vertical=8),
        margin=ft.margin.all(12),
    )

    # Área del chat
    area_chat = ft.Column(
        controls=[
            header,
            ft.Container(
                content=mensajes,
                expand=True,
                padding=ft.padding.symmetric(horizontal=12, vertical=8),
            ),
            input_bar,
        ],
        expand=True,
        spacing=0,
    )

    # Layout principal: menú + chat side by side
    page.add(
        ft.Row(
            controls=[
                panel_menu,
                area_chat,
            ],
            expand=True,
            spacing=0,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )
    )