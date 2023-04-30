import flet as ft

class DashboardTabControl(ft.UserControl):
    def build(self):
        return ft.Tab(
            text="Dashboard tab",
            content=ft.Container(
                content=ft.Text("Main Windows Content"),
            )
        )