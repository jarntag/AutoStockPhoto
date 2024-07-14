import flet
from flet import (
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    Page,
    Row,
    Text,
    Image,
    IconButton,
    Icon,
    icons,
    FilePickerFileType,
    AppBar,
    PopupMenuButton,
    colors,
    PopupMenuItem,
    Column,
    MainAxisAlignment,
    CrossAxisAlignment,
    TextField,
    border_radius,
    ImageFit,
    Chip,
    GridView,
)
import pandas as pd
import os
import exiftool

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

    page.title = "Image List from Directory"
    page.window_width = 800
    page.window_height = 1000

    # Text widget to display the selected directory path
    directory_path = Text()
    csv_file_path = TextField(label="CSV File Path",width=400)

    # TextField widgets to display CSV data
    title_field = TextField(label="Title")
    keyword_field = TextField(label="Keywords")
    description_field = TextField(label="Description")


    # Container to hold image components
    image_container = GridView(height=400,
        width=800,
        runs_count=5,
        max_extent=150,
        child_aspect_ratio=1.0,
        spacing=5,
        padding=5,
        )
    
    # Container to hold image components
    csv_data_container = Column()


    # Function to list and display images in a directory
    def list_images(directory):
        image_container.controls.clear()  # Clear previous images
        for filename in os.listdir(directory):
            if filename.lower().endswith(('.jpg', '.png', '.svg')):
                image_path = os.path.join(directory, filename)
                image_component = Row([
                    Image(src=image_path, width=150, height=150,
                        border_radius=border_radius.all(10),tooltip=filename,fit=ImageFit.COVER),
                ])
                image_container.controls.append(image_component)
        
                      
                
        page.update()


    # Pick files dialog
    def pick_files_result(e: FilePickerResultEvent):
        
        csv_file_path.value = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else "Cancelled!"
        )
        csv_file_path.update()

    pick_files_dialog = FilePicker(on_result=pick_files_result)
    selected_files = Text()

    # Save file dialog
    def save_file_result(e: FilePickerResultEvent):
        save_file_path.value = e.path if e.path else "Cancelled!"
        save_file_path.update()

    save_file_dialog = FilePicker(on_result=save_file_result)
    save_file_path = Text()

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
    page.overlay.extend([pick_files_dialog, save_file_dialog, get_directory_dialog])

    
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
        
        # Open directory
        Row(
            [
                ElevatedButton(
                    "Open directory",
                    icon=icons.FOLDER_OPEN,
                    on_click=lambda _: get_directory_dialog.get_directory_path(),
                    disabled=page.web,
                ),
                directory_path,
                
            ]
        ),
        Text(value="Title : "),
        Text(value="Keywords : "),
        image_container,
        
        Row(
            [  
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
            ]
        ),
        Row([csv_file_path, ElevatedButton("Load csv data", on_click=read_csv)]),

        csv_data_container,
        
        Row(
            [
                ElevatedButton(
                    "Save file",
                    icon=icons.SAVE,
                    on_click=lambda _: save_file_dialog.save_file(file_name="metadata",
                    initial_directory="uploads",file_type=FilePickerFileType.CUSTOM,
                    allowed_extensions=["csv"]),
                    disabled=page.web,
                    
                ),
                save_file_path,
            ]
        ),
        
    )

# Run the app
flet.app(target=main)