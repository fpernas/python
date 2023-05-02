import flet as ft
import docker

from tabs.dashboard import *
from tabs.textControl import *
from tabs.controls.TextContainerControl import *
from tabs.controls.ContainerRowControl import *

isLoading = True

dockerClient = docker.DockerClient(base_url='tcp://localhost:2375')

def main(page: ft.Page):
    page.window_width = 1000        # window's width is 200 px
    page.window_height = 600       # window's height is 200 px
    page.window_resizable = True  # window is not resizable
    page.update()

    containers = []

    def create_containers_table_headers():
        return ft.Row(
            controls=[
                ft.Container(
                    content=ft.Checkbox(
                        tooltip="Select all"
                    ),
                ),
                ft.Container( 
                    content=ft.Text("Status"), 
                    width=50
                ),
                ft.Container( 
                    content=ft.Text("Short id"),
                    width=150 
                ),
                ft.Container( 
                    content=ft.Text("Name"),
                    width=200 
                ),
                ft.Container( 
                    content=ft.Text("Actions"),
                    width=300 
                )
            ]
        )

    def list_containers(listAll):

        # modal = ft.AlertDialog(
        #     modal=True,
        #     content=ft.Text("something!")
        # )

        # page.dialog = modal
        # modal.open = True
        # display loading control
        containerList.content = ft.Container(
            content=ft.ProgressRing(),
            padding=10
        )
        page.update()

        containers = dockerClient.containers.list(all=listAll)
        # text.value = f"There are {len(containers)} containers"
        containerRows = [create_containers_table_headers()]
        if (len(containers) > 0):
            for container in containers:
                containerRows.append(ContainerRowControl(container.id, dockerClient, page))
            
            containerList.content = ft.Column(
                controls=containerRows
            )

            page.update()
        else:
            containerList.content = ft.Text("There are no containers")


    title = TextContainerControl("Docker Management APP")

    # text = ft.Text()
    containerList = ft.Container(
        content=ft.Text("There are no containers"),
        alignment=ft.alignment.center
    )

    center = ft.Tabs (
            selected_index=1,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="Dashboard",
                    content=TextContainerControl("Dashboard tab")
                ),
                ft.Tab(
                    text="Containers",
                    content=ft.Column(
                        controls=[
                            ft.Row (
                                controls=[
                                    ft.Container(
                                        content=ft.TextButton(
                                            icon=ft.icons.PLAY_ARROW,
                                            text="Run all",
                                            disabled=len(containers) == 0
                                        )
                                    ),
                                    ft.Container(
                                        content=ft.TextButton(
                                            icon=ft.icons.REFRESH,
                                            text="Reload containers",
                                            on_click=list_containers,
                                            data=False
                                        )
                                    )
                                ]
                            ),
                            containerList
                        ]
                    )
                ),
                ft.Tab(
                    text="Images",
                ),
                ft.Tab(
                    text="Network"
                )
            ],

            expand=1
        )


    page.add(title, center)

ft.app(target=main)