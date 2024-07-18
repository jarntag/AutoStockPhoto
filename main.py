import flet as ft
import pandas as pd

import exiftool
import os

# Container to hold image components


image_container = ft.GridView( 
    runs_count=5, 
    max_extent=150,
    child_aspect_ratio=1.0, 
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

progress_bar = ft.ProgressBar(value=0)
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
split_num=ft.Dropdown(
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

# main function
def main(page: ft.Page):
    page.window_width = 1000
    page.window_height = 1000
    
    
    #Function \\\\\\\\\\

    def embed_metadata():
        path=directory_path.value
        images = sorted([f for f in os.listdir(path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
        num = int(images_per_prompt.value)
        process_count = 0  # Initialize image count

        cleaned_string = main_prompt.value.replace("\n", ",").replace(", ", ",").strip(",")
        main_prompt_list = [promptst.strip() for promptst in cleaned_string.split(",") if promptst.strip()]
        total_prompt = len(main_prompt_list)

        keywords_list = main_keywords.value.replace("\n", "; ").replace(",", "; ").split("; ")

        for i, prompt in enumerate(main_prompt_list):
            start_index = i * num
            end_index = start_index + num
            prompt_images = images[start_index:end_index]

            for j, image_file in enumerate(prompt_images):
                image_path = os.path.join(path, image_file)
                prompt=prompt.replace("\n", " ").replace("'", "")
                title = f"{prefix_prompt.value} {prompt} {enhance_prompt.value}{subfix_prompt.value}"

                # Prepare prompt key
                prompt_words = [word.rstrip('.,!?') for word in prompt.lower().split() if len(word) > 2]
                unique_words = []
                seen = set()
                for word in prompt_words:
                    if word not in seen:
                        unique_words.append(word)
                        seen.add(word)
                prompt_keyp = ', '.join(unique_words)

                keywords = f"{prompt}; {enhance_prompt.value}; {'; '.join(keywords_list)};"


                with exiftool.ExifToolHelper() as et:
                    et.execute("-overwrite_original", 
                           f"-XMP:Title={title}", 
                           f"-XMP:Subject={keywords}", 
                           image_path)
                    process_count += 1
                    image_count_label.value = f"Total process Images: {process_count}"
                    image_count_label.update()
                    
                    progress_bar.value = process_count/(total_prompt*num)
                    progress_bar.update()
                    print(keywords)    
        print(keywords_list)
        image_count_label.value = f"Total process Images: {process_count}"
        image_count_label.update()
    # ... (rest of the code)
    
    def extract_metadata(image_path):
        with exiftool.ExifToolHelper() as et:
            metadata = et.get_metadata(image_path)

            # Extract title and keywords
            if metadata:
            # Assuming the first element contains image metadata
                metadata = metadata[0]

                title = metadata.get('XMP:Title', '')
                keywords = metadata.get('XMP:Subject', '')
                image_title.value = f"{title}"
                image_keywords.value = f"{keywords}"

                image_title.update()
                image_keywords.update()

                return title, keywords
            else:
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
            extract_metadata(image_path)
            change_color(e, card, filename)

        for filename in os.listdir(directory):
            if filename.lower().endswith(('.jpg', '.png', '.svg')):
                image_path = os.path.join(directory, filename)
                
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
                    ),shape=ft.RoundedRectangleBorder(radius=0),margin=0,color = ft.colors.GREY_50
                )
                # Now set the on_click handler
                card.content.content.controls[2].on_click = lambda e, card=card, image_path=image_path, filename=filename: handle_click(e, card, image_path, filename)

                image_container.controls.append(card)
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
                    main_prompt.value = content
                    page.update()  # Update the page to reflect the changes
            except Exception as ex:
                print(f"An error occurred while loading the text file: {ex}")
        else:
            print("No file selected")

    get_txt_main = ft.FilePicker(on_result=get_txt_result)

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
                            ft.TextField(label="Filename", value=row['Filename']),
                            ft.TextField(label="Title", value=row['Title']),
                            ft.Row([*keyword_texts]),
                            ft.TextField(label="Category", value=row['Category']),
                            ft.TextField(label="Releases", value=row['Releases']),
                        ])
                    )
                csv_data_container.update()
            else:
                csv_data_container.value = "CSV file is empty!"
        else:
            csv_data_container.value = "Invalid file path!"
        csv_data_container.update()

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


    # hide all dialogs in overlay
    page.overlay.extend([pick_files_dialog, get_directory_dialog, get_txt_main])


    # UI setup
    page.add(
        ft.Row([
            directory_path,
            image_count_label, 
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        progress_bar,
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
            ), 
        ],
        spacing=10,
        expand=True,
        ), 


        image_metadata,             
        image_title,
        image_keywords,
        ft.Row([]),        
    )

    right_content.controls.append(
        ft.Container(
            content=ft.Column([
                #ft.Text("Images"),  
                ft.Row([check_metadata_bt,open_directory_bt,],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,),
                    
                #ft.Text("Prompt to Title"),
                images_per_prompt,
                prefix_prompt,
                main_prompt,
                ft.Row([mainprompt_bt,],
                    alignment=ft.MainAxisAlignment.END,),
                ft.Row([prompt_to_Keywords,
                        split_prompt_to_Keywords,
                        split_num,
                        ],
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

                ft.Divider(),  

                csv_file_path,
                ft.Row([pick_csv_bt, load_csv_bt],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,),
                csv_data_container,
                
                ], scroll=ft.ScrollMode.AUTO,alignment=ft.MainAxisAlignment.START),
            #bgcolor=ft.colors.BROWN_400,
            alignment=ft.alignment.top_left,
            expand=True,
        ),
    )
       
    page.update()

ft.app(target=main)