import flet as ft

class ContainerRowControl(ft.UserControl):
    def __init__(self, container):
        super().__init__()
        self.container = container

    def __get_container_status__(self):
        if (self.container.status == 'exited'):
            return ft.colors.RED
        elif (self.container.status == 'running'):
            return ft.colors.GREEN
    
    def build(self):
        return ft.Row(
            controls=[
                ft.Checkbox(
                    tooltip="Select to initiate",
                    value=False
                ),
                ft.Container(
                    tooltip="Status",
                    width = 10,
                    height = 10,
                    bgcolor=self.__get_container_status__()
                ),
                ft.Container(
                    content=ft.Text(f"{self.container.short_id}")
                ),
                ft.Container(
                    content=ft.Text(f"{self.container.name}")
                ),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.IconButton(
                                tooltip="Run",
                                icon=ft.icons.PLAY_CIRCLE,
                                disabled=self.container.status == 'running',
                            ),
                            ft.IconButton(
                                tooltip="Stop",
                                icon=ft.icons.STOP_CIRCLE,
                                disabled=self.container.status != 'running',
                            ),
                            ft.IconButton(
                                tooltip="Delete",
                                icon=ft.icons.DELETE,
                                disabled=self.container.status != 'running',
                            )
                        ]
                    )
                )
            ]
        )