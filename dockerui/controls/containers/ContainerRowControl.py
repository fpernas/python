import flet as ft
import docker

from ..shared.DockerContainerUtils import *
from ..shared.LoadingRingControl import *

# need to try-catch when executing container operations

class ContainerRowControl(ft.UserControl):

    # show logs in a hidden container, not in a modal
    # in that way, page shouldn't be needed
    def __init__(self, container_id, dockerClient, delete_op, select_op):
        super().__init__()
        self.docker_client = dockerClient
        self.container_id = container_id
        self.delete_container_op = delete_op
        self.select_container_op = select_op
        self.container = get_container_by_id(self.docker_client, self.container_id)
        self.row_control = ft.Column( controls=[] )
        self.__create_controls_references__()

    def __create_controls_references__(self):
        self.row_wrapper = ft.Container()
        
        self.log_wrapper = ft.Column()
        self.log_row_list_view = ft.ListView()

    def __get_container_status__(self):
        container = get_container_by_id(self.docker_client, self.container_id)
        if (container != None):
            if (container.status == 'exited'):
                return ft.colors.RED
            elif (container.status == 'running'):
                return ft.colors.GREEN
        else:
            return ft.colors.GREY
    
    def __init_console_on_container__(self, args):
        print("not yet implemented")
    
    def __stream_container_logs__(self, args):
        self.log_wrapper.visible = True
        self.update()

        logRowsArray = []
        for log in self.container.logs(stream=True):
            logLine = log.decode('UTF-8')
            if (len(logLine.strip()) > 0):
                logRowsArray.append(ft.Text(logLine.strip()))
                self.log_row_list_view.controls = logRowsArray
                self.update()

    def __start_container__(self, args):
        self.__create_loading_ring__()

        docker_container = get_container_by_id(self.docker_client, self.container_id)
        if (docker_container != None and docker_container.status != 'running'):
            docker_container.start()
        elif (docker_container.status == 'running'):
            print("Container is already running")

        self.__display_row__()

    def __stop_container__(self, args):
        self.__create_loading_ring__()

        docker_container = get_container_by_id(self.docker_client, self.container_id)
        if (docker_container != None and docker_container.status == 'running'):
            docker_container.stop()
        elif (docker_container.status != 'running'):
            print("container already running")

        self.__display_row__()
    
    def __delete_container__(self, args):
        self.__create_loading_ring__()
        
        docker_container = get_container_by_id(self.docker_client, self.container_id)
        if (docker_container != None and docker_container.status != 'running'):
            docker_container.remove()
            self.delete_container_op(self)
        elif (docker_container.status == 'running'):
            print("To delete a container it cannot be running")

        self.__display_row__()
        
    def __on_checkbox_selected__(self, data):
        return self.select_container_op(self)

    def __create_loading_ring__(self):
        self.row_control.controls = [LoadingRingControl(5)]
        self.update()

    def __display_row__(self):
        # instead of re-drawing everything, I should keep actions in variables
        # and update their status after some operation is performed
        self.row_control.controls = self.__create_container_info_row_controls__()
        self.update()
    
    def __create_row_to_display__(self):
        # create two rows: one with the info, etc, and the other with the log container
        self.row_control.controls = self.__create_container_info_row_controls__()
        self.row_control.controls.append(self.__create_container_log_control__())

        return self.row_control

    def __close_log_container__(self, args):
        self.log_row_list_view.controls = []
        self.log_wrapper.visible = False
        self.update()

    def __create_container_log_control__(self):
        row_closing_icon = ft.Row(
            controls=[
                ft.Container(
                    width=800,
                    content=ft.Container(
                        content=ft.IconButton(
                            icon=ft.icons.CLOSE,
                            tooltip="Close",
                            on_click=self.__close_log_container__,
                        ),
                        alignment=ft.alignment.top_right,
                    ),
                    bgcolor=ft.colors.AMBER,
                    alignment=ft.alignment.top_center,
                )
            ]
        )

        self.log_row_list_view.width = 800
        self.log_row_list_view.height = 200
        self.log_row_list_view.spacing = -10
        self.log_row_list_view.padding = 0
        self.log_row_list_view.auto_scroll = True
        self.log_row_list_view.controls = []

        row_displaying_info = ft.Row(
            controls=[
                ft.Container(
                    content=self.log_row_list_view,
                )
            ]
        ) 

        self.log_wrapper.visible = False
        self.log_wrapper.controls = [
            row_closing_icon,
            row_displaying_info
        ]

        return self.log_wrapper

    def __create_container_info_row_controls__(self):
        return [
            ft.Row(
                controls=[
                    ft.Checkbox(
                        value=False,
                        on_change=self.__on_checkbox_selected__
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
                                    disabled=get_container_status(self.docker_client, self.container_id) == 'running',
                                    on_click=self.__start_container__,
                                ),
                                ft.IconButton(
                                    tooltip="Console (not implemented)",
                                    icon=ft.icons.TEXT_FIELDS_ROUNDED,
                                    disabled=get_container_status(self.docker_client, self.container_id) != 'running',
                                    on_click=self.__init_console_on_container__
                                ),
                                ft.IconButton(
                                    tooltip="Logs",
                                    icon=ft.icons.DOCUMENT_SCANNER_ROUNDED,
                                    disabled=get_container_status(self.docker_client, self.container_id) != 'running',
                                    on_click=self.__stream_container_logs__
                                ),
                                ft.IconButton(
                                    tooltip="Stop",
                                    icon=ft.icons.STOP_CIRCLE,
                                    disabled=get_container_status(self.docker_client, self.container_id) != 'running',
                                    on_click=self.__stop_container__
                                ),
                                ft.IconButton(
                                    tooltip="Delete",
                                    icon=ft.icons.DELETE,
                                    disabled=get_container_status(self.docker_client, self.container_id) == 'running',
                                    on_click=self.__delete_container__
                                )
                            ]
                        )
                    )
                ]
                
            ),
        ]

    def get_container_id(self):
        return self.container_id

    def build(self):
        return self.__create_row_to_display__()