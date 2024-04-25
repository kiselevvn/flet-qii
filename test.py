import csv
import math

import flet as ft
import numpy as np

from src.core.sys_analysis import FunctionalCompleteness

# with open("myfile.txt", "w") as file1:
#     def get_row(index):
#         row = [f"Programmer №{index}",]
#         for i in range(1,8):
#             row.append(str(round(np.random.random_sample()*i*3, 2)))
#         return row
#     # Writing data to a file
#     for i in range(1, 11):
#         file1.write(",".join(get_row(i))+"\n")



def get_table(path="", title=""):
    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        reader_list = list(reader)
        # print(reader)
        # [[print(cell) for cell in row] for row in reader][0]
        rows = []
        for row in reader_list:
            cells = []
            for cell in row:
                # print(cell)
                cells.append(ft.DataCell(ft.Text((cell))))
                # print(cells)
            rows.append(ft.DataRow(cells=cells))
            # print(rows)
        # print()
        columns = []
        columns.append(ft.DataColumn(ft.Text("ID")))
        for cell in range(1, len(reader_list[0])-1):
            columns.append(ft.DataColumn(ft.Text(f"{cell}")))

        # rows = [ft.DataRow(cells=[ for cell in row]) for row in reader]
        # print(rows)
        obj = ft.DataTable(
            columns=columns,
            rows=rows,
        )

        return obj

def get_rail(config={}):
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        # extended=True,
        min_width=100,
        min_extended_width=400,
        leading=ft.FloatingActionButton(icon=ft.icons.CREATE, text="Add"),
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.FAVORITE_BORDER, selected_icon=ft.icons.FAVORITE, label="First"
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.BOOKMARK_BORDER),
                selected_icon_content=ft.Icon(ft.icons.BOOKMARK),
                label="Second",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.SETTINGS_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.SETTINGS),
                label_content=ft.Text("Settings"),
            ),
        ],
        on_change=lambda e: print("Selected destination:", e.control.selected_index),
    )
    return rail

# ft.DataRow(
                #     cells=[
                #         ft.DataCell(ft.Text("John")),
                #         ft.DataCell(ft.Text("Smith")),
                #         ft.DataCell(ft.Text("43")),
                #     ],
                # ),
                # ft.DataRow(
                #     cells=[
                #         ft.DataCell(ft.Text("Jack")),
                #         ft.DataCell(ft.Text("Brown")),
                #         ft.DataCell(ft.Text("19")),
                #     ],
                # ),
                # ft.DataRow(
                #     cells=[
                #         ft.DataCell(ft.Text("Alice")),
                #         ft.DataCell(ft.Text("Wong")),
                #         ft.DataCell(ft.Text("25")),
                #     ],
                # ),
def main(page: ft.Page):
    page.title = "Routes Example"

    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("Flet app"), bgcolor=ft.colors.SURFACE_VARIANT),
                    ft.ElevatedButton("Visit Store", on_click=lambda _: page.go("/data")),
                ],
            )
        )
        if page.route == "/data":
            page.views.append(
                ft.View(
                    "/data",
                    [
                        ft.Row(
                            [
                                get_rail(),
                                ft.VerticalDivider(width=1),
                                get_table(path=".\data\programmers.csv"),
                            ],
                            expand=True,
                        ),
                    ],
                )

            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(target=main, view=ft.AppView.WEB_BROWSER)