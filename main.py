import flet as ft
from app import App

if __name__ == "__main__":
    
    def main(page: ft.Page):
        page.title = "Password Manager"
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.auto_scroll = True
        page.scroll = ft.ScrollMode.HIDDEN
        
        app = App(page)
        page.update()
 
    ft.app(main)