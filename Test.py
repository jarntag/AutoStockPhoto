import flet
from flet import (
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    Page,
    Row,
    Text,
    Image,
    TextField,
    icons,
    FilePickerFileType,
    Column
)
import pandas as pd
import os

def main(page: Page):
    page.title = "Image List from Directory"
    page.window_width = 800
    page.window_height = 600

    # Text widgets to display the selected directory path and CSV file contents
    directory_path = Text()
    csv_content = Text()

    # TextField widgets to display CSV data
    title_field = TextField(label="Title")
    keyword_field = TextField(label="Keyword")
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

    # FilePicker dialog to upload CSV file
    def upload_csv_result(e: FilePickerResultEvent):
        if e.files:
            csv_file_path = e.files[0].path
            df = pd.read_csv(csv_file_path)
            if not df.empty:
                # Assuming the CSV has columns: title, keyword, description
                title_field.value = df.iloc[0]['title']
                keyword_field.value = df.iloc[0]['keyword']
                description_field.value = df.iloc[0]['description']
                csv_content.value = df.to_string(index=False)
            else:
                csv_content.value = "CSV file is empty!"
        else:
            csv_content.value = "Cancelled!"
        title_field.update()
        keyword_field.update()
        description_field.update()
        csv_content.update()

    upload_csv_dialog = FilePicker(
        on_result=upload_csv_result,
        
    )

    # UI setup
    page.add(
        ElevatedButton(
            "Open Directory",
            icon=icons.FOLDER_OPEN,
            on_click=lambda _: get_directory_dialog.get_directory_path(),
            disabled=page.web,
        ),
        directory_path,
        ElevatedButton(
            "Upload CSV",
            icon=icons.UPLOAD_FILE,
            on_click=lambda _: upload_csv_dialog.pick_files(allow_multiple=False),
        ),
        csv_content,
        title_field,
        keyword_field,
        description_field,
        image_container
    )

    # Overlay file picker
    page.overlay.append([get_directory_dialog, upload_csv_dialog])

# Run the app
flet.app(target=main)
