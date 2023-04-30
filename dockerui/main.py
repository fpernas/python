import flet as ft
import docker

from tabs.dashboard import *
from tabs.textControl import *
from tabs.controls.TextContainerControl import *

def main(page: ft.Page):
    page.window_width = 420        # window's width is 200 px
    page.window_height = 600       # window's height is 200 px
    page.window_resizable = True  # window is not resizable
    page.update()

    def list_containers(listAll):
        client = docker.DockerClient(base_url='tcp://localhost:2375')
        containers = client.containers.list(all=listAll)
        text.value = f"There are {len(containers)} containers"
        page.update()

    title = TextContainerControl("Docker Management APP")

    text = ft.Text()

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
                            ft.Container(
                                content=text
                            )
                        ]
                    )
                )
            ],

            expand=1
        )


    page.add(title, center)

ft.app(target=main)