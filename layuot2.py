import flet as ft
import pandas as pd
import exiftool
import os
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

# Main page  \\\\\\\\\\
def main(page: ft.Page):

    # Page config \\\\\\\\\\
    page.title = "Image Metadata Viewer"
    page.window_width = 1000
    page.window_height = 1000

    # Text widget to display the selected directory path
    directory_path = ft.TextField(label="Images directory path")
    csv_file_path = ft.TextField(label="CSV File Path")
    prefix_prompt = ft.TextField(label="Prefix prompt", value="Portrait view of a regular happy smiling",
        min_lines=1,max_lines=2, multiline=True,color=ft.colors.BLUE_700,)
    subfix_prompt = ft.TextField(label="Subfix prompt", value=", ultra realistic, candid, social media, avatar image, plain solid background",
        min_lines=1,max_lines=2, multiline=True,color=ft.colors.BLUE_700,)
    main_prompt = ft.TextField(label="Main prompt matrix List", value="thai",
        min_lines=1,max_lines=5, multiline=True,color=ft.colors.BLUE_700,)
    enhance_prompt = ft.TextField(label="Enhance prompt matrix List", value="boy")
    main_keywords = ft.TextField(label="Keywords", value="line1\nline2",
        min_lines=2,max_lines=3, multiline=True,color=ft.colors.BLUE_700,)
    image_title = ft.TextField(label="Title")
    image_metadata = ft.Text("Metadata")
    image_keywords = ft.TextField(label="Keywords", value="",
        min_lines=2,max_lines=5, multiline=True,color=ft.colors.BLUE_700,)
    image_keywords_chip = ft.Row([ft.Chip(label=ft.Text("Keywords01"),on_select=chip_select, selected=True),
        ft.Chip(label=ft.Text("Keywords01"),on_select=chip_select, selected=True),
        ft.Chip(label=ft.Text("Keywords01"),on_select=chip_select, selected=True),
        ft.Chip(label=ft.Text("Keywords01"),on_select=chip_select, selected=True),])
    main_prompt_list = ['Africa', 'Algeria', 'Angola', 'Benin',]
    keywords_list = []
    images_select_list = []
    images_per_prompt = ft.TextField(label="images per prompt", value="4",)
    pb = ft.ProgressBar(value=0)

    #Contant \\\\\\\\\\
    #Appbar
    appbar=ft.AppBar(
            leading=ft.Icon(ft.icons.NOW_WALLPAPER),
            leading_width=40,
            title=ft.Text("Image Metadata Viewer"),
            center_title=False,
            #bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
            ft.IconButton(ft.icons.WB_SUNNY_OUTLINED),
            ft.IconButton(ft.icons.FILTER_3),
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="Item 1"),
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(
                        text="Checked item", checked=False, on_click=""
                    ),
                ]
            ),
        ],
        )
    
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
        allowed_extensions=["csv"]),
    )

    embed_metadata_bt=ft.ElevatedButton("embed metadata",
        icon=ft.icons.DATA_OBJECT,
        on_click=lambda _: embed_metadata(),
    )

    # Container to hold image components
    image_container = ft.GridView( runs_count=5, max_extent=150,
        child_aspect_ratio=1.0, spacing=10,)
    # Define the image container and image count label
    image_count_label = ft.Text(value="Total Images: 0")

    # Container to hold image components
    csv_data_container = ft.Column()
   

    #Function \\\\\\\\\\

    # ... (chip function and main function)

    def embed_metadata():
        path=directory_path.value
        images = sorted([f for f in os.listdir(path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
        num = int(images_per_prompt.value)
        process_count = 0  # Initialize image count

        cleaned_string = main_prompt.value.replace("\n", ",").replace(", ", ",").strip(",")
        main_prompt_list = [promptst.strip() for promptst in cleaned_string.split(",") if promptst.strip()]
        total_prompt = len(main_prompt_list)
        keywords_list = main_keywords.value.replace("\n", "; ").replace(",", "; ")

        for i, prompt in enumerate(main_prompt_list):
            start_index = i * num
            end_index = start_index + num
            prompt_images = images[start_index:end_index]

            for j, image_file in enumerate(prompt_images):
                image_path = os.path.join(path, image_file)
                prompt=prompt.replace("\n", " ").replace("'", "")
                title = f"{prefix_prompt.value} {prompt} {enhance_prompt.value}{subfix_prompt.value}"
                keywords = f"{prompt}; {enhance_prompt.value}; {keywords_list}"


                with exiftool.ExifToolHelper() as et:
                    et.execute("-overwrite_original", 
                           f"-XMP:Title={title}", 
                           f"-XMP:Subject={keywords}", 
                           image_path)
                    process_count += 1
                    image_count_label.value = f"Total process Images: {process_count}"
                    image_count_label.update()
                    
                    pb.value = process_count/(total_prompt*num)
                    pb.update()
                    print(pb.value)    
        print(main_prompt_list)
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
        for filename in os.listdir(directory):
            if filename.lower().endswith(('.jpg', '.png', '.svg')):
                image_path = os.path.join(directory, filename)

                image_component = ft.Stack([
                    ft.Image(src=image_path, width=150, height=150,
                        border_radius=ft.border_radius.all(10),tooltip=filename,fit=ft.ImageFit.COVER
                        ),
                    ft.Container(
                    content=ft.CircleAvatar(bgcolor=ft.colors.GREEN, radius=5),
                    alignment=ft.alignment.top_left,margin=5,),
                    ft.Container(
                    content= ft.Checkbox(value=False,
                    on_change=lambda e, filename=filename: images_select(filename) ,),
                    alignment=ft.alignment.bottom_right,margin=0,ink=True,padding=5,
                    on_click=lambda e, image_path=image_path, : extract_metadata(image_path),
                    ),    
                ],)
                image_container.controls.append(image_component)
                image_count += 1  # Increment image count
        
        # Update the label with the image count
        image_count_label.value = f"Total Images: {image_count}"
        page.update()
        return image_component
    

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
                            ft.TextField(label="Title", value=row['Title']),
                            ft.Row([*keyword_texts]),
                            ft.TextField(label="Description", value=row['Description']),
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
    
    
    
    

    # hide all dialogs in overlay
    page.overlay.extend([pick_files_dialog, get_directory_dialog])

    # UI setup
    page.add(
        appbar,
        ft.Row([image_count_label,],alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        pb,
         # Image contant layout
        ft.Row(
            [
                ft.Container(
                    content=image_container,
                    #bgcolor=ft.colors.ORANGE_300,
                    alignment=ft.alignment.top_center,
                    expand=True,
                ),
                ft.Container(
                    content=ft.Column([
                        #ft.Text("Images"),  
                        directory_path,
                        open_directory_bt,
                        
                        #ft.Text("Prompt to Title"),
                        images_per_prompt,
                        prefix_prompt,
                        main_prompt,
                        enhance_prompt,
                        subfix_prompt,
                        #ft.Text("Keywords"),
                        # Pick csv files
                        # Load csv data
                        csv_file_path,
                        ft.Row([pick_csv_bt, ft.ElevatedButton("Load csv data", on_click=read_csv)],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,),
                        main_keywords,
                        ft.Row([ft.ElevatedButton("Test", on_click=image_metadata_Process),embed_metadata_bt, ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,),  
                        csv_data_container,
                        
                        ], scroll=ft.ScrollMode.AUTO,alignment=ft.MainAxisAlignment.START),
                    #bgcolor=ft.colors.BROWN_400,
                    alignment=ft.alignment.top_left,
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
        ft.Row([]),
        
    )


# Run the app
ft.app(target=main)    