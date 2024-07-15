import flet as ft
"""from flet import (
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    FilePickerUploadEvent,
    FilePickerUploadFile,
    FilePickerFileType,
    Page,
    Row,
    Text,
    Image,
    icons,
    GridView,
    ImageFit,
    ImageRepeat,
    border_radius,
    TextField,
    AppBar,
    Icon,
    colors,
    IconButton,
    PopupMenuButton,
    PopupMenuItem,
    ProgressRing,
    Ref,
    Column,
)"""
import pandas as pd
import exiftool
import os

# async def function  \\\\\\\\\\
# Chip function
def chip_select():
    async def amenity_selected(e):
        await amenity_chips.update_async()

    title = ft.Row([ft.Icon(ft.icons.HOTEL_CLASS), ft.Text("Amenities")])
    amenities = ["Washer / Dryer", "Ramp access", "Dogs OK", "Cats OK", "Smoke-free"]
    amenity_chips = ft.Row()

    for amenity in amenities:
        amenity_chips.controls.append(
            ft.Chip(
                label=ft.Text(amenity),
                on_select=amenity_selected,
            )
        )
    return ft.Column(controls=[title, amenity_chips])  

# Main page  \\\\\\\\\\
def main(page: ft.Page):

    # Page config \\\\\\\\\\
    page.title = "Image Metadata Viewer"
    page.window_width = 1000
    page.window_height = 1000

    # Text widget to display the selected directory path
    directory_path = ft.Text()
    csv_file_path = ft.TextField(label="CSV File Path",width=400)

    # Container to hold image components
    image_container = ft.GridView( runs_count=5, max_extent=150,
        child_aspect_ratio=1.0, spacing=10,)
    # Define the image container and image count label
    image_count_label = ft.Text(value="Total Images: 0")

    # Container to hold image components
    csv_data_container = ft.Column()
   

    #Function \\\\\\\\\\

    # Function to list and display images in a directory
    def list_images(directory):
        image_container.controls.clear()  # Clear previous images
        image_count = 0  # Initialize image count
        for filename in os.listdir(directory):
            if filename.lower().endswith(('.jpg', '.png', '.svg')):
                image_path = os.path.join(directory, filename)
                image_component = ft.Stack([
                    ft.Image(src=image_path, width=150, height=150,
                        border_radius=ft.border_radius.all(10),tooltip=filename,fit=ft.ImageFit.COVER
                        ),
                    ft.Container(
                    content=ft.CircleAvatar(bgcolor=ft.colors.GREEN, radius=5),
                    alignment=ft.alignment.bottom_left,margin=5,
                        ),
                    ft.Container(
                    content=ft.TextField(label="Standard"),
                    alignment=ft.alignment.bottom_left,margin=5,
                        ),    
                ],)
                image_container.controls.append(image_component)
                image_count += 1  # Increment image count
        
        # Update the label with the image count
        image_count_label.value = f"Total Images: {image_count}"
        page.update()

    # FilePicker dialog to select a directory
    def get_directory_result(e: ft.FilePickerResultEvent):
        if e.path:
            directory_path.value = e.path
            list_images(e.path)
        else:
            directory_path.value = "Cancelled!"
        directory_path.update()
    get_directory_dialog = ft.FilePicker(on_result=get_directory_result)

    # Pick files dialog
    def pick_files_result(e: ft.FilePickerResultEvent):
        csv_file_path.value = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else "Cancelled!"
        )
        csv_file_path.update()

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    selected_files = ft.Text()

    # Function to read and display CSV data
    def read_csv(e):
        csv_path = csv_file_path.value
        if os.path.isfile(csv_path):
            df = pd.read_csv(csv_path)
            if not df.empty:
                csv_data_container.controls.clear()
                for idx, row in df.iterrows():
                    keywords_list = row['Keywords'].split(';')
                    keyword_texts = [ft.Chip(label=ft.Text(keyword),on_select=chip_select, selected=True) for i, keyword in enumerate(keywords_list)]
                        
                    csv_data_container.controls.append(
                        ft.Column([
                            ft.Text(f"Row {idx + 1}"),
                            ft.TextField(label="Title", value=row['Title']),
                            ft.Row([*keyword_texts]),
                            ft.TextField(label="Description", value=row['Description']),
                        ])
                    )
                csv_data_container.update()
            else:
                csv_data_container.value = "CSV file is empty!"
        else:
            csv_data_container.value = "Invalid file path!"
        csv_data_container.update()

    #Contant \\\\\\\\\\
    #Appbar
    appbar=ft.AppBar(
            leading=ft.Icon(ft.icons.PALETTE),
            leading_width=40,
            title=ft.Text("AppBar Example"),
            center_title=False,
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
            ft.IconButton(ft.icons.WB_SUNNY_OUTLINED),
            ft.IconButton(ft.icons.FILTER_3),
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="Item 1"),
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(
                        text="Checked item", checked=False, on_click=""
                    ),
                ]
            ),
        ],
        )
    
    #Button
    open_directory_bt=ft.ElevatedButton("Open directory",
        icon=ft.icons.FOLDER_OPEN,
        on_click=lambda _: get_directory_dialog.get_directory_path(),
        disabled=page.web,
    )
    pick_csv_bt=ft.ElevatedButton("Pick csv files",
        icon=ft.icons.UPLOAD_FILE,
        on_click=lambda _: pick_files_dialog.pick_files(
            allow_multiple=True,
        file_type=ft.FilePickerFileType.CUSTOM,
        allowed_extensions=["csv"]),
    )

    # hide all dialogs in overlay
    page.overlay.extend([pick_files_dialog, get_directory_dialog])

    # UI setup
    page.add(
        appbar,
        ft.Row([
            open_directory_bt,directory_path,image_count_label
            ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        
         # Image contant layout
        ft.Row(
            [
                ft.Container(
                    content=image_container,
                    #bgcolor=ft.colors.ORANGE_300,
                    alignment=ft.alignment.top_center,
                    expand=True,
                ),
                ft.VerticalDivider(),
                ft.Container(
                    content=ft.Column([ft.Text("Metadata"),
                        ft.Container(content=ft.Image(src="uploads\dd.jpg",  height=150,
                        border_radius=ft.border_radius.all(10),fit=ft.ImageFit.FIT_WIDTH,),
                        alignment=ft.alignment.center),               
                        ft.TextField(label="Title"),
                        ft.TextField(label="Keywords", multiline=True,value="line1\nline2\nline3\nline4\nline5",),
                        ft.Chip(label=ft.Text("Keywords01"),on_select=chip_select, selected=True),
                        ft.Chip(label=ft.Text("Keywords01"),on_select=chip_select, selected=True),
                        ft.Chip(label=ft.Text("Keywords01"),on_select=chip_select, selected=True),
                        ft.Chip(label=ft.Text("Keywords01"),on_select=chip_select, selected=True),
                        ft.Chip(label=ft.Text("Keywords01"),on_select=chip_select, selected=True),
                        ]),
                    #bgcolor=ft.colors.BROWN_400,
                    alignment=ft.alignment.top_left,
                    expand=False,
                ),
            ],
            spacing=0,
            expand=True,
        ),
        # Pick csv files
        ft.Row([pick_csv_bt,selected_files,]),
        # Load csv data
        ft.Row([csv_file_path, ft.ElevatedButton("Load csv data", on_click=read_csv)]),
        csv_data_container,

        ft.Row([]),
        ft.Row([]),        
        ft.Row([]),
        
    )


# Run the app
ft.app(target=main)    