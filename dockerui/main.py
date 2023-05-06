import flet as ft
import docker

from controls.TextContainerControl import *
from controls.MainDashboardControl import *
from controls.ImagesControl import *
from controls.NetworksControl import *

from controls.containers.ContainerRowControl import *
from controls.containers.ContainersControl import *

isLoading = True

dockerClient = docker.DockerClient(base_url='tcp://localhost:2375')

def main(page: ft.Page):
    page.window_width = 1000        # window's width is 200 px
    page.window_height = 600       # window's height is 200 px
    page.window_resizable = True  # window is not resizable
    page.update()

    containers = []

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
                    content=MainDashboardControl()
                ),
                ft.Tab(
                    text="Containers",
                    content=ContainersControl(dockerClient)
                ),
                ft.Tab(
                    text="Images",
                    content=ImagesControl()
                ),
                ft.Tab(
                    text="Network",
                    content=NetworksControl()
                )
            ],

            expand=1
        )


    page.add(title, center)

ft.app(target=main)