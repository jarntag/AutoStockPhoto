import flet as ft
import pandas as pd
import os
import configparser

class ImageCard(ft.Column):
    def __init__(self, image_path, title, keywords):
        super().__init__(
            spacing=10,
            children=[
                ft.Image(src=image_path, width=100, height=100),
                ft.Text(title, bold=True),
                ft.TextField(value=keywords, label="Keywords"),
            ]
        )

def serialize_image_data(image_data):
    """Convert a list of dictionaries to a serialized string format."""
    return '|'.join([f"{key}:{value}" for key, value in image_data.items()])

def deserialize_image_data(data_str):
    """Convert a serialized string format back to a list of dictionaries."""
    return {item.split(':')[0]: item.split(':')[1] for item in data_str.split('|')}

def convert_to_list(categories_str):
    """Convert a comma-separated string to a list."""
    return [item.strip() for item in categories_str.split(',')]

def convert_to_string(categories_list):
    """Convert a list to a comma-separated string."""
    return ', '.join(categories_list)

# Load configuration data
config = configparser.ConfigParser()
config.read('config.ini')

# Access data from the DEFAULT section
app_theme = config['USER'].get('Theme', 'LIGHT')
save_path = config['USER'].get('SavePath', 'default/path')
images_per_prompt = config['USER'].get('ImagesPerPrompt', '2')
prefix_prompt = config['USER'].get('PrefixPrompt', '')
main_prompt = config['USER'].get('MainPrompt', '')
suffix_prompt = config['USER'].get('suffixPrompt', '')
main_keywords = config['USER'].get('MainKeywords', '')
default_categories = config['USER'].get('SelectCategories', '')
adobe_categories_str = config['USER'].get('AdobeCategories', '')
adobe_categories_list = convert_to_list(adobe_categories_str)
image_data_str = config['USER'].get('ImageData', '')
image_data = deserialize_image_data(image_data_str)


selected_index = int(default_categories)

# Container to hold image components

image_grid = ft.ListView(spacing=10,)
image_data = ""
image_container = ft.ListView(spacing=10,)
main_container = ft.Container(
    content=image_container,
    #bgcolor=ft.colors.ORANGE_300,
    alignment=ft.alignment.center,
    width=800,
    expand=True,
)
right_content = ft.Row([],spacing=10,expand=True,
)
right_container = ft.Container(
    content=right_content,
    #bgcolor=ft.colors.BROWN_400,
    alignment=ft.alignment.center,
    width=400,  # Start width, adjusted according to total width
    expand=False,
)

image_count_label = ft.Text(value="")
directory_path = ft.Text("Select images directory path first!", expand=True,)

csv_file_path = ft.TextField(label="CSV File Path"
)

image_title = ft.TextField(label="Title")

image_keywords = ft.TextField(
    label="Keywords", 
    value="",
    min_lines=2,
    max_lines=3, 
    multiline=True,
    color=ft.colors.BLUE_700,
)
image_releases = ft.Text("releases")

progress_bar = ft.ProgressBar(
    value=0,
    bar_height=1,)
csv_data_container = ft.Column()


main_prompt_list = []
keywords_list = []
images_select_list = []

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

prompt_to_Keywords=ft.Chip(label=ft.Text("Promt to Keyword"),on_select=chip_select, selected=False)
split_prompt_to_Keywords=ft.Chip(label=ft.Text("Split Promt"),on_select=chip_select, selected=False)


async def move_vertical_divider(e: ft.DragUpdateEvent):
    new_width = main_container.width + e.delta_x
    if 100 <= new_width <= 900 and 150 <= right_container.width - e.delta_x:
        main_container.width = new_width
        right_container.width -= e.delta_x
        await main_container.update_async()
        await right_container.update_async()

async def show_draggable_cursor(e: ft.HoverEvent):
    e.control.mouse_cursor = ft.MouseCursor.RESIZE_LEFT_RIGHT
    await e.control.update_async()            

# Function to save data to CSV
def save_to_csv(e):
    df = pd.DataFrame(image_data)
    df.to_csv(save_path, index=False)
    print(f"CSV file created and saved at {save_path}")



# main function
def main(page: ft.Page):
    page.title = "AutoStockPhoto"
    # Initial theme mode
    
    ft.Page.window_width = 1000
    ft.Page.window_height = 1000
    
    global theme_switch, save_path_field, images_per_prompt_field, prefix_prompt_field
    global main_prompt_field, suffix_prompt_field, main_keywords_field
    global adobe_categories_field

    def on_click(e, click_message):
        page.snack_bar = ft.SnackBar(ft.Text(click_message))
        page.snack_bar.open = True
        
        #page.overlay.append(ft.SnackBar(ft.Text(click_message)))
        page.update()

    # Function to save user data
    def save_user_data(e, click_message):
        config['USER'] = {
            'Theme': ("LIGHT" if page.theme_mode == ft.ThemeMode.LIGHT else "DARK"),
            'SavePath': save_path,
            'ImagesPerPrompt': images_per_prompt_field.value,
            'PrefixPrompt': prefix_prompt_field.value,
            'MainPrompt': main_prompt_field.value,
            'suffixPrompt': suffix_prompt_field.value,
            'MainKeywords': main_keywords_field.value,
            'SelectCategories': selected_index,
            'AdobeCategories': convert_to_string([adobe_categories_field.value]),
            'ImageData': image_data_str,
        }

        with open('config.ini', 'w') as configfile:
            config.write(configfile)
            
        on_click(e, click_message)
        
    # Function to be called on app close
    def on_close(event):
        print("App is closing...")
        save_user_data()

    # Create TextFields for each config item
    

    save_path_field = ft.TextField(label="Save Path", 
                                    value=save_path,
                                    prefix_icon=ft.icons.FOLDER_OPEN,
                                    hint_text="Type your save path",
                                    color=ft.colors.BLUE_700,
                                    )
    images_per_prompt_field = ft.TextField(label="image per prompt", 
                                            value=images_per_prompt,
                                            prefix_icon=ft.icons.BURST_MODE,
                                            color=ft.colors.BLUE_700,
                                            
                                            )
    prefix_prompt_field = ft.TextField(label="Prefix Prompt", 
                                        value=prefix_prompt,
                                        color=ft.colors.BLUE_700,
                                        prefix_icon=ft.icons.TEXT_FIELDS,
                                        counter_text="Title = prefix + main + suffix prompt",)
    main_prompt_field = ft.TextField(label="Main prompt matrix List", 
                                    value=main_prompt,
                                    min_lines=1,
                                    max_lines=5, 
                                    multiline=True,
                                    color=ft.colors.BLUE_700,
                                    prefix_icon=ft.icons.TEXT_FIELDS,
                                    counter_text="Separate each prompt with , or new line",)
    suffix_prompt_field = ft.TextField(label="suffix Prompt", 
                                        value=suffix_prompt,
                                        color=ft.colors.BLUE_700,
                                        prefix_icon=ft.icons.TEXT_FIELDS,
                                        counter_text="0 totle Title symbols typed",)
    main_keywords_field = ft.TextField(label="Main Keywords", 
                                        value=main_keywords,
                                        min_lines=1,
                                        max_lines=5, 
                                        multiline=True,
                                        color=ft.colors.BLUE_700,
                                        prefix_icon=ft.icons.SELL,
                                        helper_text="Separate each keywords with , or new line",
                                        counter_text="0 keywords",)
    adobe_categories_field = ft.TextField(label="Adobe Categories", value=adobe_categories_str)


    # Create Save Button
    save_button_config = ft.ElevatedButton(text="Save", on_click=lambda e: save_user_data(e, "Data saved successfully!"))

    def toggle_theme(e):
        page.theme_mode = (ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT)
        theme_switch.label = (" Light Theme : " if page.theme_mode == ft.ThemeMode.LIGHT else " Dark Theme : ")
        theme_icon.name = (ft.icons.LIGHT_MODE if page.theme_mode == ft.ThemeMode.LIGHT else ft.icons.DARK_MODE)
        page.update()
    
    if app_theme.upper() == 'LIGHT':
        page.theme_mode = ft.ThemeMode.LIGHT
    elif app_theme.upper() == 'DARK':
        page.theme_mode = ft.ThemeMode.DARK

    theme_switch = ft.Switch(label=(" Light theme : " if page.theme_mode == ft.ThemeMode.LIGHT else " Dark theme : "), 
                            value=(True if page.theme_mode == ft.ThemeMode.LIGHT else False),
                            label_position=ft.LabelPosition.LEFT,
                            on_change=toggle_theme)
    theme_icon = ft.Icon(name=(ft.icons.LIGHT_MODE if page.theme_mode == ft.ThemeMode.LIGHT else ft.icons.DARK_MODE),
                         )
    #Function \\\\\\\\\\

    def embed_metadata():
        path=directory_path.value
        images = sorted([f for f in os.listdir(path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
        num = int(images_per_prompt_field.value)
        process_count = 0  # Initialize image count

        main_prompt_list = [line.strip() for line in main_prompt_field.value.strip().split('\n') if line.strip()]
        total_prompt = len(main_prompt_list)

        keywords_list = main_keywords_field.value.replace("\n", ", ").replace(", ", ",").split(",")

        all_data = []  # List to store all data

        for i, prompt in enumerate(main_prompt_list):
            start_index = i * num
            end_index = start_index + num
            prompt_images = images[start_index:end_index]

            for j, image_file in enumerate(prompt_images):
                image_path = os.path.join(path, image_file)

                title = f"{prefix_prompt_field.value} {prompt} {suffix_prompt_field.value}"
                prompt=prompt.replace("\n", " ").replace("'", "")

                # Prepare prompt key
                prompt_words = [word.rstrip('.,!?') for word in prompt.lower().split() if len(word) > 2]

                # Initialize seen set with the correct syntax
                seen = {'the', 'out', 'up', 'with'}
                seen.update(keywords_list)
                unique_words = []

                for word in prompt_words:
                    if word not in seen:
                        unique_words.append(word)
                        seen.add(word)
                prompt_keyp = ', '.join(unique_words)

                keywords = f"{prompt_keyp}, {', '.join(keywords_list)},".rstrip(', ')

                data = {
                    "Filename": image_file,
                    "Title": title,
                    "Keywords": keywords,
                    "Category": selected_index,
                    "Releases": None,
                }

                all_data.append(data)  # Append new data to the list

                process_count += 1
                image_count_label.value = f"Total process Images : {process_count}"
                image_count_label.update()
                
                progress_bar.value = process_count/(total_prompt*num)
                progress_bar.update()
                print(keywords)   

        # Extract folder name from directory path
        folder_name = os.path.basename(os.path.normpath(path))

        # Save all data to CSV file with folder name as the file name
        csv_file_path = os.path.join(path, f"{folder_name}.csv")
        df = pd.DataFrame(all_data)
        df.to_csv(csv_file_path, index=False)
        print(f"CSV file saved in folder: {csv_file_path}")

        print(main_prompt_list,len(main_prompt_list))
        image_count_label.value = f"Total process Images : {process_count}"
        image_count_label.update()
    # ... (rest of the code)

    # Create a DataFrame from the data
    df = pd.DataFrame([image_data]) 

    def extract_csv(image_path):
        
        return None, None
    
    # Function to read CSV and return metadata
    def read_csv(directory):
        # Extract folder name from directory path
        folder_name = os.path.basename(os.path.normpath(directory))
        # Save all data to CSV file with folder name as the file name
        csv_file_path = os.path.join(directory, f"{folder_name}.csv")
        try:
            df = pd.read_csv(csv_file_path)
            metadata_list = df.to_dict(orient='records')
            return metadata_list
        except FileNotFoundError:
            print(f"File '{csv_file_path}' not found. Creating a new file.")
            # Create a new empty DataFrame with specified columns and save it as a CSV file
            all_data = []  # List to store all data
            images = sorted([f for f in os.listdir(directory) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
            for image in images:
                data = {
                    "Filename": image,
                    "Title": "",
                    "Keywords": "",
                    "Category": 0,
                    "Releases": "",
                }
                all_data.append(data)  # Append new data to the list
            df = pd.DataFrame(all_data)
            df.to_csv(csv_file_path, index=False)
            df = pd.read_csv(csv_file_path)
            metadata_list = df.to_dict(orient='records')
            return metadata_list
            
    # Function to list and display images in a directory
    def list_images(directory):
        image_container.controls.clear()  # Clear previous images
        image_count = 0  # Initialize image count
        card = ft.Card()
        metadata = read_csv(directory)
        
        def change_color(e, card, filename):
            if card.color == ft.colors.BLUE:
                card.color = ft.colors.GREY_50
                if filename in images_select_list:
                    images_select_list.remove(filename)
                    print(images_select_list)
            elif card.color == ft.colors.GREY_50:
                card.color = ft.colors.BLUE
                if filename not in images_select_list:
                    images_select_list.append(filename)
                    print(images_select_list)
            page.update()

        def handle_click(e, card, image_path, filename):
            extract_csv(image_path)
            change_color(e, card, filename)

        for filename in os.listdir(directory):
            if filename.lower().endswith(('.jpg', '.png', '.svg')):
                image_path = os.path.join(directory, filename)
                image_container.controls.append(ft.Text(f"filename : {filename}",),)
                image_metadata = next((item for item in metadata if item['Filename'] == filename), {})

                card = ft.Card(content=
                    ft.Container(content=
                        ft.Stack([
                            ft.Image(
                                src=image_path,
                                border_radius=ft.border_radius.all(0),
                                tooltip=filename,
                                fit=ft.ImageFit.COVER,
                                width=100,
                                height=100,
                            ),
                            ft.Container(content=
                                ft.Container(content=         
                                    ft.Row([
                                        ft.Row([
                                            ft.Icon(name=ft.icons.SELL, size=12),
                                            ft.Text(value="10", size=10,),
                                        ],alignment=ft.MainAxisAlignment.START,
                                        ),    
                                        ft.CircleAvatar(bgcolor=ft.colors.GREY, radius=4),
                                    ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    ),bgcolor=ft.colors.GREY_50,opacity=0.5,height=24,
                                    alignment=ft.alignment.bottom_right,margin=0,padding=5,
                                ),
                                alignment=ft.alignment.bottom_center,margin=0,
                            ),
                            ft.Container(
                                alignment=ft.alignment.bottom_right,margin=0,
                                ink=True,padding=ft.padding.only(0),
                                on_click=None,  # Set to None initially
                            ),   
                        ]),margin=3,
                    ),shape=ft.RoundedRectangleBorder(radius=0),
                    margin=0,color = ft.colors.GREY_50,
                    width=100, height=100,
                )
                # Now set the on_click handler
                card.content.content.controls[2].on_click = lambda e, card=card, image_path=image_path, filename=filename: handle_click(e, card, image_path, filename)
                
                category = image_metadata.get('Category')

                if category is not None and category > 0:
                    image_category = adobe_categories_list[int(category) - 1]
                else:
                    image_category = "Selected Category"
                                    
                print(image_metadata)
                    

                right_con=ft.Column([
                    
                    ft.Dropdown(
                        label=None,
                        options=[ft.dropdown.Option(key=f"{index+1} : {category}") for index, category in enumerate(adobe_categories_list)],
                        hint_text=f"{image_metadata.get('Category', '')} : {image_category}",
                        on_change=on_change_category_dropdown
                    ),
                   
                    ft.TextField(label=(f"{image_metadata.get('Title', '')}")),
                    ft.TextField(
                        label="Keywords", 
                        value=(f"{image_metadata.get('Keywords', '')}"),
                        min_lines=2,
                        max_lines=3, 
                        multiline=True,
                        color=ft.colors.BLUE_700,
                    ),
                    ft.Text((f"Releases : {image_metadata.get('Releases', '')}")),

                        ],
                        expand=True,
                    )
                row_con=ft.Row([
                    card,
                    right_con,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True,
                )

                image_container.controls.append(row_con)
                image_container.controls.append(ft.Divider(height=9,),)
                image_count += 1  # Increment image count
        
        # Update the label with the image count
        image_count_label.value = f"Total Images : {image_count} | "
        page.update()
        return card
    
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

    # FilePicker dialog to select and read txt
    def get_txt_result(e: ft.FilePickerResultEvent):
        if e.files:
            file_path = e.files[0].path
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                    processed_data = content
                    main_prompt_field.value = processed_data
                    page.update()  # Update the page to reflect the changes
            except Exception as ex:
                print(f"An error occurred while loading the text file: {ex}")
        else:
            print("No file selected")

    get_txt_main = ft.FilePicker(on_result=get_txt_result)


    # FilePicker dialog to select a directory
    def image_metadata_Process(e):
        title = f"{prefix_prompt_field.value} {main_prompt_field.value} {suffix_prompt_field.value}"
        keywords = main_keywords_field.value.replace("\n", "; ").replace(",", "; ")
        image_title.value = f"{title}"
        image_keywords.value = f"{keywords}"

        image_title.update()
        image_keywords.update()
        print(image_title.value,image_keywords.value)
        return title,keywords

    def images_select(filename):
        if filename in images_select_list:
            images_select_list.remove(filename)
            print(f"Removed {filename} from images_select_list")
        else:
            images_select_list.append(filename)
            print(f"Added {filename} to images_select_list")

        print(images_select_list)
        return images_select_list
    
    def Check_metadata(image_path):
        with exiftool.ExifToolHelper() as et:
            metadata = et.get_metadata(image_path)[0]
            title = metadata.get('XMP:Title', '')
            color = ft.colors.RED if not title else ft.colors.RED

        print(images_select_list)
        return color
    

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
            allowed_extensions=["csv"]
        ),
    )

    embed_metadata_bt=ft.ElevatedButton("embed metadata",
        icon=ft.icons.DATA_OBJECT,
        on_click=lambda _: embed_metadata(),
    )

    mainprompt_bt=ft.ElevatedButton("Load Prompt txt data",
        icon=ft.icons.UPLOAD_FILE,
        on_click=lambda _: get_txt_main.pick_files(
            allow_multiple=True,
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["txt"]
        ),
    )
    
    check_metadata_bt=ft.ElevatedButton("check metadata",
        icon=ft.icons.PLAYLIST_ADD_CHECK_CIRCLE_OUTLINED,
        on_click=lambda _: embed_metadata(),
    )

    load_csv_bt=ft.ElevatedButton("Load csv data", on_click=read_csv)

    save_button = ft.OutlinedButton(text="Save to CSV", on_click=save_to_csv)

    # Button to read data from CSV
    read_button = ft.OutlinedButton(text="Read from CSV", on_click=read_csv)

    # Create dropdown menu for categories
    def on_change_category_dropdown(event):
        category = event.control.value
        global selected_index
        selected_index = adobe_categories_list.index(category)+1  # Adjust to zero-indexed
        event.control.label="Selected Category"
        print(f"Selected category: {category} (Index: {selected_index})")
        
        page.update()  # Ensure the page updates if necessary

        return selected_index

    category_dropdown = ft.Dropdown(
        label=(f"{adobe_categories_list[int(selected_index-1)]}" if selected_index is not None and selected_index > 0 else "Selected Category"),

        options=[ft.dropdown.Option(key=f"{category}") for index, category in enumerate(adobe_categories_list)],
        on_change=on_change_category_dropdown,
    )

    image_categories_dropdown = ft.Dropdown(
        label=None,
        options=[ft.dropdown.Option(key=f"{index+1} : {category}") for index, category in enumerate(adobe_categories_list)],
        on_change=on_change_category_dropdown
    )

     # Container to hold the table
    table_container = ft.Column()

    tabs_main = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        
        tabs=[
            ft.Tab(
                text="Images Massive Metadata",
                icon=ft.icons.DATASET_OUTLINED,
                
                    content=ft.Column([
                        progress_bar,
                        ft.Row([
                            directory_path,
                            image_count_label,
                            open_directory_bt,
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        
                        ft.Row([
                            ft.ResponsiveRow([
                                ft.Row(controls=[
                                main_container,
                                ft.GestureDetector(content=
                                    ft.VerticalDivider(),
                                    drag_interval=10,
                                    on_pan_update=move_vertical_divider,
                                    on_hover=show_draggable_cursor,
                                ),
                                right_container,
                                ],
                                spacing=0,
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ) ],
                                spacing=10,
                                expand=True,
                            )],
                            spacing=10,
                            expand=True,
                        ),
                        #image_metadata,             
                        #image_title,
                        #image_keywords,
                        ft.Row([]),   
                    ]),
                    
            ),
            ft.Tab(
                text="Images Edit",
                icon=ft.icons.IMAGE_SEARCH,
                content=ft.Container(
                    content=ft.Column([
                        progress_bar,
                        ft.Row([
                            #directory_path,
                            #image_count_label, 
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        
                        ft.Row([
                            ft.ResponsiveRow([
                                ft.Row(controls=[
                                #main_container,
                                ft.GestureDetector(content=
                                    ft.VerticalDivider(),
                                    drag_interval=10,
                                    on_pan_update=move_vertical_divider,
                                    on_hover=show_draggable_cursor,
                                ),
                                #right_container,
                                ],
                                spacing=0,
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ) ],
                                spacing=10,
                                expand=True,
                            )],
                            spacing=10,
                            expand=True,
                        ),
                    ],),
                )
            ),
            ft.Tab(
                text="Re-Upload batch",
                icon=ft.icons.BATCH_PREDICTION,
                content=ft.Text("Re-Upload batch"),
            ),
            ft.Tab(
                text="Setting",
                icon=ft.icons.SETTINGS,
                content=ft.Container(
                    content=ft.Column([
                        progress_bar,
                        ft.Text("Configuration"),
                        ft.Row([theme_icon, theme_switch, ]),
                        
                        ft.Row([category_dropdown]),
                        ft.Row([images_per_prompt_field]),
                        ft.Row([prefix_prompt_field]),
                        ft.Row([main_prompt_field]),
                        ft.Row([suffix_prompt_field]),
                        ft.Row([main_keywords_field]),
                        ft.Row([save_path_field]),
                        ft.Row([adobe_categories_field]),

                        save_button_config
                        

                        ],
                        scroll=ft.ScrollMode.AUTO,alignment=ft.MainAxisAlignment.START,
                        expand=True,
                    )
                ),
            ),
        ],
        expand=True,
        tab_alignment=ft.TabAlignment.FILL,
    )

    # hide all dialogs in overlay
    page.overlay.extend([pick_files_dialog, get_directory_dialog, get_txt_main])
    
    # Register on_close handler
    page.on_close = on_close

    # UI setup
    page.add(
        tabs_main,
        
        


             
    )

    right_content.controls.append(
        ft.Container(
            content=ft.Column([
                ft.Row([category_dropdown,images_per_prompt_field,],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    wrap=True,), 
                prefix_prompt_field,
                main_prompt_field,
                ft.Row([mainprompt_bt,],
                    alignment=ft.MainAxisAlignment.END,),
                suffix_prompt_field,
                #ft.Text("Keywords"),
                # Pick csv files
                # Load csv data
                main_keywords_field,
                ft.Row([ft.ElevatedButton("Test", on_click=image_metadata_Process),embed_metadata_bt, ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,), 

                ft.Divider(),  
                ft.Row([prompt_to_Keywords,
                    split_prompt_to_Keywords,],
                    alignment=ft.MainAxisAlignment.END,
                ),
                csv_file_path,
                ft.Row([pick_csv_bt, load_csv_bt],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,),
                csv_data_container,

                # Button to save data to CSV
                save_button, read_button, table_container, check_metadata_bt,
                
                ], scroll=ft.ScrollMode.AUTO,alignment=ft.MainAxisAlignment.START),
            #bgcolor=ft.colors.BROWN_400,
            alignment=ft.alignment.top_left,
            expand=True,
        ),
    )
       
    page.update()
    

    

ft.app(target=main)