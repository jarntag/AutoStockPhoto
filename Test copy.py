import flet
from flet import (
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    FilePickerFileType,
    Page,
    Row,
    Text,
    Image,
    TextField,
    Column,
    icons
)
import pandas as pd
import os

def main(page: Page):
    page.title = "Image List from Directory"
    page.window_width = 800
    page.window_height = 600

    # Text widgets to display the selected directory path
    directory_path = Text()
    csv_file_path = TextField(label="CSV File Path")

    # TextField widgets to display CSV data
    title_field = TextField(label="Title")
    keyword_field = TextField(label="Keywords")
    description_field = TextField(label="Description")

    # Container to hold image components
    image_container = Column()

    # Function to list and display images in a directory
    def list_images(directory):
        image_container.controls.clear()  # Clear previous images
        for filename in os.listdir(directory):
            if filename.lower().endswith(('.jpg', '.png', '.svg')):
                image_path = os.path.join(directory, filename)
                image_component = Row([
                    Image(src=image_path, width=200, height=200),
                    Text(filename)
                ])
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

    get_directory_dialog = FilePicker(
        on_result=get_directory_result,
        
    )

    # Function to read and display CSV data
    def read_csv(e):
        csv_path = csv_file_path.value
        if os.path.isfile(csv_path):
            df = pd.read_csv(csv_path)
            if not df.empty:
                title_field.value = df.iloc[0]['Title']
                keyword_field.value = df.iloc[0]['Keywords']
                description_field.value = df.iloc[0]['Description']
            else:
                csv_content.value = "CSV file is empty!"
        else:
            csv_content.value = "Invalid file path!"
        title_field.update()
        keyword_field.update()
        description_field.update()

    # Overlay file picker
    page.overlay.append(get_directory_dialog)

    # UI setup
    page.add(
        ElevatedButton(
            "Open Directory",
            icon=icons.FOLDER_OPEN,
            on_click=lambda _: get_directory_dialog.get_directory_path(),
            disabled=page.web,
        ),
        directory_path,
        Row([csv_file_path, ElevatedButton("Load CSV", on_click=read_csv)]),
        title_field,
        keyword_field,
        description_field,
        image_container
    )

    

# Run the app
flet.app(target=main, upload_dir="uploads", view=flet.WEB_BROWSER)
