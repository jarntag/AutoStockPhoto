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
    Column,
    icons,
    Icon,
    FilePickerFileType,
    Chip,
)
import pandas as pd
import exiftool
import os

os.environ["FLET_SECRET_KEY"] = os.urandom(12).hex()
secret_key = "1234"

def example():
    async def amenity_selected(e):
        await amenity_chips.update_async()

    title = Row([Icon(icons.HOTEL_CLASS), Text("Amenities")])
    amenities = ["Washer / Dryer", "Ramp access", "Dogs OK", "Cats OK", "Smoke-free"]
    amenity_chips = Row()

    for amenity in amenities:
        amenity_chips.controls.append(
            Chip(
                label=Text(amenity),
                on_select=amenity_selected,
            )
        )
    return Column(controls=[title, amenity_chips])    

def main(page: Page):
    page.title = "Image Metadata Viewer"
    page.window_width = 800
    page.window_height = 600

    # Text widgets to display the selected directory path and CSV file contents
    directory_path = Text()
    csv_file_path = TextField(label="CSV File Path")

    # Container to hold CSV data TextFields
    csv_data_container = Column()

    # Container to hold image components
    image_container = Column()


    


    # Pick files dialog
    def pick_files_result(e: FilePickerResultEvent):
        
        csv_file_path.value = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else "Cancelled!"
        )
        csv_file_path.update()

    pick_files_dialog = FilePicker(on_result=pick_files_result)
    selected_files = Text()
    

    # Function to list and display images in a directory with their metadata
    def list_images(directory):
        image_container.controls.clear()  # Clear previous images
        with exiftool.ExifTool() as et:
            for filename in os.listdir(directory):
                if filename.lower().endswith(('.jpg', '.png', '.svg')):
                    image_path = os.path.join(directory, filename)
                    metadata = et.get_metadata(image_path)
                    image_title = metadata.get("XMP:Title", "No Title")
                    image_keywords = metadata.get("XMP:Keywords", "No Keywords")

                    image_component = Column([
                        Row([
                            Image(src=image_path, width=200, height=200),
                            Column([
                                Text(f"Filename: {filename}"),
                                Text(f"Title: {image_title}"),
                                Text(f"Keywords: {image_keywords}"),
                     
                            ])
                        ])
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
                csv_data_container.controls.clear()
                for idx, row in df.iterrows():
                    keywords_list = row['Keywords'].split(';')
                    keyword_texts = [Chip(label=Text(keyword),on_select=example, selected=True) for i, keyword in enumerate(keywords_list)]
                        
                    csv_data_container.controls.append(
                        Column([
                            Text(f"Row {idx + 1}"),
                            TextField(label="Title", value=row['Title']),
                            Row([*keyword_texts]),
                            TextField(label="Description", value=row['Description']),
                        ])
                    )
                csv_data_container.update()
            else:
                csv_data_container.value = "CSV file is empty!"
        else:
            csv_data_container.value = "Invalid file path!"
        csv_data_container.update()

    # hide all dialogs in overlay
    page.overlay.extend([pick_files_dialog, get_directory_dialog])

    # UI setup
    page.add(
        ElevatedButton(
                    "Pick csv files",
                    icon=icons.UPLOAD_FILE,
                    on_click=lambda _: pick_files_dialog.pick_files(
                        allow_multiple=True,
                    file_type=FilePickerFileType.CUSTOM,
                    allowed_extensions=["csv"]

                        
                    ),
                ),
                selected_files,
        Row([csv_file_path, ElevatedButton("Load CSV", on_click=read_csv)]),
        csv_data_container,
        image_container
    )

    

# Run the app
flet.app(target=main)
