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

class ImageManager:
    def __init__(self, directory,):
        self.directory = directory
        self.image_data = self.load_image_data()
        self.images_display = images_display

    def load_image_data(self):
        try:
            folder_name = os.path.basename(os.path.normpath(self.directory))
            csv_path = os.path.join(self.directory, f"{folder_name}.csv")
            df = pd.read_csv(csv_path)
            return df.to_dict(orient="records")
        except FileNotFoundError as e:
            print(f"CSV file not found: {e}")
            return self.create_empty_data(self.directory)  # Call the defined function
        except pd.errors.ParserError as e:
            print(f"Error parsing CSV file: {e}")
            return []  # Or handle the error differently
        except Exception as e:
            print(f"Unexpected error while reading CSV: {e}")
            # Handle unexpected errors

    def display_images(directory, images_display):
        # ... create and display image cards
        if images_display == "thumbnail":
            UIBuilder.images_display(main)
            
            print(images_display)
        if images_display == "list":
            print(images_display)
        else : print(images_display)

    def create_empty_data(self, directory):
        # Define logic to create an empty data structure (e.g., empty list or dictionary)
        # This function should return the empty data structure
        return []  # Example: return an empty list

class UIBuilder:
    def __init__(self, processed_data, main_title, prefix_prompt, suffix_prompt, main_keywords,):
        
        self.main_container = ft.Container(
            #bgcolor=ft.colors.ORANGE_300,
            alignment=ft.alignment.top_left,
            width=800,
            expand=True,)
        self.image_container = ft.ListView()

        self.right_container = ft.Container(
            #bgcolor=ft.colors.BROWN_400,
            alignment=ft.alignment.top_left,
            width=400,  # Start width, adjusted according to total width
            expand=False,
        )
        self.right_content = ft.ListView([], spacing=10, expand=True,)
        
        self.processed_data = processed_data
        self.progress_bar = ft.ProgressBar(bar_height=1, value=0,)
        self.directory_path = ft.Text("Select images directory path first!", expand=True,)
        self.image_count_label = ft.Text(value="")
        self.massive_column = ft.Column([])
        self.massive_container = ft.Container(alignment=ft.alignment.top_left, content= self.massive_column)
        self.massive_content = ft.Column()
        
        self.category_dropdown = ft.Dropdown(
            label=(f"{adobe_categories_list[int(categories_index-1)]}" if categories_index is not None and categories_index > 0 else "Selected Category"),
            options=[ft.dropdown.Option(key=f"{category}") for index, category in enumerate(adobe_categories_list)],
            on_change=EventHandler.on_change_category_dropdown,)
        
        self.images_per_prompt_field = ft.TextField(
            label="image per prompt", 
            value=images_per_prompt,
            #prefix_icon=ft.icons.BURST_MODE,
            color=ft.colors.BLUE_700,)
        self.prefix_prompt_field = ft.TextField(
            label="Prefix Prompt", 
            value=prefix_prompt,
            color=ft.colors.BLUE_700,
            #prefix_icon=ft.icons.TEXT_FIELDS,
            #counter_text="Title = prefix + main + suffix prompt",
            on_change= lambda e, : EventHandler.textfield_change(main_title, prefix_prompt, suffix_prompt))
        self.main_prompt_field = ft.TextField(
            label="Main prompt matrix List", 
            value=main_prompt,
            min_lines=1,
            max_lines=5, 
            multiline=True,
            color=ft.colors.BLUE_700,
            #prefix_icon=ft.icons.TEXT_FIELDS,
            counter_text="Separate each prompt with new line",
            on_change= lambda e, : EventHandler.textfield_change(main_title, prefix_prompt, suffix_prompt))
        self.suffix_prompt_field = ft.TextField(
            label="suffix Prompt", 
            value=suffix_prompt,
            color=ft.colors.BLUE_700,
            #prefix_icon=ft.icons.TEXT_FIELDS,
            #counter_text="0 totle Title symbols typed",
            on_change= lambda e, : EventHandler.textfield_change(main_title, prefix_prompt, suffix_prompt))
        
        
        self.image_metadata_txt = ft.Text(value = "Metadata | Category : Animals | 0/200 Title characters | 0/49 keywords")
        self.image_title_txt = ft.Text(color=ft.colors.BLUE_700,
            value= main_title)
        self.image_keywords_txt = ft.Text(color=ft.colors.BLUE_700,
            value= main_keywords)
        

        #Button
        self.open_directory_bt=ft.ElevatedButton("Open directory",
            icon=ft.icons.FOLDER_OPEN,
            on_click=lambda _: self.get_directory_dialog.get_directory_path(),
            #disabled=page.web,
        )
        self.get_directory_dialog = ft.FilePicker(on_result=EventHandler.get_directory_result)

        self.embed_metadata_bt=ft.ElevatedButton("embed metadata",
            icon=ft.icons.DATA_OBJECT,
            on_click=lambda _: DataProcessor.embed_metadata(),
        )
        self.select_all_bt = ft.IconButton(
            icon=ft.icons.CHECK_BOX_OUTLINED,
            tooltip="Select All",
            on_click=lambda _: EventHandler.select_all())
        
        self.table_view_bt = ft.IconButton(
            icon=(ft.icons.TABLE_ROWS if images_display == "table" else ft.icons.TABLE_ROWS_OUTLINED),
            tooltip="Table View",
            on_click=lambda _: EventHandler.list_view(self.table_view_bt, "table"))
        self.list_view_bt = ft.IconButton(
            icon=(ft.icons.BALLOT if images_display == "list" else ft.icons.BALLOT_OUTLINED),
            tooltip="List View",
            on_click=lambda _: EventHandler.list_view(self.list_view_bt, "list"))
        self.thumb_view_bt = ft.IconButton(
            icon=(ft.icons.DATASET if images_display == "thumbnail" else ft.icons.DATASET_OUTLINED),
            tooltip="Thumb View",
            on_click=lambda _: EventHandler.list_view(self.thumb_view_bt, "thumbnail"))
        self.list_buttons = [self.table_view_bt, self.list_view_bt, self.thumb_view_bt]

        self.mainprompt_bt=ft.ElevatedButton("Load Prompt txt",
            icon=ft.icons.UPLOAD_FILE,
            on_click=lambda _:  self.get_txt_main.pick_files(
                allow_multiple=True,
                file_type=ft.FilePickerFileType.CUSTOM,
                allowed_extensions=["txt"]))
        self.get_txt_main = ft.FilePicker(on_result=EventHandler.get_txt_result)

        self.main_keyword_bt=ft.ElevatedButton("Load Keywords txt",
            icon=ft.icons.UPLOAD_FILE,
            on_click=lambda _:  self.get_txt_keyword.pick_files(
                allow_multiple=True,
                file_type=ft.FilePickerFileType.CUSTOM,
                allowed_extensions=["txt"]))
        self.get_txt_keyword = ft.FilePicker(on_result=EventHandler.get_keywords_result)

        self.keywords_chip_h = ft.Row([ft.Icon(ft.icons.SELL), ft.Text("Keywords")])
        self.keywords_chip_row = ft.Row([], 
            alignment=ft.MainAxisAlignment.START, spacing=10, wrap=True,)
        
        self.main_keywords_field = ft.TextField(
            label="Main Keywords", 
            value=main_keywords,
            min_lines=1,
            max_lines=5, 
            multiline=True,
            color=ft.colors.BLUE_700,
            #prefix_icon=ft.icons.SELL,
            #helper_text="Separate each keywords with , or new line",
            counter_text="Separate each keywords with , or new line",
            on_change= lambda e, : EventHandler.textfield_change(main_title, prefix_prompt, suffix_prompt),
            on_blur=lambda e: EventHandler.keywords_chip_Update(self.keywords_chip_row))
        self.keywords_chip = ft.Chip(label=ft.Text("Promt to Keyword"),on_select=DataProcessor.keywords_chip, selected=False)
    
        # ... other UI components   
    
    def build_ui(self,):
        # Create UI elements and add them to containers
        edit_content = ft.Column([ft.Text("Images Edit")])
        batch_content = ft.Column()
        config_content = ft.Column()
        self.main_container.content = self.image_container
        self.right_container.content = self.right_content
        self.right_content.controls.append(self.category_dropdown)
        self.right_content.controls.append(self.images_per_prompt_field)
        self.right_content.controls.append(self.image_title_txt)
        self.right_content.controls.append(self.prefix_prompt_field)
        self.right_content.controls.append(self.main_prompt_field)
        self.right_content.controls.append(self.suffix_prompt_field)
        self.right_content.controls.append(self.main_keywords_field)
        
        self.right_content.controls.append(self.keywords_chip_h)
        self.right_content.controls.append(self.keywords_chip_row)
        

        tabs_main = ft.Tabs(
            selected_index=0,
            tabs=[
                ft.Tab(
                    text="Images Massive Metadata",
                    icon=ft.icons.DATASET_OUTLINED,
                    content=ft.Column([
                        self.progress_bar,
                        ft.Row([
                            self.directory_path,
                            self.image_count_label,
                            self.open_directory_bt,
                            ],
                            #alignment=ft.MainAxisAlignment.START,
                            spacing=10,
                            ),
                        ft.Row([
                            ft.ResponsiveRow([
                                ft.Row(controls=[
                                    self.main_container,
                                ft.GestureDetector(content=ft.VerticalDivider(),
                                    drag_interval=10,
                                    on_pan_update=Async.move_vertical_divider,
                                    on_hover=Async.show_draggable_cursor,
                                ),
                                self.right_container,
                                ],
                                spacing=0,
                                #alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ) ],
                                spacing=0,
                                expand=True,
                            )],
                            spacing=10,
                            expand=True,
                        ),
                        
                        ft.Row([
                            self.table_view_bt,
                            self.list_view_bt,
                            self.thumb_view_bt,
                            ft.VerticalDivider(),
                            self.select_all_bt,
                            ft.Row([],expand=True,), 
                            self.mainprompt_bt,
                            self.main_keyword_bt,
                            ft.VerticalDivider(),
                            self.embed_metadata_bt,
                        ]),
                        ft.Row([
                            
                            ft.Column([
                                #self.image_metadata_txt, 
                                #self.image_title_txt, 
                                #self.image_keywords_txt,
                                ],
                                expand=True,),
                            
                        ]),
                    ]),
                        
                ),
                ft.Tab(
                    text="Images Edit",
                    icon=ft.icons.IMAGE_SEARCH,
                    content=edit_content
                ),
                ft.Tab(
                    text="Re-Upload batch",
                icon=ft.icons.BATCH_PREDICTION,
                content=ft.Column([ft.Text("Re-Upload batch")])
                ),
                ft.Tab(
                    text="Configuration",
                    icon=ft.icons.SETTINGS,
                    content=ft.Column([ft.Text("Configuration")])
                ),
                ],expand=1,
            )
        

        keywords_list, main_keywords = DataProcessor.keywords_process(self.main_keywords_field)
        print(f"keywords_list: {keywords_list}")

        for keyword in keywords_list:
            chip = (ft.Chip(label=ft.Text(keyword),on_select = lambda e, keyword=keyword, : EventHandler.keywords_selected(keyword), selected=True))
            self.keywords_chip_row.controls.append(chip)
            keywords_selected_list.append(keyword)
                
                
        for image in self.processed_data:
            self.image_container.controls.append(
                ft.Text(f"Filename: {image['Filename']},\nTitle: {image['Title']},\nKeywords: {image['Keywords']},\nCategory: {image['Category']},\nReleases: {image['Releases']}")
            )
            self.image_container.controls.append(
                ft.Divider())

        edit_content.controls.append(
            ft.Text("Content for Tab 2")
        )

        batch_content.controls.append(
            ft.Text("Content for Tab 3")
        )

        config_content.controls.append(
            ft.Text("Content for Tab 4")
        )
        
        if not self.processed_data:
            return ft.Text("No data available.")
        headers = list(self.processed_data[0].keys())
        # Create DataTable
        table = ft.DataTable(
            columns=[ft.DataColumn(ft.Text(header)) for header in headers],
            rows=[
                ft.DataRow(cells=[ft.DataCell(ft.Text(str(image[header]))) for header in headers])
                for image in self.processed_data
            ]
        )
        
        return  tabs_main

    def images_display(directory,listtype):

        image_view_thumb = ft.GridView(runs_count=5, max_extent=150, child_aspect_ratio=1.0, spacing=10, cache_extent=20)
        images_display = listtype
        main_container.content.clean()

        image_count = 0  # Initialize image count
        process_count = 0  # Initialize image count

        images_select_list = []
        metadata = DataProcessor.read_csv(directory)
        print(images_display)
        if images_display == "thumbnail":
            ui = image_view_thumb
        if images_display == "list":
            ui = ft.ListView(spacing=10,)
        if images_display == "table":
            if not processed_data:
                return ft.Text("No data available.")
            # Create header row
            ui = ft.Column(spacing=5, scroll=True)
            
        else : pass
        
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
            card.update()
            image_count_label.value = f"Select Images: {len(images_select_list)}/{image_count}"
            image_count_label.update()

        def handle_click(e, card, image_path, filename):
            DataProcessor.extract_csv(image_path)
            change_color(e, card, filename)

        for filename in os.listdir(directory):
            if filename.lower().endswith(('.jpg', '.png', '.svg')):
                image_path = os.path.join(directory, filename)
                image_metadata = next((item for item in metadata if item['Filename'] == filename), {})
                
                if images_display == "thumbnail":
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
                    ui.controls.append(card)
                    
                if images_display == "list":
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
                            options=[ft.dropdown.Option(key=f"{category}") for index, category in enumerate(adobe_categories_list)],
                            hint_text=f"{image_category}",
                            on_change=EventHandler.on_change_category_dropdown
                        ),
                    
                        ft.TextField(
                            label=("Title"),
                            value=(f"{image_metadata.get('Title', '')}"),
                            color=ft.colors.BLUE_700,
                            ),
                            
                        ft.TextField(
                            label="Keywords", 
                            value=(f"{image_metadata.get('Keywords', '')}"),
                            min_lines=1,
                            max_lines=3, 
                            multiline=True,
                            color=ft.colors.BLUE_700,
                        ),
                        ft.Row([
                            ft.Icon(name=ft.icons.PERSON_PIN),
                            ft.Text((f"{image_metadata.get('Releases', '')}"))]),
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

                    ui.controls.append(row_con)
                    ui.controls.append(ft.Divider(height=9,),)
                
                if images_display == "table":
                    card = ft.ListTile(
                        leading=ft.Image(
                                src=image_path,
                                border_radius=ft.border_radius.all(0),
                                tooltip=filename,
                                fit=ft.ImageFit.COVER,
                                width=50,
                                height=50,
                            ),
                        title=ft.Text(f"{image_metadata.get('Title', '')}"),
                        subtitle=ft.Text(f"{image_metadata.get('Keywords', '')}"),
                        dense=True,
                    )
                    ui.controls.append(card)
                    
                    
                else : pass
                process_count += 1
                progress_bar.value = process_count/(len(os.listdir(directory)))
                progress_bar.update()
                    
                image_count += 1  # Increment image count
                image_count_label.value = f"Total Images : {image_count}"
                image_count_label.update()
        
        
        # Update the label with the image count

        main_container.content = ui
        main_container.update()
       
class DataProcessor:
    def __init__(self):
        pass

    def process_image_data(self, image_data):
        # Placeholder for data processing logic
        # This is where you'll implement:
        # - Extracting metadata from image files (if necessary)
        # - Processing existing metadata (e.g., cleaning, categorizing)
        # - Generating keywords based on image content or metadata
        # - Updating image data with processed information

        # Example:
        processed_data = []
        for image in image_data:
            # Extract metadata or process existing data
            processed_image = {
                "Filename": image["Filename"],
                "Title": image.get("Title", ""),
                "Keywords": image.get("Keywords", ""),
                "Category": image.get("Category", ""),
                "Releases": image.get("Releases", ""),
            }
            processed_data.append(processed_image)
        return processed_data
    
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
    
    def serialize_image_data(image_data):
        # Convert a list of dictionaries to a serialized string format.
        return '|'.join([f"{key}:{value}" for key, value in image_data.items()])

    def deserialize_image_data(data_str):
        # Convert a serialized string format back to a list of dictionaries.
        return {item.split(':')[0]: item.split(':')[1] for item in data_str.split('|')}

    def convert_to_list(categories_str):
        # Convert a comma-separated string to a list.
        return [item.strip() for item in categories_str.split(',')]

    def convert_to_string(categories_list):
        # Convert a list to a comma-separated string.
        return ', '.join(categories_list)

    def read_config(config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        global theme, savepath, images_per_prompt, prefix_prompt, main_prompt, suffix_prompt
        global main_keywords, categories_index, adobe_categories_list, image_data, images_display
        # Access configuration values
        default_theme = config.get('DEFAULT', 'theme')
        default_savepath = config.get('DEFAULT', 'savepath')
        default_images_per_prompt = config.get('DEFAULT', 'ImagesPerPrompt')
        default_prefix_prompt = config.get('DEFAULT', 'PrefixPrompt')
        default_main_prompt = config.get('DEFAULT', 'MainPrompt')
        default_suffix_prompt = config.get('DEFAULT', 'suffixPrompt')
        default_main_keywords = config.get('DEFAULT', 'MainKeywords')
        default_categories = config.get('DEFAULT', 'SelectCategories')
        default_adobe_categories_str = config.get('DEFAULT', 'AdobeCategories')
        default_adobe_categories_list = DataProcessor.convert_to_list(default_adobe_categories_str)
        default_image_data_str = config.get('DEFAULT', 'ImageData')
        default_image_data = DataProcessor.deserialize_image_data(default_image_data_str)
        default_images_display = config.get('DEFAULT', 'imagesdisplay')

        # Access user-specific configurations
        theme = config.get('USER', 'theme', fallback=default_theme)
        savepath = config.get('USER', 'savepath', fallback=default_savepath)
        images_per_prompt = config.get('USER', 'ImagesPerPrompt', fallback=default_images_per_prompt)
        prefix_prompt = config.get('USER', 'PrefixPrompt', fallback= default_prefix_prompt)
        main_prompt = config.get('USER', 'MainPrompt', fallback=default_main_prompt)
        suffix_prompt = config.get('USER', 'suffixPrompt', fallback=default_suffix_prompt)
        main_keywords = config.get('USER', 'MainKeywords', fallback=default_main_keywords)
        categories = config.get('USER', 'SelectCategories', fallback=default_categories)
        adobe_categories_str = config.get('USER', 'AdobeCategories', fallback=default_adobe_categories_str)
        adobe_categories_list = DataProcessor.convert_to_list(adobe_categories_str)
        image_data_str = config.get('USER', 'ImageData', fallback=default_image_data_str)
        image_data = DataProcessor.deserialize_image_data(image_data_str)
        images_display = config.get('USER', 'imagesdisplay', fallback=default_images_display)

        categories_index = int(categories)

        return {
            'theme': theme,
            'savepath': savepath,
            'ImagesPerPrompt': images_per_prompt,
            'PrefixPrompt': prefix_prompt,
            'MainPrompt': main_prompt,
            'suffixPrompt': suffix_prompt,
            'MainKeywords': main_keywords,
            'SelectCategories': categories_index,
            'adobe_categories_list': adobe_categories_list,
            'ImageData': image_data,
            'imagesdisplay': images_display,
        }
    
    def main_prompt_process(): 
        main_prompt_list = [line.strip() for line in main_prompt_field.value.strip().split('\n') if line.strip()]
        return main_prompt_list
    
    def keywords_process(main_keywords_field): 
        keywords_list = main_keywords_field.value.replace("\n", ", ").replace(", ", ",").split(",")
        main_keywords = main_keywords_field.value.replace("\n", "; ").replace(", ", "; ").split(",")
        return keywords_list,main_keywords
    def embed_metadata():
        path=directory_path.value
        images = sorted([f for f in os.listdir(path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
        num = int(images_per_prompt_field.value)
        process_count = 0  # Initialize image count

        main_prompt_list = DataProcessor.main_prompt_process()
        total_prompt = len(main_prompt_list)
        keywords_list, = DataProcessor.keywords_process()

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
    
    def keywords_chip(content, main_keywords_field):
        

        def keywords_selected(e, keyword):
            if keyword in keywords_selected_list:
                keywords_selected_list.remove(keyword)
                print(keywords_selected_list)
            else : 
                keywords_selected_list.append(keyword)
                print(keywords_selected_list)
            content.update()    
            
            

        keywords_list, main_keywords = DataProcessor.keywords_process(main_keywords_field)

        print(keywords_list) 
        if content is not None:
            content.controls.clear()
            for keyword in keywords_list:
                chip = (ft.Chip(label=ft.Text(keyword),on_select = lambda e, keyword=keyword, : keywords_selected(e, keyword), selected=True))
                content.controls.append(chip)
                keywords_selected_list.append(keyword)
            
class EventHandler:
    def __init__(self):
        pass

    def handle_button_click(self, e):
        # ... handle button clicks
        pass

    def handle_file_picker(self, e):
        # ... handle file picker events
        pass

    # FilePicker dialog to select and read txt
    def get_txt_result(e: ft.FilePickerResultEvent):
        if e.files:
            file_path = e.files[0].path
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                    processed_data = content
                    main_prompt_field.value = processed_data
                    main_prompt_field.update()
                    EventHandler.textfield_change(main_title, prefix_prompt, suffix_prompt)
            except Exception as ex:
                print(f"An error occurred while loading the text file: {ex}")
        else:
            print("No file selected")

    # FilePicker dialog to select and read txt
    def get_keywords_result(e: ft.FilePickerResultEvent):
        if e.files:
            file_path = e.files[0].path
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                    processed_data = content
                    main_keywords_field.value = processed_data
                    main_keywords_field.update()
                    EventHandler.textfield_change(main_title, prefix_prompt, suffix_prompt)
                    EventHandler.keywords_chip_Update(keywords_chip_row)
            except Exception as ex:
                print(f"An error occurred while loading the text file: {ex}")
        else:
            print("No file selected")        
    
    # Create dropdown menu for categories
    def on_change_category_dropdown(event):
        category = event.control.value
        global selected_index
        selected_index = adobe_categories_list.index(category)+1  # Adjust to zero-indexed
        event.control.label="Selected Category"
        print(f"Selected category: {category} (Index: {selected_index})")
        
        event.control.update()  # Ensure the page updates if necessary

        return selected_index
    
    # FilePicker dialog to select a directory
    def get_directory_result(e: ft.FilePickerResultEvent):
        if e.path:
            global path
            path = e.path
            directory_path.value = path
            
            UIBuilder.images_display(path,images_display)
        else:
            directory_path.value = "Cancelled!"
        directory_path.update()
        return path

    def list_change(listtype_current):
        listtype=listtype_current
        CheckProcess.check_path()
        print(CheckProcess.check_path())
        if CheckProcess.check_path() == False : 
            get_directory_dialog
        else : UIBuilder.images_display(path, listtype)
        print(listtype)

    def select_all():
        if select_all_bt.icon == ft.icons.CHECK_BOX_OUTLINED:
            select_all_bt.icon = ft.icons.CHECK_BOX
        else:
            select_all_bt.icon = ft.icons.CHECK_BOX_OUTLINED
        select_all_bt.update()
        print(select_all_bt.icon)

    def list_view(bt, listtype_current):
        icons = bt.icon.upper()
        print(f"old {icons}")
        if icons.endswith("_OUTLINED"):
            icons = icons.replace("_OUTLINED", "")
            print(f"new1 {icons}")
        else:
            icons = icons
            print(f"new2 {icons}")
        bt.icon = icons
        bt.update()
        
        for button in list_buttons:
            if button != bt:
                button_icon = button.icon.upper()
                if button_icon.endswith("_OUTLINED"):
                    button.icon = button.icon
                else:
                    button.icon = button.icon + "_OUTLINED"
                button.update()

        EventHandler.list_change(listtype_current)

    def textfield_change(main_title, prefix_prompt, suffix_prompt) :

        prefix_prompt=prefix_prompt_field.value
        main_prompt = main_prompt_field.value
        suffix_prompt = suffix_prompt_field.value
        max_length_element=0
        main_prompt_list = DataProcessor.main_prompt_process()
        if len(main_prompt_list) == 1 :
            main_title = f"{prefix_prompt} {main_prompt_list[0]} {suffix_prompt}"
            main_title = f"Title : {main_title}" + f" | {len(main_title)}"
        else : 
            max_length_element = max(main_prompt_list, key=len)

            main_title = f"{prefix_prompt} {max_length_element} {suffix_prompt}"
            main_title = f"Title : {prefix_prompt} " + "{" f"{len(main_prompt_list)}" " prompt matrix}" + f" {suffix_prompt}" + f" | {len(main_title)}"

        image_title_txt.value = main_title
        if len(f"{prefix_prompt} {max_length_element} {suffix_prompt}") > 200:
            image_title_txt.color = ft.colors.RED
        else:
            image_title_txt.color = ft.colors.BLUE_700
        image_title_txt.update()
        
        
        keywords_list, main_keywords = DataProcessor.keywords_process(main_keywords_field)
        image_keywords_txt.value = f"Keywords : {main_keywords}" + f" | {len(keywords_list)}"
        if len(keywords_list) > 49:
            image_keywords_txt.color = ft.colors.RED
        else:
            image_keywords_txt.color = ft.colors.BLUE_700
        image_keywords_txt.update()

    def keywords_selected(keyword):
            if keyword in keywords_selected_list:
                keywords_selected_list.remove(keyword)
                print(keywords_selected_list)
            else : 
                keywords_selected_list.append(keyword)
                print(keywords_selected_list)   

    def keywords_chip_Update(keywords_chip_row): 
        keywords_list, main_keywords = DataProcessor.keywords_process(main_keywords_field)

        if keywords_chip_row is not None:
            keywords_chip_row.controls.clear()
            for keyword in keywords_list:
                chip = (ft.Chip(label=ft.Text(keyword),on_select = lambda e, keyword=keyword, : EventHandler.keywords_selected(keyword), selected=True))
                keywords_chip_row.controls.append(chip)
                keywords_selected_list.append(keyword)
        keywords_chip_row.update()  

class CheckProcess :
    def __init__(self):
        pass

    def check_path():
        try:
            if path is None:
                pathcheak = False
                print("please select path1")
                
            else:
                pathcheak = True
        except NameError:
            pathcheak = False
            print("please select path2")
            
        return pathcheak
    
class Async :
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

def main(page: ft.Page):

    page.title = "AutoStockPhoto"
    ft.Page.window_width = 1000
    ft.Page.window_height = 1000
    
    global theme_switch, save_path_field, images_per_prompt_field, prefix_prompt_field
    global main_prompt_field, suffix_prompt_field, main_keywords_field, progress_bar
    global adobe_categories_field,image_count_label, directory_path, processed_data,images_display
    global select_all_bt, mainprompt_bt, list_buttons, table_view_bt, list_view_bt, thumb_view_bt
    global dlg, get_directory_dialog, main_container, right_container, keywords_chip_row
    global main_title, image_title_txt, image_keywords_txt, keywords_selected_list
    

    config = DataProcessor.read_config('config.ini')
    # Use configuration values
    theme = config['theme']
    savepath = config['savepath']
    images_per_prompt = config['ImagesPerPrompt']
    prefix_prompt = config['PrefixPrompt']
    main_prompt = config['MainPrompt']
    suffix_prompt = config['suffixPrompt']
    main_keywords = config['MainKeywords']
    categories = config['SelectCategories']
    adobe_categories_list = config['adobe_categories_list']
    image_data = config['ImageData']
    images_display = config['imagesdisplay']

    categories_index = int(categories)

    main_title = f"Title : {prefix_prompt} {main_prompt} {suffix_prompt}"
    keywords_selected_list = []  

    page.theme_mode = (ft.ThemeMode.LIGHT if theme.upper() == 'LIGHT' else ft.ThemeMode.DARK)

    # Create instances of classes
    image_manager = ImageManager(savepath,)
    data_processor = DataProcessor()
    event_handler = EventHandler()
    
    # Process image data
    processed_data = data_processor.process_image_data(image_manager.image_data,)
    # Add sample processed data if none is loaded
    if not processed_data:
        print("No image data found. Adding sample data.")
        processed_data = []
        
    # Build UI
    ui_builder = UIBuilder(processed_data, main_title, prefix_prompt, suffix_prompt, main_keywords,)
    ui = ui_builder.build_ui()

    directory_path = ui_builder.directory_path
    main_container = ui_builder.main_container
    progress_bar = ui_builder.progress_bar
    image_count_label = ui_builder.image_count_label
    list_buttons = ui_builder.list_buttons
    select_all_bt = ui_builder.select_all_bt
    prefix_prompt_field = ui_builder.prefix_prompt_field
    main_prompt_field = ui_builder.main_prompt_field
    suffix_prompt_field = ui_builder.suffix_prompt_field
    main_keywords_field = ui_builder.main_keywords_field

    image_title_txt = ui_builder.image_title_txt
    image_keywords_txt = ui_builder.image_keywords_txt
    right_container = ui_builder.right_container
    keywords_chip_row = ui_builder.keywords_chip_row

    
    # Add event handlers
    # ...
    # hide all dialogs in overlay
    page.overlay.extend([ ui_builder.get_directory_dialog, ui_builder.get_txt_main, ui_builder.get_txt_keyword ])
    #page.add(tabs_main)
    page.add(ui,)
    
    # Start the app
    

ft.app(target=main)