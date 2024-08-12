from flet import (
    icons,
    colors,
    Chip,
    Text,
    FilePickerResultEvent,
    SnackBar,
    ThemeMode,
    )
from data_processor import DataProcessor
import configparser

class EventHandler :
    def __init__(self):
        pass
    
    



    def select_all(btt):
        if btt.icon == icons.CHECK_BOX_OUTLINED:
            btt.icon = icons.CHECK_BOX
        else:
            btt.icon = icons.CHECK_BOX_OUTLINED
        btt.update()
        print(btt.icon) 

    # Create dropdown menu for categories
    def on_change_category_dropdown(e, list):
        category = e.control.value
        selected_index = list.index(category)+1  # Adjust to zero-indexed
        e.control.label="Selected Category"
        print(f"Selected category: {category} (Index: {selected_index})")
        
        e.control.update()  # Ensure the page updates if necessary

        return selected_index    
    
    # Create toggle menu
    def on_toggle_menu(e, list): pass

    def textfield_change(main_title_txt, main_keywords_txt, prefix_prompt_txf, main_prompt_txf, suffix_prompt_txf, main_keywords_txf,) :

        prefix_prompt=prefix_prompt_txf.value
        main_prompt = main_prompt_txf.value
        suffix_prompt = suffix_prompt_txf.value
        max_length_element=0
        main_prompt_list = DataProcessor.main_prompt_process(main_prompt)
        if len(main_prompt_list) == 1 :
            main_title = f"{prefix_prompt} {main_prompt_list[0]} {suffix_prompt}"
            main_title = f"Title : {main_title}" + f" | {len(main_title)}"
        else : 
            max_length_element = max(main_prompt_list, key=len)

            main_title = f"{prefix_prompt} {max_length_element} {suffix_prompt}"
            main_title = f"Title : {prefix_prompt} " + "{" f"{len(main_prompt_list)}" " prompt matrix}" + f" {suffix_prompt}" + f" | {len(main_title)}"

        main_title_txt.value = main_title
        if len(f"{prefix_prompt} {max_length_element} {suffix_prompt}") > 200:
            main_title_txt.color = colors.RED
        else:
            main_title_txt.color = colors.BLUE_700
        main_title_txt.update()
        
        
        keywords_list, main_keywords = DataProcessor.keywords_process(main_keywords_txf)
        main_keywords_txt.value = f"Keywords : {main_keywords}" + f" | {len(keywords_list)}"
        if len(keywords_list) > 49:
            main_keywords_txt.color = colors.RED
        else:
            main_keywords_txt.color = colors.BLUE_700
        main_keywords_txt.update()

    def keywords_selected(keyword, keywords_select_list):
            if keyword in keywords_select_list:
                keywords_select_list.remove(keyword)
                print(keywords_select_list)
            else : 
                keywords_select_list.append(keyword)
                print(keywords_select_list)   

    def keywords_chip_Update(keywords_chip_row, main_keywords_txf, keywords_select_list): 
        keywords_list, main_keywords = DataProcessor.keywords_process(main_keywords_txf)

        if keywords_chip_row is not None:
            keywords_chip_row.controls.clear()
            for keyword in keywords_list:
                chip = (Chip(label=Text(keyword),
                    on_select = lambda e, keyword=keyword, keywords_select_list=keywords_select_list : EventHandler.keywords_selected(keyword, keywords_select_list), selected=True))
                keywords_chip_row.controls.append(chip)
                keywords_select_list.append(keyword)
        keywords_chip_row.update()
        print(keywords_list)
    
    # FilePicker dialog to select and read txt
    def get_prompt_result(e: FilePickerResultEvent, main_title_txt, main_keywords_txt, prefix_prompt_txf, main_prompt_txf, suffix_prompt_txf, main_keywords_txf,):
        if e.files:
            file_path = e.files[0].path
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                    processed_data = content
                    main_prompt_txf.value = processed_data
                    main_prompt_txf.update()
                    EventHandler.textfield_change(main_title_txt, main_keywords_txt, prefix_prompt_txf, main_prompt_txf, suffix_prompt_txf, main_keywords_txf,)
            except Exception as ex:
                print(f"An error occurred while loading the text file: {ex}")
        else:
            print("No file selected")

    # FilePicker dialog to select and read txt
    def get_keywords_result(e: FilePickerResultEvent, main_title_txt, main_keywords_txt, prefix_prompt_txf, main_prompt_txf, suffix_prompt_txf, main_keywords_txf, keywords_chip_row, keywords_select_list):
        if e.files:
            file_path = e.files[0].path
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                    processed_data = content
                    main_keywords_txf.value = processed_data
                    main_keywords_txf.update()
                    EventHandler.textfield_change(main_title_txt, main_keywords_txt, prefix_prompt_txf, main_prompt_txf, suffix_prompt_txf, main_keywords_txf,)
                    EventHandler.keywords_chip_Update(keywords_chip_row, main_keywords_txf, keywords_select_list)
            except Exception as ex:
                print(f"An error occurred while loading the text file: {ex}")
        else:
            print("No file selected")
            
    def on_click(e, click_message, page):
        page.snack_bar = SnackBar(Text(click_message))
        page.snack_bar.open = True
        
        page.overlay.append(SnackBar(Text(click_message)))
        page.update()
        
        # Function to save user data
    def save_user_data(e, click_message, page, theme_switch_csb):
        config = configparser.ConfigParser()
        """config['USER'] = {
            'Theme': ("LIGHT" if theme_switch_csb.selected_index == 0 else "DARK"),
            'SavePath': save_path,
            'ImagesPerPrompt': images_per_prompt_field.value,
            'PrefixPrompt': prefix_prompt_field.value,
            'MainPrompt': main_prompt_field.value,
            'SuffixPrompt': suffix_prompt_field.value,
            'MainKeywords': main_keywords_field.value,
            'SelectCategories': selected_index,
            'ImageData': image_data_str,
        }

        with open('config.ini', 'w') as configfile:
            config.write(configfile)"""
            
        EventHandler.on_click(e, click_message, page)

    def toggle_theme(e, page):
            page.theme_mode = (ThemeMode.LIGHT if e.control.selected_index == 0 else ThemeMode.DARK)
            page.update()    
        
    # Function to be called on app close
    def on_close(self, e):
        print("App is closing...")
        self.save_user_data()  

    def slider_changed(e, txt):
        txt.value = f"{int(e.control.value)}"
        txt.update()    