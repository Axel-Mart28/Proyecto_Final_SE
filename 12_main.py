import flet as ft
from views.welcome_view import welcome_view

def main(page: ft.Page):
    page.title = "Expertech AI - Asesor"
    page.window_width = 400
    page.window_height = 800
    page.bgcolor = "black"
    welcome_view(page)

if __name__ == "__main__":
    ft.app(target=main)