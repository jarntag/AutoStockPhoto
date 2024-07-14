from typing import Dict
import os
import flet
from flet import (
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

)
import pandas as pd
import exiftool

os.environ["FLET_SECRET_KEY"] = os.urandom(12).hex()

def main(page: Page):
    page.title = "Image List from Directory"
    page.window_width = 800
    page.window_height = 1000

    # File pick
    prog_bars: Dict[str, ProgressRing] = {}
    files = Ref[Column]()
    upload_button = Ref[ElevatedButton]()

    # File pick
    def file_picker_result(e: FilePickerResultEvent):
        upload_button.current.disabled = True if e.files is None else False
        prog_bars.clear()
        files.current.controls.clear()
        if e.files is not None:
            for f in e.files:
                prog = ProgressRing(value=0, bgcolor="#eeeeee", width=20, height=20)
                prog_bars[f.name] = prog
                files.current.controls.append(Row([prog, Text(f.name)]))
        page.update()

    def on_upload_progress(e: FilePickerUploadEvent):
        prog_bars[e.file_name].value = e.progress
        prog_bars[e.file_name].update()    

    file_picker = FilePicker(on_result=file_picker_result, on_upload=on_upload_progress)

    def upload_files(e):
        uf = []
        if file_picker.result is not None and file_picker.result.files is not None:
            for f in file_picker.result.files:
                uf.append(
                    FilePickerUploadFile(
                        f.name,
                        upload_url=page.get_upload_url(f.name, 60),
                    )
                )
            file_picker.upload(uf)


    # Text widget to display the selected directory path
    directory_path = Text()
    result_text = Text()
    t = Text(value="", size=12)

    title_field = TextField(label="Title")
    
    # Container to hold image components
    image_container = flet.GridView(height=400,
        width=800,
        runs_count=5,
        max_extent=150,
        child_aspect_ratio=1.0,
        spacing=5,
        run_spacing=5,)

    
    def embed_metadata(e):
        folder_path = page.session.get("selected_folder")
        if folder_path and os.path.isdir(folder_path):
            df = pd.read_csv("metadata.csv")
            with exiftool.ExifTool() as et:
                for index, row in df.iterrows():
                    file_path = os.path.join(folder_path, row['filename'])
                    if os.path.isfile(file_path):
                        metadata = {
                            "Title": row['title'],
                            "Keywords": row['keyword'],
                            "Description": row['description']
                        }
                        et.execute(*[f"-{k}={v}" for k, v in metadata.items()], file_path)
            result_text.value = "Metadata embedded into images successfully!"
        else:
            result_text.value = "Please select a valid folder!"
        page.update()

    # Function to list and display images in a directory
    def list_images(directory):
        image_container.controls.clear()  # Clear previous images
        for filename in os.listdir(directory):
            if filename.lower().endswith(('.jpg', '.png', '.svg')):
                image_path = os.path.join(directory, filename)
                image_component = Row([
                    Image(src=image_path, width=150, height=150,
                        fit=ImageFit.COVER,
                        repeat=ImageRepeat.NO_REPEAT,
                        border_radius=border_radius.all(10),tooltip=filename, ),
                    Text(filename)
                ])
                Row([Text(filename)])
                image_container.controls.append(image_component)
        page.update()

    # FilePicker dialog to select a directory
    def get_directory_result(e: FilePickerResultEvent):
        if e.path:
            directory_path.value = e.path
            list_images(e.path)
        else:
            directory_path.value = "Cancelled!"
        directory_path.update()

    get_directory_dialog = FilePicker(on_result=get_directory_result)
       
    
 # hide all dialogs in overlay
    page.overlay.extend([ get_directory_dialog, file_picker])

    # UI setup
    page.add(
        # Appbar
        AppBar(
            leading=Icon(icons.WALLPAPER),
            leading_width=40,
            title=Text("Image Metadata Embedder"),
            center_title=False,
            bgcolor=colors.SURFACE_VARIANT,
            actions=[
                IconButton(icons.WB_SUNNY_OUTLINED),
                IconButton(icons.FILTER_9),
                PopupMenuButton(
                    items=[
                        PopupMenuItem(text="Item 1"),
                        PopupMenuItem(),  # divider
                        PopupMenuItem(
                            text="Checked item",
                            checked=False,
                        ),
                    ]
                ),
            ],
        ),
        # Open Directory
        ElevatedButton(
            "Open Directory",
            icon=icons.FOLDER_OPEN,
            on_click=lambda _: get_directory_dialog.get_directory_path(),
            disabled=page.web,
        ),
        directory_path,
        Text(value="Title : "),
        Text(value="Keywords : "),
        image_container,
        ElevatedButton("CSV File",
            on_click=embed_metadata,
            icon=icons.EDIT_NOTE,
            ),
            
        result_text,

        # upload csv file
        ElevatedButton(
            "Select files...",
            icon=icons.FOLDER_OPEN,
            on_click=lambda _: file_picker.pick_files(allow_multiple=True),
        ),
        Column(ref=files),
        ElevatedButton(
            "Upload",
            ref=upload_button,
            icon=icons.UPLOAD,
            on_click=upload_files,
            disabled=True,
        ),

        TextField(value=f"{t.value}",
            label="CSV Value",
            on_change="",
            ),
        ElevatedButton("Embed Metadata",
            on_click=embed_metadata,
            icon=icons.EDIT_NOTE,
            ),
            
        result_text,

    )

    # Overlay file picker
    page.overlay.extend([get_directory_dialog, file_picker])

# Run the app
flet.app(target=main, upload_dir="uploads", )
