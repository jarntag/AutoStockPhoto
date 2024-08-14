from flet import (
    app,
    Page,
)
from ui import UIBuilder

def main(page: Page):
    Page.window_width = 1000
    Page.window_height = 600
    page.title = "AutoStockPhoto"
    page.padding = 4
    page.window.title_bar_hidden = True
    page.window.title_bar_buttons_hidden = True
    #page.bgcolor=colors.RED,
    
    # Create an instance of AppUi
    app_ui = UIBuilder(page)
    ui = app_ui.build_ui()

    
    # hide all dialogs in overlay
    page.overlay.extend([ app_ui.get_directory_dialog, app_ui.get_txt_prompt, app_ui.get_txt_keyword, ])

    page.add(ui)
    

    
app(target=main)
