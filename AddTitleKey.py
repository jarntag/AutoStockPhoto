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
    border_radius,
    ImageFit,
)
import pandas as pd
import exiftool
import os
import subprocess

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


    # Processes images in batches based on regions, adding metadata.
    """Args:
    directory_path: The directory containing images.
    regions: A list of region strings.
    age: The age string.
    disc_string: The base description string.
    keywords_list: A list of keywords."""

    def process_images(directory_path, regions, age, disc_string, keywords_list):

        images = sorted([f for f in os.listdir(directory_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
        num_images_per_region = 4

        for i, region in enumerate(regions):
            start_index = i * num_images_per_region
            end_index = start_index + num_images_per_region
            region_images = images[start_index:end_index]

            for j, image_file in enumerate(region_images):
                image_path = os.path.join(directory_path, image_file)
                title = f"{disc_string} {region} {age}, ultra realistic, candid, social media, avatar image, plain solid background"
                keywords = f"{region}; {age}; {'; '.join(keywords_list)}"
                metadata = {'Title': title, 'XMP:Subject': keywords}
                add_metadata_to_image(image_path, metadata)
                print(title) 

    # Adds title and keywords to an image using exiftool.
    """Args:
    image_path: Path to the image file.
    metadata: A dictionary containing title and keywords."""
    def add_metadata_to_image(image_path, metadata):
        try:
            command = ['exiftool', '-overwrite_original']
            for field, value in metadata.items():
                command.extend([f'-{field}={value}'])
                command.append(image_path)
                subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error processing {image_path}: {e}")


    regions = [
        # Africa
        'Africa', 'Algeria', 'Angola', 'Benin', 'Botswana', 'Burkina Faso', 'Burundi', 'Cabo Verde', 'Cameroon',
        'Central African Republic', 'Chad', 'Comoros', 'Congo', 'Democratic Republic of the Congo', 'Republic of the Congo',
        'Côte d Ivoire', 'Djibouti', 'Egypt', 'Equatorial Guinea', 'Eritrea', 'Eswatini', 'Ethiopia', 'Gabon', 'Gambia',
        'Ghana', 'Guinea', 'Guinea-Bissau', 'Kenya', 'Lesotho', 'Liberia', 'Libya', 'Madagascar', 'Malawi', 'Mali',
        'Mauritania', 'Mauritius', 'Morocco', 'Mozambique', 'Namibia', 'Niger', 'Nigeria', 'Rwanda', 'São Tomé and Príncipe',
        'Senegal', 'Seychelles', 'Sierra Leone', 'Somalia', 'South Africa', 'South Sudan', 'Sudan', 'Tanzania', 'Togo',
        'Tunisia', 'Uganda', 'Zambia', 'Zimbabwe',

        # Asia
        'Asia', 'Afghanistan', 'Armenia', 'Azerbaijan', 'Bahrain', 'Bangladesh', 'Bhutan', 'Brunei', 'Cambodia', 'China',
        'Cyprus', 'East Timor', 'Georgia', 'India', 'Indonesia', 'Iran', 'Iraq', 'Israel', 'Japan', 'Jordan', 'Kazakhstan',
        'North Korea', 'South Korea', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Lebanon', 'Malaysia', 'Maldives', 'Mongolia',
        'Myanmar', 'Nepal', 'Oman', 'Pakistan', 'Palestine', 'Philippines', 'Qatar', 'Russia', 'Saudi Arabia', 'Singapore',
        'Sri Lanka', 'Syria', 'Tajikistan', 'Thailand', 'Turkey', 'Turkmenistan', 'United Arab Emirates', 'Uzbekistan',
        'Vietnam', 'Yemen',

        # Europe
        'Europe', 'Albania', 'Andorra', 'Austria', 'Belarus', 'Belgium', 'Bosnia and Herzegovina', 'Bulgaria', 'Croatia',
        'Cyprus', 'Czech Republic', 'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary', 'Iceland',
        'Ireland', 'Italy', 'Kosovo', 'Latvia', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Malta', 'Moldova', 'Monaco',
        'Montenegro', 'Netherlands', 'North Macedonia', 'Norway', 'Poland', 'Portugal', 'Romania', 'Russia', 'San Marino',
        'Serbia', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'Turkey', 'Ukraine', 'United Kingdom',
        'Vatican City',

        # North America
        'North America', 'Antigua and Barbuda', 'Bahamas', 'Barbados', 'Belize', 'Canada', 'Costa Rica', 'Cuba', 'Dominica',
        'Dominican Republic', 'El Salvador', 'Grenada', 'Guatemala', 'Haiti', 'Honduras', 'Jamaica', 'Mexico', 'Nicaragua',
        'Panama', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'United States',

        # Oceania
        'Oceania', 'Australia', 'Fiji', 'Kiribati', 'Marshall Islands', 'Federated States of Micronesia', 'Nauru',
        'New Zealand', 'Palau', 'Papua New Guinea', 'Samoa', 'Solomon Islands', 'Tonga', 'Tuvalu', 'Vanuatu',

        # South America
        'South America', 'Argentina', 'Bolivia', 'Brazil', 'Chile', 'Colombia', 'Ecuador', 'Guyana', 'Paraguay', 'Peru',
        'Suriname', 'Uruguay', 'Venezuela'
        ]

    age = 'old man'
    disc_string = 'Portrait view of a regular happy smiling'
    keywords_list = ['people', 'person', 'portrait', 'Country', 'region', 'nationality', 'Continent', 'world population', 'age', 'face', 'energetic', 'innocent', 'playful', 'lifestyle', 'authentic', 'model', 'genuine', 'vibrant', 'positive', 'candid', 'carefree', 'one', 'expression', 'joy', 'happiness', 'casual', 'studio', 'smiling', 'smile', 'happy', 'joyful', 'laughing', 'cheerful', 'fun', 'eyes', 'child', 'teenager', 'man', 'male', 'youth', 'handsome', 'cute', 'woman', 'children', 'beauty', 'young', 'childhood']
            

    # Pick files dialog
    def pick_files_result(e: FilePickerResultEvent):
        
        csv_file_path.value = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else "Cancelled!"
        )
        csv_file_path.update()

    pick_files_dialog = FilePicker(on_result=pick_files_result)
    selected_files = Text()
    

    # Function to list and display images in a directory with their metadata
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

    # FilePicker dialog to select a directory
    def get_directory_result(e: FilePickerResultEvent):
        if e.path:
            directory_path.value = e.path
            list_images(e.path)
        else:
            directory_path.value = "Cancelled!"
        directory_path.update()

    get_directory_dialog = FilePicker(on_result=get_directory_result)

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

        ElevatedButton(
                    "process_images",
                    icon=icons.UPLOAD_FILE,
                    on_click=lambda _: process_images(directory_path, 
                        regions, age, disc_string, keywords_list)
                ),
    )

    

# Run the app
flet.app(target=main)
