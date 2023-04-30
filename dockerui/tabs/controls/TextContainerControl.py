import flet as ft

class TextContainerControl(ft.UserControl):
    def __init__(self, mssg):
        super().__init__()
        self.message = mssg
    
    def build(self):
        return ft.Container(
            content=ft.Text(self.message),
            alignment=ft.alignment.center
        )