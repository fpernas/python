import flet as ft

class TableHeaders(ft.UserControl):

    def __init__(self, tableHeaders):
        super().__init__()
        self.tableHeaders = tableHeaders

    def build(self):
        headers = [ ft.Container(content=ft.Checkbox(tooltip="Select all")) ]
        for tableHeader in self.tableHeaders:
            headers.append(ft.Container(
                content=ft.Text(tableHeader['title']),
                width=tableHeader['width']
            ))

        return ft.Row(controls=headers)