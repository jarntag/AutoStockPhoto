import flet as ft
import pandas as pd
import os

# Path to save the CSV file
save_path = 'save/sample_images.csv'
# Sample data to be added
data = [
    {
        "Filename": "image1.jpg",
        "Title": "Beautiful Sunset",
        "Keywords": "sunset, nature, beauty",
        "Category": "Nature",
        "Releases": "2024-07-18"
    },

]

adobe_categories = [
    "Animals",
    "Buildings and Architecture",
    "Business",
    "Drinks",
    "The Environment",
    "States of Mind",
    "Food",
    "Graphic Resources",
    "Hobbies and Leisure",
    "Industry",
    "Landscape",
    "Lifestyle",
    "People",
    "Plants and Flowers",
    "Culture and Religion",
    "Science",
    "Social Issues",
    "Sports",
    "Technology",
    "Transport",
    "Travel"
]

# Container to hold image components

image_grid = ft.ListView( 

    spacing=10,
)
image_data = ""
image_container = ft.ListView( 

    spacing=10,
)
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
directory_path = ft.Text("Select images directory path first!")
images_per_prompt = ft.TextField(
    label="images per prompt", 
    value="4",
)
prefix_prompt = ft.TextField(
    label="Prefix prompt",
    value="",
    min_lines=1,max_lines=2,
    multiline=True,
    color=ft.colors.BLUE_700,
)
main_prompt = ft.TextField(
    label="Main prompt matrix List", 
    value="",
    min_lines=1,
    max_lines=5, 
    multiline=True,
    color=ft.colors.BLUE_700,
)

enhance_prompt = ft.TextField(
    label="Enhance prompt matrix List", 
    value="",
    min_lines=1,
    max_lines=2, 
    multiline=True,
    color=ft.colors.BLUE_700,
)
subfix_prompt = ft.TextField(
    label="Subfix prompt", 
    value=", ultra realistic, candid, social media, avatar image, plain solid background",
    min_lines=1,
    max_lines=2, 
    multiline=True,
    color=ft.colors.BLUE_700,
)
main_keywords = ft.TextField(
    label="Keywords", 
    value="line1\nline2",
    min_lines=2,
    max_lines=5, 
    multiline=True,
    color=ft.colors.BLUE_700,
)

csv_file_path = ft.TextField(label="CSV File Path"
)

image_title = ft.TextField(label="Title")
image_metadata = ft.Text("Metadata")
image_keywords = ft.TextField(
    label="Keywords", 
    value="",
    min_lines=2,
    max_lines=3, 
    multiline=True,
    color=ft.colors.BLUE_700,
)
categories_select=ft.Dropdown(
    on_change=print(),
    options=[
        ft.dropdown.Option("Red"),
        ft.dropdown.Option("Green"),
        ft.dropdown.Option("Blue"),
    ],
    width=200,
)

progress_bar = ft.ProgressBar(
    value=0,
    bar_height=1,)
csv_data_container = ft.Column()


main_prompt_list = ['Africa', 'Algeria', 'Angola', 'Benin',]
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
categories_main=ft.Dropdown(
        width=64,
        value=1,
        options=[
            ft.dropdown.Option("1"),
            ft.dropdown.Option("2"),
            ft.dropdown.Option("3"),
        ],
    )

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
    df = pd.DataFrame(data)
    df.to_csv(save_path, index=False)
    print(f"CSV file created and saved at {save_path}")



# main function
def main(page: ft.Page):
    page.window_width = 1000
    page.window_height = 1000
    
    def on_change(event):
        print("Selected category:", category_dropdown.value(index))

    #Function \\\\\\\\\\

    def embed_metadata():
        path=directory_path.value
        images = sorted([f for f in os.listdir(path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
        num = int(images_per_prompt.value)
        process_count = 0  # Initialize image count
        selected_index_g=""
        cleaned_string = main_prompt.value.replace("\n", ",").replace(", ", ",").strip(",")
        main_prompt_list = [promptst.strip() for promptst in cleaned_string.split(",") if promptst.strip()]
        total_prompt = len(main_prompt_list)

        keywords_list = main_keywords.value.replace("\n", ", ").replace(", ", ",").split(",")

        all_data = []  # List to store all data

        for i, prompt in enumerate(main_prompt_list):
            start_index = i * num
            end_index = start_index + num
            prompt_images = images[start_index:end_index]

            for j, image_file in enumerate(prompt_images):
                image_path = os.path.join(path, image_file)

                title = f"{prefix_prompt.value} {prompt} {enhance_prompt.value}{subfix_prompt.value}"
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
                    "Category": selected_index+1,
                    "Releases": None,
                }

                all_data.append(data)  # Append new data to the list

                process_count += 1
                image_count_label.value = f"Total process Images: {process_count}"
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

        print(keywords_list)
        image_count_label.value = f"Total process Images: {process_count}"
        image_count_label.update()
    # ... (rest of the code)

    # Create a DataFrame from the data
    df = pd.DataFrame(data) 

    def extract_csv(image_path):
        
        return None, None
            
    # Function to list and display images in a directory
    def list_images(directory):
        image_container.controls.clear()  # Clear previous images
        image_count = 0  # Initialize image count
        card = ft.Card()

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
                card = ft.Card(content=
                    ft.Container(content=
                        ft.Stack([
                            ft.Image(
                                src=image_path,
                                border_radius=ft.border_radius.all(0),
                                tooltip=filename,
                                fit=ft.ImageFit.COVER,
                                width=150,
                                height=150,
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
                    width=150, height=150,
                )
                # Now set the on_click handler
                card.content.content.controls[2].on_click = lambda e, card=card, image_path=image_path, filename=filename: handle_click(e, card, image_path, filename)
                right_con=ft.Column([
                    ft.Dropdown(
                        label="Categories",
                        hint_text="Choose Categories",
                        options=[
                            ft.dropdown.Option("1. Animals"),
                            ft.dropdown.Option("2. Buildings and Architecture"),
                            ft.dropdown.Option("3. Business"),
                            ft.dropdown.Option("4. Drinks"),
                            ft.dropdown.Option("5. The Environment"),
                            ft.dropdown.Option("6. States of Mind"),
                        ],
                    ),
                    ft.CupertinoTextField(
                        placeholder_text="Title",
                    ),
                    ft.CupertinoTextField(
                        placeholder_text="Keywords",
                    ),
                    ft.CupertinoTextField(
                        placeholder_text="Releases",
                    ),
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
        image_count_label.value = f"Total Images: {image_count}"
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
                    processed_data = content.replace("\n", ",")
                    main_prompt.value = processed_data
                    page.update()  # Update the page to reflect the changes
            except Exception as ex:
                print(f"An error occurred while loading the text file: {ex}")
        else:
            print("No file selected")

    get_txt_main = ft.FilePicker(on_result=get_txt_result)


    # Function to read data from CSV
    def read_csv(e):
        df = pd.read_csv(save_path)
        
        # Create table headers
        columns = [ft.DataColumn(ft.Text(col)) for col in df.columns]
        
        # Create table rows
        rows = []
        for _, row in df.iterrows():
            cells = [ft.DataCell(ft.Text(str(cell))) for cell in row]
            rows.append(ft.DataRow(cells))
        
        # Create DataTable and add it to the page
        table = ft.DataTable(columns=columns, rows=rows)
        table_container.controls.clear()
        table_container.controls.append(table)
        page.update()

    # FilePicker dialog to select a directory
    def image_metadata_Process(e):
        title = f"{prefix_prompt.value} {main_prompt.value} {enhance_prompt.value}{subfix_prompt.value}"
        keywords = main_keywords.value.replace("\n", "; ").replace(",", "; ")
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
        global selected_index
        selected_index = int(event.control.value.split(" : ")[0]) - 1  # Adjust to zero-indexed
        selected_category = adobe_categories[selected_index]
        print("Selected category:", selected_category)
        print(f"Selected category: {selected_category} (Index: {selected_index})")

        page.update()  # Ensure the page updates if necessary

        return selected_index

    category_dropdown = ft.Dropdown(
        label="Select Category",
        options=[ft.dropdown.Option(key=f"{index+1} : {category}") for index, category in enumerate(adobe_categories)],
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
                content=ft.Container(
                    content=ft.Column([
                        progress_bar,
                        ft.Row([
                            directory_path,
                            image_count_label, 
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
                    alignment=ft.alignment.top_left
                ),
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
                    ]),
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
                content=ft.Text("Setting"),
            ),
        ],
        expand=True,
        tab_alignment=ft.TabAlignment.FILL,
    )

    # hide all dialogs in overlay
    page.overlay.extend([pick_files_dialog, get_directory_dialog, get_txt_main])


    # UI setup
    page.add(
        tabs_main,
        
        


             
    )

    right_content.controls.append(
        ft.Container(
            content=ft.Column([
                #ft.Text("Images"),  
                ft.Row([check_metadata_bt,open_directory_bt,],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,),
                    
                #ft.Text("Prompt to Title"),
                category_dropdown,
                images_per_prompt,
                prefix_prompt,
                main_prompt,
                ft.Row([mainprompt_bt,],
                    alignment=ft.MainAxisAlignment.END,),
                ft.Row([prompt_to_Keywords,
                        split_prompt_to_Keywords,],
                    alignment=ft.MainAxisAlignment.END,
                ),
                
                enhance_prompt,
                subfix_prompt,
                #ft.Text("Keywords"),
                # Pick csv files
                # Load csv data
                main_keywords,
                ft.Row([ft.ElevatedButton("Test", on_click=image_metadata_Process),embed_metadata_bt, ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,), 

                ft.Divider(),  

                csv_file_path,
                ft.Row([pick_csv_bt, load_csv_bt],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,),
                csv_data_container,

                # Button to save data to CSV
                save_button, read_button, table_container,
                
                ], scroll=ft.ScrollMode.AUTO,alignment=ft.MainAxisAlignment.START),
            #bgcolor=ft.colors.BROWN_400,
            alignment=ft.alignment.top_left,
            expand=True,
        ),
    )
       
    page.update()

ft.app(target=main)