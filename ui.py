from flet import (
    UserControl,
    Column,
    Container,
    IconButton,
    Row,
    Text,
    IconButton,
    NavigationRail,
    NavigationRailDestination,
    TextField,
    alignment,
    border_radius,
    colors,
    icons,
    Icon,
    padding,
    margin,
    TextButton,
    Page,
    MainAxisAlignment,
    ResponsiveRow,
    GestureDetector,
    Divider,
    VerticalDivider,
    DragUpdateEvent,
    GridView,
    ListView,
    HoverEvent,
    MouseCursor,
    SegmentedButton,
    Segment,
    CupertinoSlidingSegmentedButton,
    ProgressBar,
    Dropdown,
    dropdown,
    WindowDragArea,
    Chip,
    ElevatedButton,
    FilePicker,
    FilePickerFileType,
    Card,
    Stack,
    Image,
    ImageFit,
    CircleAvatar,
    RoundedRectangleBorder,
    CrossAxisAlignment,
    ListTile,
    FilePickerResultEvent,
    ThemeMode,
    Slider,
    TextAlign,
    ButtonStyle,
    CircleBorder,
)

import os
from event_handler import EventHandler
from data_processor import DataProcessor
from image_manager import ImageManager
from check_process import CheckProcess
from custom_class import ImageCard, ImageCardList


class UIBuilder(UserControl):

    def __init__(self, page):
        super().__init__()
        
        self.page = page  # Save the page instance

        # config data
        config= DataProcessor.read_config('config.ini')

        theme = config['Theme']
        savepath = config['SavePath']
        images_per_prompt = config['ImagesPerPrompt']
        prefix_prompt = config['PrefixPrompt']
        main_prompt = config['MainPrompt']
        suffix_prompt = config['SuffixPrompt']
        main_keywords = config['MainKeywords']
        select_categories =  config['SelectCategories']
        adobe_categories_list = config['AdobeCategoriesList']
        image_data = config['ImageData']
        images_listtype = config['ImagesDisplay']
        default_path = config['DefaultPath']
        
        main_title = f"Title : {prefix_prompt}{main_keywords}{suffix_prompt}"
        self.adobe_categories_list = adobe_categories_list
        self.images_listtype = images_listtype
        
        self.page.theme_mode = (ThemeMode.LIGHT if theme.upper() == 'LIGHT' else ThemeMode.DARK)

        # Create Save Button
        self.save_config_btt = ElevatedButton(text="Save", on_click=lambda e: EventHandler.save_user_data(e, "Data saved successfully!", self.page, self.theme_switch_csb))

        self.theme_switch_csb = CupertinoSlidingSegmentedButton(
            selected_index = 0 if self.page.theme_mode == ThemeMode.LIGHT else 1,
            #thumb_color=colors.BLUE_400,
            on_change=lambda e: EventHandler.toggle_theme(e, self.page),
            padding=padding.symmetric(0, 10),
            controls=[
                Text("LIGHT Theme"),
                Text("DARK Theme"),
            ],
        )

        # Top_menu
        self.open_dir_btt = IconButton(icon=icons.FOLDER_OPEN,
            on_click=lambda _: self.get_directory_dialog.get_directory_path(),)
        self.stat_txt = Text("",)
        self.path_txt = Text("",)
        self.top_menu_row = Row([
            self.path_txt, 
            self.stat_txt, 
            self.open_dir_btt], 
            spacing=0, alignment=MainAxisAlignment.SPACE_BETWEEN,)

        # windows top
        self.windows_row = Row([
                WindowDragArea(Container(Row([
                    Text(" AutoStockPhoto - beta 0.3.0"),
                    Row([], expand=True),
                    self.path_txt, 
                    VerticalDivider(),
                    self.stat_txt, 
                    VerticalDivider(),
                    self.open_dir_btt,
                    IconButton(icons.CLOSE, on_click=lambda e: self.page.window.close()),
                    ], expand=True ), #bgcolor=colors.GREY_100, 
                    padding=0), expand=True),
                ],  )
        
        # Text widget to display prompt
        self.images_per_prompt = TextField(value=f"{images_per_prompt}",width=50,)
        self.images_per_prompt_sld = Slider(label="{value}",
            min=1, max=20, divisions=19, value=f"{images_per_prompt}", expand=True,
            on_change=lambda e: EventHandler.slider_changed(e, self.images_per_prompt)
            )
        self.images_per_prompt_row = Row([
            Text("images per prompt : ", text_align = TextAlign.CENTER),
            
            self.images_per_prompt_sld,
            self.images_per_prompt,
        ], alignment=MainAxisAlignment.START, vertical_alignment=CrossAxisAlignment.CENTER )

        self.prefix_prompt_txf = TextField(
            label="Prefix prompt", value=f"{prefix_prompt}",
            min_lines=1,max_lines=2, multiline=True,color=colors.BLUE_700,
            on_change= lambda e, : EventHandler.textfield_change(self.main_title_txt, self.main_keywords_txt, self.prefix_prompt_txf, self.main_prompt_txf, self.suffix_prompt_txf, self.main_keywords_txf,),
        )
        self.main_prompt_txf = TextField(label="Main prompt matrix List", value=f"{main_prompt}",
            min_lines=1,max_lines=5, 
            multiline=True,color=colors.BLUE_700,
            hint_text="Separate prompt with new line",
            on_change= lambda e, : EventHandler.textfield_change(self.main_title_txt, self.main_keywords_txt, self.prefix_prompt_txf, self.main_prompt_txf, self.suffix_prompt_txf, self.main_keywords_txf,),
            )
        self.suffix_prompt_txf = TextField(label="Suffix prompt", value=f"{suffix_prompt}",
            min_lines=1,max_lines=2, multiline=True,color=colors.BLUE_700,
            on_change= lambda e, : EventHandler.textfield_change(self.main_title_txt, self.main_keywords_txt, self.prefix_prompt_txf, self.main_prompt_txf, self.suffix_prompt_txf, self.main_keywords_txf,),
            )

        self.main_keywords_txf = TextField(label="Keywords", value=f"{main_keywords}",
            min_lines=1,max_lines=5, 
            multiline=True,
            color=colors.BLUE_700,
            hint_text="Separate keywords with , or new line",
            on_change= lambda e, : EventHandler.textfield_change(self.main_title_txt, self.main_keywords_txt, self.prefix_prompt_txf, self.main_prompt_txf, self.suffix_prompt_txf, self.main_keywords_txf,),
            on_blur=lambda e: EventHandler.keywords_chip_Update(self.keywords_chip_row, self.main_keywords_txf, self.keywords_select_list,),
            )
        
        self.main_title_txt = Text(color=colors.BLUE_700,
            value= main_title)
        self.main_keywords_txt = Text(color=colors.BLUE_700, value = main_keywords,)
        
        self.image_title_txf = TextField(label="Title")
        self.image_metadata_txt = Text("Metadata")
        self.image_keywords_txf = TextField(label="Keywords", value="",
            min_lines=2,max_lines=3, multiline=True,color=colors.BLUE_700,)
        
        self.csv_path_txf = TextField(label="CSV File Path")
        self.defaul_path_txf = TextField(label="Default Path", value=default_path)
        self.images_display_csb = CupertinoSlidingSegmentedButton(
            selected_index=1,
            #thumb_color=colors.BLUE_400,
            on_change=lambda e: print(f"selected_index: {e.data}"),
            padding=padding.symmetric(0, 10),
            controls=[
                Text("thumbnail"),
                Text("table"),
                Text("list"),
            ],
        )
        
        # Create instances of classes
        image_manager = ImageManager(savepath,)
        # Process image data
        self.processed_data = DataProcessor.process_image_data(self, image_manager.image_data,)
        # Add sample processed data if none is loaded
        if not self.processed_data:
            print("No image data found. Adding sample data.")
            self.processed_data = []

        self.main_prompt_list = []
        self.keywords_list = []
        self.keywords_select_list = []
        self.images_select_list = []
        
        self.progress_bar = ProgressBar(bar_height=2, value=0, )
        
        self.category_dropdown = Dropdown(
            label=(f"{adobe_categories_list[int(select_categories-1)]}" if select_categories is not None and select_categories > 0 else "Select Category"),
            options=[dropdown.Option(key=f"{category}") for index, category in enumerate(adobe_categories_list)],
            on_change=lambda e:EventHandler.on_change_category_dropdown(e, adobe_categories_list),)
        
        self.keywords_chip_h = Row([Icon(icons.LABEL), Text(color=colors.BLUE_700, value ="keywords :",)])
        self.keywords_chip_row = Row([], alignment=MainAxisAlignment.START, spacing=10, wrap=True,)


        #Get Button
        self.open_directory_btt=ElevatedButton("Open directory",
            icon=icons.FOLDER_OPEN,
            on_click=lambda e: self.get_directory_dialog.get_directory_path(),
            style=ButtonStyle(shape=CircleBorder(), padding=64)
            #disabled=page.web,
        )
        self.get_directory_dialog = FilePicker(on_result=lambda e: self.get_directory_result(e, self.path_txt, self.images_listtype))

        # Get txt Menu
        self.prompt_txt_btt=ElevatedButton("Load Prompt txt",
            icon=icons.UPLOAD_FILE,
            on_click=lambda e:  self.get_txt_prompt.pick_files(
                allow_multiple=True,
                file_type=FilePickerFileType.CUSTOM,
                allowed_extensions=["txt"]))
        self.get_txt_prompt = FilePicker(on_result=lambda e: EventHandler.get_prompt_result(e, self.main_title_txt, self.main_keywords_txt, self.prefix_prompt_txf, self.main_prompt_txf, self.suffix_prompt_txf, self.main_keywords_txf,))

        self.keyword_txt_btt=ElevatedButton("Load Keywords txt",
            icon=icons.UPLOAD_FILE,
            on_click=lambda e:  self.get_txt_keyword.pick_files(
                allow_multiple=True,
                file_type=FilePickerFileType.CUSTOM,
                allowed_extensions=["txt"]))
        self.get_txt_keyword = FilePicker(on_result=lambda e: EventHandler.get_keywords_result(e, self.main_title_txt, self.main_keywords_txt, self.prefix_prompt_txf, self.main_prompt_txf, self.suffix_prompt_txf, self.main_keywords_txf, self.keywords_chip_row, self.keywords_select_list))

        # Embed metadata
        self.embed_metadata_bt=ElevatedButton("embed metadata",
            icon=icons.DATA_OBJECT,
            on_click=lambda e: DataProcessor.embed_metadata(self.path_txt, self.images_per_prompt, self.prefix_prompt_txf, self.main_prompt_txf, self.suffix_prompt_txf, self.main_keywords_txf, self.category_dropdown, self.stat_txt, self.progress_bar),
        )

        # Bottom_menu
        self.select_all_btt = IconButton(
            icon=icons.CHECK_BOX_OUTLINED,
            tooltip="Select All",
            on_click=lambda e: EventHandler.select_all(self.select_all_btt))
        
        self.table_view_btt = IconButton(
            icon=(icons.TABLE_ROWS if images_listtype == "table" else icons.TABLE_ROWS_OUTLINED),
            tooltip="Table View",
            on_click=lambda e: self.list_view(self.table_view_btt, "table"))
        self.thumb_view_btt = IconButton(
            icon=(icons.DATASET if images_listtype == "thumbnail" else icons.DATASET_OUTLINED),
            tooltip="Thumb View",
            on_click=lambda e: self.list_view(self.thumb_view_btt, "thumbnail"))
        self.list_view_btt = IconButton(
            icon=(icons.BALLOT if images_listtype == "list" else icons.BALLOT_OUTLINED),
            tooltip="List View",
            on_click=lambda e: self.list_view(self.list_view_btt, "list"))
        self.view_btt_list = [self.table_view_btt, self.thumb_view_btt, self.list_view_btt]
        self.bottom_menu_row = Row([
            VerticalDivider(),
            self.prompt_txt_btt,
            VerticalDivider(),
            self.keyword_txt_btt,
            VerticalDivider(),
            self.embed_metadata_bt,
            Row([], expand=True),
            self.select_all_btt,
            VerticalDivider(),
            self.table_view_btt, 
            self.thumb_view_btt, 
            self.list_view_btt], 
            spacing=0, alignment=MainAxisAlignment.END,)




        # Main_UI
        self.content_div = VerticalDivider(width=4, thickness=1)
        self.content_ges = GestureDetector()
        self.content_row = Row([], spacing=0, alignment=MainAxisAlignment.SPACE_BETWEEN)
        self.body_res = ResponsiveRow([], expand=True, spacing=0,)
        self.body_row = Row([], expand=True, spacing=0, alignment=MainAxisAlignment.START)
        self.body_col = Column([], expand=True, spacing=0)
        self.main_ctn = Container(expand=True, padding = 0, margin=0)
        self.main_menu_col = Column([])
        self.main_row = Row([], expand=True, spacing=0,)

        # Container to hold image components

        self.start_content = Row([self.open_directory_btt], expand=True, spacing=0,alignment=MainAxisAlignment.CENTER)
        self.right_content = GridView( 
            runs_count=5, 
            max_extent=150,
            child_aspect_ratio=1.0, 
            spacing=10,
            cache_extent=20,
        )
        self.main_content = ListView(  
            spacing=10,
        )

        self.right_container = Container(
            # bgcolor=colors.BROWN_400,
                alignment=alignment.center,
                width=400,  # Start width, adjusted according to total width
                expand=False,
                content=self.open_directory_btt,
                padding = 10,
        )
        self.main_container = Container(
            content=self.main_content,
            #bgcolor=colors.ORANGE_300,
            alignment=alignment.center,
            width=600,
            padding = 10,
            expand=True,
        )

        self.web_seg_btt = SegmentedButton(
            selected_icon=Icon(icons.CHECK),
            selected={"1", "4"},
            allow_multiple_selection=True,
            segments=[
                Segment(
                    value="1",
                    label=Text("AdobeStock"),
                    #icon=Icon(icons.LOOKS_ONE),
                ),
                Segment(
                    value="2",
                    label=Text("DreamsTime"),
                    #icon=Icon(icons.LOOKS_TWO),
                ),
                Segment(
                    value="3",
                    label=Text("123rf"),
                    #icon=Icon(icons.LOOKS_3),
                ),
                Segment(
                    value="4",
                    label=Text("FreePik"),
                    #icon=Icon(icons.LOOKS_4), vecteezy
                ),
                Segment(
                    value="5",
                    label=Text("Vecteezy"),
                    #icon=Image(src="assets/icon.png", width=24, height=24),
                    #icon=Icon(icons.LOOKS_4), vecteezy
                ),
            ],
        )
        




    # Build Main_menu UI
    def build_mainmenu(self,menu_style):
        self.main_menu_col.controls.clear()

        if menu_style == "icon":
            toggle_menu_btt = TextButton("", icon=icons.MENU, on_click=lambda _: self.build_mainmenu("text"))
            images_mass_btt = TextButton("", icon=icons.DATASET_OUTLINED, on_click= lambda e: self.build_massive())
            aigen_btt = TextButton("", icon=icons.AUTO_AWESOME, on_click= lambda e: self.build_aigen())
            upscale_btt = TextButton("", icon=icons.OPEN_IN_NEW, on_click= lambda e: self.build_upscale())
            remove_bg_btt = TextButton("", icon=icons.TEXTURE, on_click= lambda e: self.build_removebg())
            account_btt = TextButton("", icon=icons.ACCOUNT_CIRCLE_OUTLINED, on_click= lambda e: self.build_user())
            setting_btt = TextButton("", icon=icons.SETTINGS_OUTLINED, on_click= lambda e: self.build_setting())
        else:
            toggle_menu_btt = TextButton("Menu", icon=icons.MENU, on_click=lambda _: self.build_mainmenu("icon"))
            images_mass_btt = TextButton("Massive Metadata", icon=icons.DATASET_OUTLINED, on_click= lambda e: self.build_massive())
            aigen_btt = TextButton("AI Generate", icon=icons.AUTO_AWESOME, on_click= lambda e: self.build_aigen())
            upscale_btt = TextButton("Images Upscale", icon=icons.OPEN_IN_NEW, on_click= lambda e: self.build_upscale())
            remove_bg_btt = TextButton("Remove Background", icon=icons.TEXTURE, on_click= lambda e: self.build_removebg())
            account_btt = TextButton("Account", icon=icons.ACCOUNT_CIRCLE_OUTLINED, on_click= lambda e: self.build_user())
            setting_btt = TextButton("Setting", icon=icons.SETTINGS_OUTLINED, on_click= lambda e: self.build_setting())

        main_menu_top_items = [images_mass_btt, aigen_btt, upscale_btt, remove_bg_btt]
        main_menu_bottom_items = [account_btt, setting_btt]
        
        self.main_menu_col.controls.append(toggle_menu_btt)
        self.main_menu_col.controls.append(Divider(),)
        for menu in main_menu_top_items :
            self.main_menu_col.controls.append(menu)
        self.main_menu_col.controls.append(Column([], expand=True),)
        for menu in main_menu_bottom_items :
            self.main_menu_col.controls.append(menu)

        self.page.update()
        return self.main_menu_col
    
    # Build Main_menu UI
    def build_massive(self):

        ui_head = Text("Massive Metadata Embed")
        self.main_content.controls.clear()
        
        self.main_content.controls.append(ui_head)
        self.main_content.controls.append(self.web_seg_btt)
        self.main_content.controls.append(self.images_per_prompt_row)
        self.main_content.controls.append(Divider(height=1,))
        self.main_content.controls.append(self.category_dropdown)
        self.main_content.controls.append(self.main_title_txt)
        self.main_content.controls.append(self.prefix_prompt_txf)
        self.main_content.controls.append(self.main_prompt_txf)
        self.main_content.controls.append(self.suffix_prompt_txf)
        self.main_content.controls.append(Divider(height=1,))
        self.main_content.controls.append(self.main_keywords_txf)
        self.main_content.controls.append(self.keywords_chip_h)
        self.main_content.controls.append(self.main_keywords_txt)
        self.main_content.controls.append(self.keywords_chip_row)


        self.page.update()
        return self.main_content
    
    # Build user UI
    def build_aigen(self):
        ui_head = Text("AI Generate")
        ai_provide_seg = SegmentedButton(
            selected_icon=Icon(icons.CHECK),
            selected={"1",},
            allow_multiple_selection=False,
            segments=[
                Segment(
                    value="1",
                    label=Text("Open Ai"),
                    #icon=Icon(icons.LOOKS_ONE),
                ),
                Segment(
                    value="2",
                    label=Text("Gemini"),
                    #icon=Icon(icons.LOOKS_TWO),
                ),
            ],
        )
        
        self.main_content.controls.clear()
        
        self.main_content.controls.append(ui_head)
        self.main_content.controls.append(ai_provide_seg)

        self.page.update()
        return self.main_content
    
    # Build upscale UI
    def build_upscale(self):
        from upscale import UpScale
        def slider_changed(e):
            scale_txt.value = f"Scale : {int(e.control.value)}X"
            self.page.update()
        def denoise_changed(e):
            denoise_txt.value = f"Denoise Strength : {(e.control.value)}"
            self.page.update()

        ui_head = Text("Upscale")
        scale_txt = Text("Scale")
        denoise_txt = Text("Denoise Strength")
        
        model_files = UpScale.get_model_files()
        model_dropdown = Dropdown(
            label="Upscale Model",
            options=[dropdown.Option(model) for model in model_files],
        )
        scale_slider = Slider(min=2, max=4, value=2, divisions=2, label="{value}", expand=True, on_change=slider_changed)
        denoise_slider = Slider(min=0, max=1, value=0.5, divisions=10, label="{value}", expand=True, on_change=denoise_changed)

        input_image = Image(width=300, height=300, fit=ImageFit.CONTAIN, src="assets/blank-thumbnail.jpg")
        output_image = Image(width=300, height=300, fit=ImageFit.CONTAIN, src="assets/blank-thumbnail.jpg")

        scale_txt.value = f"Scale : {int(scale_slider.value)}X"
        denoise_txt.value = f"Denoise Strength : {(denoise_slider.value)}"

        upscale_button = ElevatedButton("Upscale", on_click=lambda e: UpScale.upscale_image(e, input_image, model_dropdown, output_image, self.page))
        batch_seg = SegmentedButton(
            selected_icon=Icon(icons.CHECK),
            selected={"1",},
            allow_multiple_selection=False,
            segments=[
                Segment(
                    value="1",
                    label=Text("Single Image"),
                    #icon=Icon(icons.LOOKS_ONE),
                ),
                Segment(
                    value="2",
                    label=Text("Select Folder"),
                    #icon=Icon(icons.LOOKS_TWO),
                ),
            ],
        )

        self.main_content.controls.clear()
        
        self.main_content.controls.append(ui_head)
        
        self.main_content.controls.append(model_dropdown)
        self.main_content.controls.append(Row([scale_txt, scale_slider], expand=True))
        self.main_content.controls.append(Row([denoise_txt, denoise_slider], expand=True))

        self.main_content.controls.append(batch_seg)
        self.main_content.controls.append(Row([ElevatedButton("Choose image",), ElevatedButton("Choose Folder",)]))
        self.main_content.controls.append(Row([input_image, output_image], expand=True, spacing=0))

        self.main_content.controls.append(upscale_button)

        self.page.update()
        return self.main_content
    
    # Build upscale UI
    def build_removebg(self):
        from removebg import RemoveBG

        ui_head = Text("Remove Background")
        
        input_image = Image(width=300, height=300, fit=ImageFit.CONTAIN, src="assets/blank-thumbnail.jpg")
        output_image = Image(width=300, height=300, fit=ImageFit.CONTAIN, src="assets/blank-thumbnail.jpg")
        batch_seg = SegmentedButton(
            selected_icon=Icon(icons.CHECK),
            selected={"1",},
            allow_multiple_selection=False,
            segments=[
                Segment(
                    value="1",
                    label=Text("Single Image"),
                    #icon=Icon(icons.LOOKS_ONE),
                ),
                Segment(
                    value="2",
                    label=Text("Select Folder"),
                    #icon=Icon(icons.LOOKS_TWO),
                ),
            ],
        )
        
        self.main_content.controls.clear()
        
        self.main_content.controls.append(ui_head)
        self.main_content.controls.append(batch_seg)
        
        self.main_content.controls.append(Row([ElevatedButton("Choose image",), ElevatedButton("Choose Folder",)]))
        self.main_content.controls.append(Row([input_image, output_image], expand=True, spacing=0))

        self.page.update()
        return self.main_content

    # Build user UI
    def build_user(self):
        config= DataProcessor.read_config('config.ini')

        username = config['Username']
        passwords = config['Passwords']
        openai_api = config['OpenAiApi']
        gemini_api = config['GeminiApi']

        ui_head = Text("Account")
        username_txf = TextField(label="Username", value=f"{username}")
        passwords_txf = TextField(label="Passwords", value=f"{passwords}", password=True, can_reveal_password=True)

        openai_api_txf = TextField(label="Open Ai Api", value=f"{openai_api}", password=True, can_reveal_password=True)
        get_openai_api = Row([Text(value="Open Ai"), Row([], expand=True), TextButton(text="get Open ai api", on_click=lambda e:  e.control.page.launch_url("https://platform.openai.com/settings/profile?tab=api-keys")),])

        gemini_api_txf = TextField(label="Gemini Api", value=f"{gemini_api}", password=True, can_reveal_password=True)
        get_gemini_api = Row([Text(value="Gemini"), Row([], expand=True), TextButton(text="get Gemini api", on_click=lambda e:  e.control.page.launch_url("https://aistudio.google.com/app/apikey")),])

        token_txt = Row([Text(value="Your Token : 100"), Row([], expand=True), ElevatedButton("Buy Token", icon=icons.GENERATING_TOKENS_SHARP),])

        

        self.main_content.controls.clear()
        
        self.main_content.controls.append(ui_head)
        self.main_content.controls.append(username_txf)
        self.main_content.controls.append(passwords_txf)
        self.main_content.controls.append(Divider(height=1,))
        self.main_content.controls.append(get_openai_api)
        self.main_content.controls.append(openai_api_txf)
        
        self.main_content.controls.append(Divider(height=1,))
        self.main_content.controls.append(get_gemini_api)
        self.main_content.controls.append(gemini_api_txf)
        
        self.main_content.controls.append(Divider(height=1,))
        self.main_content.controls.append(token_txt)
        
        self.page.update()
        return self.main_content

    def build_setting(self):
        ui_head = Text("Setting")
        adobe_mr_title = Row([Icon(icons.PERSON_PIN), Text("Adobe model releases"),Row([], expand=True), IconButton(icon=icons.PERSON_ADD_ALT_OUTLINED,)])
        adobe_mr_chp = Chip(
        label=Text("model_releases1"),
        leading=Icon(icons.PERSON_PIN),
        selected=True,
        on_click=lambda e: print("adobe_model_releases"),
        )
    
        self.main_content.controls.clear()
        self.main_content.controls.append(ui_head)
        self.main_content.controls.append(self.theme_switch_csb)
        self.main_content.controls.append(self.web_seg_btt)
        self.main_content.controls.append(self.defaul_path_txf)
        self.main_content.controls.append(self.images_display_csb)
        self.main_content.controls.append(self.category_dropdown)
        self.main_content.controls.append(self.images_per_prompt_row)
        self.main_content.controls.append(self.prefix_prompt_txf)
        self.main_content.controls.append(self.main_prompt_txf)
        self.main_content.controls.append(self.suffix_prompt_txf)
        self.main_content.controls.append(self.main_keywords_txf)
        
        self.main_content.controls.append(Divider(height=1,))
        self.main_content.controls.append(adobe_mr_title)
        self.main_content.controls.append(adobe_mr_chp)
        self.main_content.controls.append(Divider(height=1,))
        self.main_content.controls.append(self.save_config_btt)

        self.content_row.update()
        self.main_content.update()


    def build_ui(self,):

        # Create DragUpdateEvent UI
        async def move_vertical_divider(e: DragUpdateEvent):
            new_width = self.main_container.width + e.delta_x
            if 100 <= new_width <= 900 and 150 <= self.right_container.width - e.delta_x:
                self.main_container.width = new_width
                self.right_container.width -= e.delta_x
                await self.main_container.update_async()
                await self.right_container.update_async()

        async def show_draggable_cursor(e: HoverEvent):
                e.control.mouse_cursor = MouseCursor.RESIZE_LEFT_RIGHT
                await e.control.update_async()
        
        self.content_ges = GestureDetector(
            drag_interval=10,
            on_pan_update=move_vertical_divider,
            on_hover=show_draggable_cursor,
            )
        
        self.main_menu_col = self.build_mainmenu("icon")
        
        # Create main menu UI
        self.build_massive()

        #self.main_content.controls.append(Row([self.prompt_txt_btt, self.keyword_txt_btt], alignment=MainAxisAlignment.SPACE_BETWEEN, wrap=True,))
        
        

        self.content_ges.content= self.content_div

        self.content_row.controls.append(self.main_container,)
        self.content_row.controls.append(self.content_ges)
        self.content_row.controls.append(self.right_container,)

        self.right_container.content= self.start_content
        
        
        
        # Create UI elements and add them to containers
        ui1 = Row([Container(
            self.main_menu_col, 
            #bgcolor=colors.GREY_100,
            ),
            #self.content_div,
            Container( content=
                Column([
                    self.windows_row,
                    self.progress_bar,
                    #self.top_menu_row,
                    
                    Row([
                        ResponsiveRow([
                            self.content_row
                            ], expand=True,spacing=0,), 
                        ], expand=True, spacing=0, alignment=MainAxisAlignment.START, 
                    ),

                    Divider(),
                    self.bottom_menu_row,       
                    ], expand=True, 
                ), expand=True, padding = 0, margin=0, 
                #bgcolor=colors.RED, 
            ),
            ],expand=True, spacing=0,
        )
        
        keywords_list, main_keywords = DataProcessor.keywords_process(self.main_keywords_txf)
        print(f"keywords_list: {keywords_list}")

        for keyword in keywords_list:
            chip = (Chip(label=Text(keyword),on_select = lambda e, keyword=keyword, : EventHandler.keywords_selected(keyword), selected=True))
            self.keywords_chip_row.controls.append(chip)
            
        return ui1
    
    # FilePicker dialog to select a directory
    def get_directory_result(self, e: FilePickerResultEvent, path_txt, listtype):
        if e.path:
            global path
            path = e.path
            path_txt.value = path
            
            self.images_display(path,listtype)
        else:
            path_txt.value = "Cancelled!"
        path_txt.update()
        return path
    
    def images_display(self,directory,listtype):

        self.right_container.content.clean()

        image_count = 0  # Initialize image count
        process_count = 0  # Initialize image count

        images_select_list = []
        metadata = DataProcessor.read_csv(directory)
        print(listtype)
        if listtype == "thumbnail":
            ui = GridView(runs_count=5, max_extent=150, child_aspect_ratio=1.0, spacing=10, cache_extent=20)
        if listtype == "list":
            ui = ListView(spacing=10, cache_extent = 20)
        if listtype == "table":
            if not self.processed_data:
                return Text("No data available.")
            # Create header row
            ui = ListView(spacing=10, cache_extent = 20)
            
        else : pass
        
        def change_color(e, card, filename):
            if card.color == colors.BLUE:
                card.color = colors.GREY_50
                if filename in images_select_list:
                    images_select_list.remove(filename)
                    print(images_select_list)
            elif card.color == colors.GREY_50:
                card.color = colors.BLUE
                if filename not in images_select_list:
                    images_select_list.append(filename)
                    print(images_select_list)
            card.update()
            self.stat_txt.value = f"Select Images: {len(images_select_list)}/{image_count}"
            self.stat_txt.update()

        def handle_click(e, card, image_path, filename):
            DataProcessor.extract_csv(image_path)
            change_color(e, card, filename)

        for filename in os.listdir(directory):
            if filename.lower().endswith(('.jpg', '.png', '.svg')):
                image_path = os.path.join(directory, filename)
                image_metadata = next((item for item in metadata if item['Filename'] == filename), {})
                
                if listtype == "thumbnail":
                    card = ImageCard(image_path, filename, 0, colors.GREY)

                    # Now set the on_click handler
                    card.content.content.controls[2].on_click = lambda e, card=card, image_path=image_path, filename=filename: handle_click(e, card, image_path, filename)
                    ui.controls.append(card)
                    
                if listtype == "list":
                    card_content = Card(content=
                    Container(content=
                        Stack([
                            Image(
                                src=image_path,
                                border_radius=border_radius.all(0),
                                tooltip=filename,
                                fit=ImageFit.COVER,
                                width=100,
                                height=100,
                            ),
                            Container(content=
                                Container(content=         
                                    Row([
                                        Row([
                                            Icon(name=icons.SELL, size=12),
                                            Text(value="10", size=10,),
                                        ],alignment=MainAxisAlignment.START,
                                        ),    
                                        CircleAvatar(bgcolor=colors.GREY, radius=4),
                                    ],alignment=MainAxisAlignment.SPACE_BETWEEN,
                                    ),bgcolor=colors.GREY_50,opacity=0.5,height=24,
                                    alignment=alignment.bottom_right,margin=0,padding=5,
                                ),
                                alignment=alignment.bottom_center,margin=0,
                            ),
                            Container(
                                alignment=alignment.bottom_right,margin=0,
                                ink=True,padding=padding.only(0),
                                on_click=None,  # Set to None initially
                            ),   
                        ]),margin=3,
                    ),shape=RoundedRectangleBorder(radius=0),
                    margin=0,color = colors.GREY_50,
                    width=100, height=100,
                )
                    # Now set the on_click handler
                    card_content.content.content.controls[2].on_click = lambda e, card=card_content, image_path=image_path, filename=filename: handle_click(e, card, image_path, filename)
                    
                    category = image_metadata.get('Category')

                    if category is not None and category > 0:
                        image_category = self.adobe_categories_list[int(category) - 1]
                    else:
                        image_category = "Selected Category"
                                        
                    print(image_metadata)
                        

                    right_con=Column([
                        
                        Dropdown(
                            label=None,
                            options=[dropdown.Option(key=f"{category}") for index, category in enumerate(self.adobe_categories_list)],
                            hint_text=f"{image_category}",
                            on_change=EventHandler.on_change_category_dropdown
                        ),
                    
                        TextField(
                            label=("Title"),
                            value=(f"{image_metadata.get('Title', '')}"),
                            color=colors.BLUE_700,
                            ),
                            
                        TextField(
                            label="Keywords", 
                            value=(f"{image_metadata.get('Keywords', '')}"),
                            min_lines=1,
                            max_lines=3, 
                            multiline=True,
                            color=colors.BLUE_700,
                        ),
                        Row([
                            Icon(name=icons.PERSON_PIN),
                            Text((f"{image_metadata.get('Releases', '')}"))]),
                            Divider(height=9,)
                            ],
                            expand=True,
                        )
                    row_con=Row([
                        card_content,
                        right_con,
                        ],
                        alignment=MainAxisAlignment.START,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                        expand=True,
                    )

                    ui.controls.append(row_con)
                    
                
                elif listtype == "table":
                    card =Row([
                            Image(
                                src=image_path,
                                border_radius=border_radius.all(0),
                                tooltip=filename,
                                fit=ImageFit.CONTAIN,
                                width=50,
                                height=50,
                            ),
                            Column([
                                Text(f"{image_metadata.get('Title', '')}"),
                                Text(f"{image_metadata.get('Keywords', '')}"),
                                
                            ]),
                            Divider(),
                        ])
                        

                    ui.controls.append(card)
                    
                    
                
                process_count += 1
                self.progress_bar.value = process_count/(len(os.listdir(directory)))
                self.progress_bar.update()
                    
                image_count += 1  # Increment image count
                self.stat_txt.value = f"Total Images : {image_count}"
                self.stat_txt.update()
        
        
        # Update the label with the image count
        self.right_container.clean()
        self.right_container.content = ui
        self.right_container.update()
    
    def images_display2(self,directory,listtype):

        image_view_thumb = GridView(runs_count=5, max_extent=150, child_aspect_ratio=1.0, spacing=10, cache_extent=20)
        images_display = listtype
        self.right_container.content.clean()

        image_count = 0  # Initialize image count
        process_count = 0  # Initialize image count

        images_select_list = []
        metadata = DataProcessor.read_csv(directory)
        print(images_display)
        if images_display == "thumbnail":
            ui = image_view_thumb
        if images_display == "list":
            ui = ListView(spacing=10,)
        if images_display == "table":
            if not self.processed_data:
                return Text("No data available.")
            # Create header row
            ui = Column(spacing=5, scroll=True)
            
        else : pass
        
        def change_color(e, card, filename):
            if card.color == colors.BLUE:
                card.color = colors.GREY_50
                if filename in images_select_list:
                    images_select_list.remove(filename)
                    print(images_select_list)
            elif card.color == colors.GREY_50:
                card.color = colors.BLUE
                if filename not in images_select_list:
                    images_select_list.append(filename)
                    print(images_select_list)
            card.update()
            self.stat_txt.value = f"Select Images: {len(images_select_list)}/{image_count}"
            self.stat_txt.update()

        def handle_click(e, card, image_path, filename):
            DataProcessor.extract_csv(image_path)
            change_color(e, card, filename)

        for filename in os.listdir(directory):
            if filename.lower().endswith(('.jpg', '.png', '.svg')):
                image_path = os.path.join(directory, filename)
                image_metadata = next((item for item in metadata if item['Filename'] == filename), {})
                
                if images_display == "thumbnail":
                    
                    card = Card(content=
                    Container(content=
                        Stack([
                            Image(
                                src=image_path,
                                border_radius=border_radius.all(0),
                                tooltip=filename,
                                fit=ImageFit.COVER,
                                width=150,
                                height=150,
                            ),
                            Container(content=
                                Container(content=         
                                    Row([
                                        Row([
                                            Icon(name=icons.SELL, size=12),
                                            Text(value="10", size=10,),
                                        ],alignment=MainAxisAlignment.START,
                                        ),    
                                        CircleAvatar(bgcolor=colors.GREY, radius=4),
                                    ],alignment=MainAxisAlignment.SPACE_BETWEEN,
                                    ),bgcolor=colors.GREY_50,opacity=0.5,height=24,
                                    alignment=alignment.bottom_right,margin=0,padding=5,
                                ),
                                alignment=alignment.bottom_center,margin=0,
                            ),
                            Container(
                                alignment=alignment.bottom_right,margin=0,
                                ink=True,padding=padding.only(0),
                                on_click=None,  # Set to None initially
                            ),   
                        ]),margin=3,
                    ),shape=RoundedRectangleBorder(radius=0),margin=0,color = colors.GREY_50
                )
                    # Now set the on_click handler
                    card.content.content.controls[2].on_click = lambda e, card=card, image_path=image_path, filename=filename: handle_click(e, card, image_path, filename)
                    ui.controls.append(card)
                    
                if images_display == "list":
                    card = Card(content=
                    Container(content=
                        Stack([
                            Image(
                                src=image_path,
                                border_radius=border_radius.all(0),
                                tooltip=filename,
                                fit=ImageFit.COVER,
                                width=100,
                                height=100,
                            ),
                            Container(content=
                                Container(content=         
                                    Row([
                                        Row([
                                            Icon(name=icons.SELL, size=12),
                                            Text(value="10", size=10,),
                                        ],alignment=MainAxisAlignment.START,
                                        ),    
                                        CircleAvatar(bgcolor=colors.GREY, radius=4),
                                    ],alignment=MainAxisAlignment.SPACE_BETWEEN,
                                    ),bgcolor=colors.GREY_50,opacity=0.5,height=24,
                                    alignment=alignment.bottom_right,margin=0,padding=5,
                                ),
                                alignment=alignment.bottom_center,margin=0,
                            ),
                            Container(
                                alignment=alignment.bottom_right,margin=0,
                                ink=True,padding=padding.only(0),
                                on_click=None,  # Set to None initially
                            ),   
                        ]),margin=3,
                    ),shape=RoundedRectangleBorder(radius=0),
                    margin=0,color = colors.GREY_50,
                    width=100, height=100,
                )
                    # Now set the on_click handler
                    card.content.content.controls[2].on_click = lambda e, card=card, image_path=image_path, filename=filename: handle_click(e, card, image_path, filename)
                    
                    category = image_metadata.get('Category')

                    if category is not None and category > 0:
                        image_category = self.adobe_categories_list[int(category) - 1]
                    else:
                        image_category = "Selected Category"
                                        
                    print(image_metadata)
                        

                    right_con=Column([
                        
                        Dropdown(
                            label=None,
                            options=[dropdown.Option(key=f"{category}") for index, category in enumerate(self.adobe_categories_list)],
                            hint_text=f"{image_category}",
                            on_change=EventHandler.on_change_category_dropdown
                        ),
                    
                        TextField(
                            label=("Title"),
                            value=(f"{image_metadata.get('Title', '')}"),
                            color=colors.BLUE_700,
                            ),
                            
                        TextField(
                            label="Keywords", 
                            value=(f"{image_metadata.get('Keywords', '')}"),
                            min_lines=1,
                            max_lines=3, 
                            multiline=True,
                            color=colors.BLUE_700,
                        ),
                        Row([
                            Icon(name=icons.PERSON_PIN),
                            Text((f"{image_metadata.get('Releases', '')}"))]),
                            ],
                            expand=True,
                        )
                    row_con=Row([
                        card,
                        right_con,
                        ],
                        alignment=MainAxisAlignment.START,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                        expand=True,
                    )

                    ui.controls.append(row_con)
                    ui.controls.append(Divider(height=9,),)
                
                if images_display == "table":
                    card = ListTile(
                        leading=Image(
                                src=image_path,
                                border_radius=border_radius.all(0),
                                tooltip=filename,
                                fit=ImageFit.COVER,
                                width=50,
                                height=50,
                            ),
                        title=Text(f"{image_metadata.get('Title', '')}"),
                        subtitle=Text(f"{image_metadata.get('Keywords', '')}"),
                        dense=True,
                    )
                    ui.controls.append(card)
                    
                    
                else : pass
                process_count += 1
                self.progress_bar.value = process_count/(len(os.listdir(directory)))
                self.progress_bar.update()
                    
                image_count += 1  # Increment image count
                self.stat_txt.value = f"Total Images : {image_count}"
                self.stat_txt.update()
        
        
        # Update the label with the image count
        self.right_container.clean()
        self.right_container.content = ui
        self.right_container.update()

    def list_change(self,listtype_current):
        listtype=listtype_current
        CheckProcess.check_path(path)
        print(CheckProcess.check_path(path))
        if CheckProcess.check_path(path) == False : 
            self.get_directory_dialog
        else : self.images_display(path, listtype)
        print(listtype)

    def list_view(self, btt, listtype_current):
        icons = btt.icon.upper()
        print(f"old {icons}")
        if icons.endswith("_OUTLINED"):
            icons = icons.replace("_OUTLINED", "")
            print(f"new1 {icons}")
        else:
            icons = icons
            print(f"new2 {icons}")
        btt.icon = icons
        btt.update()
        
        for button in self.view_btt_list:
            if button != btt:
                button_icon = button.icon.upper()
                if button_icon.endswith("_OUTLINED"):
                    button.icon = button.icon
                else:
                    button.icon = button.icon + "_OUTLINED"
                button.update()

        self.list_change(listtype_current)

    