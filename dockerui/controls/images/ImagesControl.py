import flet as ft

class ImagesControl(ft.UserControl):
    def __init__(self, dockerClient):
        super().__init__()
        self.dockerClient = dockerClient
        self.__create_controls_references__()

    def __create_controls_references__(self):
        self.button_load_images = ft.Container()
        self.button_delete_selected = ft.Container()
        self.button_pull_image = ft.Container()
        self.button_build_image = ft.Container()
    
    def __create_load_images_button__(self):
        self.button_load_images = ft.TextButton(
            icon=ft.icons.REFRESH,
            text="Load images",
            on_click=self.__action_load_images__,
        )

        return self.button_load_images
    
    def __create_delete_selected_button__(self):
        self.button_delete_selected = ft.TextButton(
            icon=ft.icons.DELETE,
            text="Delete selected images",
            disabled=True,
            on_click=self.__action_delete_selected__,
        )
        
        return self.button_delete_selected
    
    def __create_pull_image_button__(self):
        self.button_pull_image = ft.TextButton(
            icon=ft.icons.DOWNLOAD,
            text="Pull image",
            on_click=self.__action_pull_image__,
        )
        
        return self.button_pull_image
    
    def __create_build_image_button__(self):
        self.button_build_image = ft.TextButton(
            icon=ft.icons.BUILD,
            text="Build image",
            tooltip="Build image from Dockerfile",
            on_click=self.__action_build_image__,
        )
        
        return self.button_build_image

    def __action_load_images__(self, args):
        return
    
    def __action_delete_selected__(self, args):
        return
    
    def __action_pull_image__(self, args):
        return

    def __action_build_image__(self, args):
        return

    def build(self):
        return ft.ListView(
            controls=[
                ft.Row(
                    controls=[
                        self.__create_load_images_button__(),
                        self.__create_delete_selected_button__(),
                        self.__create_pull_image_button__(),
                        self.__create_build_image_button__(),
                    ]
                )
            ]
        )