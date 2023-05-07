import flet as ft

class LoadingRingControl(ft.UserControl):
    def __init__(self, padding):
        super().__init__()
        self.padding = padding
    
    def build(self):
        return ft.Container(
            content=ft.ProgressRing(),
            padding=self.padding,
            alignment=ft.alignment.center
        )