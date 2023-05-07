import flet as ft

from ..shared.TableHeaders import *
from ..shared.LoadingRingControl import *
from ..shared.DockerContainerUtils import *

from .ContainerRowControl import *

class ContainersControl(ft.UserControl):
    def __init__(self, dockerClient):
        super().__init__()
        self.dockerClient = dockerClient
        self.containers = []
        self.selected_containers = []
        self.__create_controls_references__()

    def __create_controls_references__(self):
        self.containersWrapper = ft.Container()
        self.containersList = ft.Column()
        
        self.button_load_containers = ft.Container()
        self.button_start_selected = ft.Container()
        self.button_delete_selected = ft.Container()
        self.button_create_container = ft.Container()

    def __create_table_headers__(self):
        headers = [{'title': "Status", 'width': 50}]
        headers.append({"title": "Id", "width": 150}),
        headers.append({"title": "Name", "width": 200}),
        headers.append({"title": "Actions", "width": 300}),
        return TableHeaders(headers)
    
    def __create_start_selected_button__(self):
        self.button_start_selected.content = ft.TextButton(
            icon=ft.icons.PLAY_ARROW,
            text="Run selected containers",
            disabled=True,
            on_click=self.__start_selected_containers__,
            data=True
        )

        return self.button_start_selected

    def __create_load_button__(self):
        self.button_load_containers.content = ft.TextButton(
            icon=ft.icons.REFRESH,
            text="Load containers",
            on_click=self.__list_containers__,
            data=True
        )

        return self.button_load_containers
    
    def __create_delete_selected_button__(self):
        self.button_delete_selected.content = ft.TextButton(
            icon=ft.icons.DELETE,
            text="Delete selected containers",
            on_click=self.__delete_selected_containers__,
            disabled=True
        )

        return self.button_delete_selected
    
    def __create_add_container_button__(self):
        self.button_create_container.content = ft.TextButton(
            icon=ft.icons.ADD,
            text="Add new container",
            tooltip="Not implemented yet",
            on_click=self.__create_new_container__
        )

        return self.button_create_container

    def __list_containers__(self, listAll):
        self.containersWrapper.content = LoadingRingControl(10)
        self.update()

        containers = self.dockerClient.containers.list(all=listAll)
        if (len(containers) > 0):
            self.containers = [self.__create_table_headers__()]
            for container in containers:
                self.containers.append(
                    ContainerRowControl(container.id, self.dockerClient, self.__delete_container__, self.__select_container__)
                )
            
            self.containersList.controls = self.containers
            self.containersWrapper.content = self.containersList
        else:
            self.containersWrapper.content = ft.Text("There are no containers")
        
        self.update()


    def __start_selected_containers__(self, startAll):
        if (len(self.selected_containers) == 0):
            print("There are no containers to run")
            return
        
        self.containersWrapper.content = LoadingRingControl(10)
        self.update()

        for container_id in self.selected_containers:
            container = get_container_by_id(self.dockerClient, container_id)
            if (container != None and container.status != 'running'):
                container.start()
        
        self.containersWrapper.content = ft.Container()
        self.update()

        self.__list_containers__(startAll)

    def __delete_selected_containers__(self, args):
        # If one couldnt be delete, log and show toast
        if (len(self.selected_containers) == 0):
            print("There are no  containers to delete")
            return
        
        self.containersWrapper.content = LoadingRingControl(10)
        self.update()

        for container_id in self.selected_containers:
            container = get_container_by_id(self.dockerClient, container_id)
            if (container != None and container.status != 'running'):
                container.remove()
        
        self.selected_containers = []

        self.__list_containers__(True)

    def __create_new_container__(self, args):
        print("Not implemented yet")

    def __delete_container__(self, container):
        self.containersList.controls.remove(container)
        self.update()

    def __select_container__(self, control):
        try:
            self.selected_containers.index(control.get_container_id())
            self.selected_containers.remove(control.get_container_id())
        except ValueError:
            self.selected_containers.append(control.get_container_id())
        
        self.button_start_selected.content.disabled = len(self.selected_containers) == 0
        self.button_delete_selected.content.disabled = len(self.selected_containers) == 0
        self.update()

    def build(self):
        return ft.ListView(
            controls=[
                ft.Row (
                    controls=[
                        self.__create_load_button__(),
                        self.__create_start_selected_button__(),
                        self.__create_delete_selected_button__(),
                        self.__create_add_container_button__()
                    ]
                ),
                self.containersWrapper
            ]
        )