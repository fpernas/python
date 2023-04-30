import flet as ft
import docker

from tabs.dashboard import *
from tabs.textControl import *
from tabs.controls.TextContainerControl import *
from tabs.controls.ContainerRowControl import *

isLoading = True

def main(page: ft.Page):
    page.window_width = 1000        # window's width is 200 px
    page.window_height = 600       # window's height is 200 px
    page.window_resizable = True  # window is not resizable
    page.update()

    def list_containers(listAll):
        # display loading control
        containerList.content = ft.Container(
            content=ft.ProgressRing(),
            padding=10
        )
        page.update()

        client = docker.DockerClient(base_url='tcp://localhost:2375')
        containers = client.containers.list(all=listAll)
        # text.value = f"There are {len(containers)} containers"
        containerRows = []
        if (len(containers) > 0):
            for container in containers:
                containerRows.append(ContainerRowControl(container))
            
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
                    text="Dashboard tab",
                    content=TextContainerControl("Dashboard tab")
                ),
                ft.Tab(
                    text="Containers",
                    content=ft.Column(
                        controls=[
                            ft.Row (
                                controls=[
                                    ft.ElevatedButton(
                                        "Start all",
                                        icon=ft.icons.PLAY_ARROW
                                    ),
                                    ft.ElevatedButton(
                                        "List all containers",
                                        icon=ft.icons.LIST,
                                        on_click=list_containers,
                                        data=True
                                    )
                                ]
                            ),
                            containerList
                        ]
                    )
                )
            ],

            expand=1
        )


    page.add(title, center)

ft.app(target=main)