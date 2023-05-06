import flet as ft

from ..shared.TableHeaders import *
from .ContainerRowControl import *

class ContainersControl(ft.UserControl):
    def __init__(self, dockerClient):
        super().__init__()
        self.dockerClient = dockerClient
        self.containers = []
        self.__create_controls_references__()

    def __create_controls_references__(self):
        self.containersWrapper = ft.Container()
        self.containersList = ft.Column()
        self.buttonStartAll = ft.Container()
        self.buttonReload = ft.Container()

    def __create_table_headers__(self):
        headers = [{'title': "Status", 'width': 50}]
        headers.append({"title": "Id", "width": 150}),
        headers.append({"title": "Name", "width": 200}),
        headers.append({"title": "Actions", "width": 300}),
        return TableHeaders(headers)
    
    def __create_start_all_button__(self):
        self.buttonStartAll.content = ft.TextButton(
            icon=ft.icons.PLAY_ARROW,
            text="Run all",
            disabled=len(self.containers) == 0,
            on_click=self.start_all_containers,
            data=True
        )

        return self.buttonStartAll

    def __create_reload_button__(self):
        self.buttonReload.content = ft.TextButton(
            icon=ft.icons.REFRESH,
            text="Reload containers",
            on_click=self.list_containers,
            data=True
        )

        return self.buttonReload

    def list_containers(self, listAll):
        # if assigning the var doesn't work, assign the content of the variable
        self.containersWrapper.content = ft.Container(
            content=ft.ProgressRing(),
            padding=10
        )

        self.update()

        containers = self.dockerClient.containers.list(all=listAll)
        # text.value = f"There are {len(containers)} containers"
        if (len(containers) > 0):
            self.containers = [self.__create_table_headers__()]
            for container in containers:
                self.containers.append(ContainerRowControl(container.id, self.dockerClient, None, self.__delete_container__))
            
            self.containersList.controls = self.containers
            self.containersWrapper.content = self.containersList

            self.buttonStartAll.content.disabled = False
            
        else:
            self.containersWrapper.content = ft.Text("There are no containers")
        
        self.update()


    def start_all_containers(self, startAll):
        self.containersWrapper.content = ft.Container(
            content=ft.ProgressRing(),
            padding=10
        )
        self.update()

        containers = self.dockerClient.containers.list(all=startAll)
        if (len(containers) > 0):
            for container in containers:
                container.start()
        
        self.containersWrapper.content = ft.Container()
        self.update()

        self.list_containers(startAll)

    def __delete_container__(self, container):
        self.containersList.controls.remove(container)
        self.update()

        

    def build(self):
        return ft.Column(
            controls=[
                ft.Row (
                    controls=[
                        self.__create_start_all_button__(),
                        self.__create_reload_button__()
                    ]
                ),
                self.containersWrapper
            ]
        )