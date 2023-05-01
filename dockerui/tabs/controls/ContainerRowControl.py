import flet as ft

class ContainerRowControl(ft.UserControl):

    def __init__(self, container, mainPage, dockerClient):
        super().__init__()
        self.container = container  # this container is not updated every time, so it would be good to obtain it every time from the client
        self.page = mainPage
        self.client = dockerClient
        self.controlToDisplay = ft.Row(
            controls=self.__create_container_info_row_controls__()
        )

    def __get_container_status__(self):
        if (self.container.status == 'exited'):
            return ft.colors.RED
        elif (self.container.status == 'running'):
            return ft.colors.GREEN
        
    def __start_container__(self, args):
        self.controlToDisplay.controls = self.__create_loading_row__()
        self.update()

        print('prior status: ', self.container.status)
        self.container.start()
        self.container = self.client.containers.get(self.container.id)
        print('post status: ', self.container.status)

        self.controlToDisplay.controls = self.__create_container_info_row_controls__()
        self.update()  # not working
    
    def __init_console_on_container__(self, args):
        return
    
    def __stream_container_logs__(self, args):
        return

    def __stop_container__(self, args):
        self.container.stop()
    
    def __delete_container__(self, args):
        return
    
    def __create_loading_row__(self):
        return [
            ft.Container(
                content=ft.ProgressRing(),
                padding=5,
                alignment=ft.alignment.center
            )
        ]

    def __create_container_info_row_controls__(self):
        return [
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
                            on_click=self.__start_container__,
                        ),
                        ft.IconButton(
                            tooltip="Console",
                            icon=ft.icons.TEXT_FIELDS_ROUNDED,
                            disabled=self.container.status != 'running',
                            on_click=self.__init_console_on_container__
                        ),
                        ft.IconButton(
                            tooltip="Logs",
                            icon=ft.icons.DOCUMENT_SCANNER_ROUNDED,
                            disabled=self.container.status != 'running',
                            on_click=self.__stream_container_logs__
                        ),
                        ft.IconButton(
                            tooltip="Stop",
                            icon=ft.icons.STOP_CIRCLE,
                            disabled=self.container.status != 'running',
                            on_click=self.__stop_container__
                        ),
                        ft.IconButton(
                            tooltip="Delete",
                            icon=ft.icons.DELETE,
                            disabled=self.container.status == 'running',
                            on_click=self.__delete_container__
                        )
                    ]
                )
            )
        ]

    def build(self):
        return self.controlToDisplay