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
import os

os.environ["FLET_SECRET_KEY"] = os.urandom(12).hex()
secret_key = "1234"


def main(page: Page):
    page.title = "Image Metadata Viewer"
    page.window_width = 800
    page.window_height = 600


    # Save file dialog
    def save_txt_change(e):
        save_txt.value = save_txt_contant.value

    def save_file_result(e:FilePickerResultEvent):
        save_location = e.path
        if save_location:
            try:
                with open(save_location,"w",encoding="utf-8") as file:
                    print("save sucsesss")
                    file.write(save_txt_contant.value)
                    save_file_path.value = e.path 
                    save_file_path.update()
            except Exception as e:
                print("save error",e)
        save_file_path.update()
        
    save_file_dialog = FilePicker(on_result=save_file_result)
    save_file_path = Text()
    save_txt = Text()
    save_txt_contant=TextField(label="Auto adjusted height with max lines",
        multiline=True,min_lines=1,max_lines=3,value="hello save file txtt", on_change=save_txt_change,)

    # hide all dialogs in overlay
    page.overlay.extend([save_file_dialog,])

    # UI setup
    page.add(
        
        Row(
            [
                ElevatedButton(
                    "Save file",
                    icon=icons.SAVE,
                    on_click=lambda _: save_file_dialog.save_file(file_name="metadata.csv",
                    initial_directory="uploads",file_type=FilePickerFileType.CUSTOM,
                    allowed_extensions=["csv"]),
                    disabled=page.web,
                    
                ),
                save_file_path,
                
                
            ]
        ),
        Row(
            [save_txt_contant]
        ),
    )

    

# Run the app
flet.app(target=main)
