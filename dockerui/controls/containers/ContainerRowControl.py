import flet as ft
import docker

# need to try-catch when executing container operations

class ContainerRowControl(ft.UserControl):

    # show logs in a hidden container, not in a modal
    # in that way, page shouldn't be needed
    def __init__(self, container_id, dockerClient, page, delete_op):
        super().__init__()
        self.client = dockerClient
        self.page = page
        self.container_id = container_id
        self.delete_container_op = delete_op
        self.container = self.__get_container_from_client__()
        self.controlToDisplay = ft.Row( controls=self.__create_container_info_row_controls__() )

    def __get_container_from_client__(self):
        try:
            return self.client.containers.get(self.container_id)
        except docker.errors.NotFound:
            print(f"container with id {self.container_id} not found")
            return None

    def __get_container_status__(self):
        container = self.__get_container_from_client__()
        if (container != None):
            if (container.status == 'exited'):
                return ft.colors.RED
            elif (container.status == 'running'):
                return ft.colors.GREEN
        else:
            return ft.colors.GREY
        
    def __start_container__(self, args):
        self.controlToDisplay.controls = self.__create_loading_row__()
        self.update()

        container = self.__get_container_from_client__()
        if (container != None):
            self.container.start()
            self.container = self.client.containers.get(self.container.id)

            self.controlToDisplay.controls = self.__create_container_info_row_controls__()
            self.update()
    
    def __init_console_on_container__(self, args):
        return
    
    def __close_modal__(self, args):
        self.modal.open = False
        self.page.update()
    
    def __stream_container_logs__(self, args):
        logRows = ft.ListView(
            controls=[],
            auto_scroll=True,
            width=700,
            height=200,
            spacing=-10,
            padding=0
        )

        self.modal = ft.AlertDialog(
            modal=True,
            content=logRows,
            actions=[ft.TextButton(text="Close", on_click=self.__close_modal__)],
            on_dismiss=lambda e: print("como cierro el stream?")
        )

        self.page.dialog = self.modal
        self.modal.open = True
        self.page.update()

        logRowsArray = []
        for log in self.container.logs(stream=True):
            logLine = log.decode('UTF-8')
            if (len(logLine.strip()) > 0):
                logRowsArray.append(ft.Text(logLine))
                logRows.controls = logRowsArray
                self.page.update()

    def __stop_container__(self, args):
        self.controlToDisplay.controls = self.__create_loading_row__()
        self.update()

        self.container.stop()
        self.container = self.client.containers.get(self.container.id)

        self.controlToDisplay.controls = self.__create_container_info_row_controls__()
        self.update()
    
    def __delete_container__(self, args):
        try:
            docker_container = self.client.containers.get(self.container_id)
            if (docker_container.status != 'running'):
                docker_container.remove()
                self.delete_container_op(self)
            else:
                print("container is running")
        except docker.errors.NotFound:
            print("container not found")
        except docker.errors.APIError:
            print("there was a problem")
        
    
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
                width=50,
                content=ft.Container(
                    tooltip="Status",
                    width = 10,
                    height = 10,
                    bgcolor=self.__get_container_status__()
                )
            ),
            ft.Container(
                content=ft.Text(f"{self.container.short_id}"),
                width=150
            ),
            ft.Container(
                content=ft.Text(f"{self.container.name}"),
                width=200
            ),
            ft.Container(
                width = 300,
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