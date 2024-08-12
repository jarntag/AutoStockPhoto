from flet import (
    app,
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
    padding,
    margin,
    TextButton,
    Page,
    MainAxisAlignment,
    ResponsiveRow,
    GestureDetector,
    VerticalDivider,
    DragUpdateEvent,
    GridView,
    ListView,
    HoverEvent,
    MouseCursor,
    ProgressBar,
    NavigationRailLabelType,
    CircleBorder,
    Icon,
    Card,
    Stack,
    Image,
    ImageFit,
    ImageRepeat,
    CircleAvatar,
    RoundedRectangleBorder,
)

from ui import UIBuilder
# Container to hold image components
image_content = GridView( 
    runs_count=5, 
    max_extent=150,
    child_aspect_ratio=1.0, 
    spacing=10,
)
main_content = ListView(  
    spacing=10,
)

right_container = Container(
       # bgcolor=colors.BROWN_400,
        alignment=alignment.center,
        width=700,  # Start width, adjusted according to total width
        expand=True,
        content=image_content,
        padding = 10,
    )
main_container = Container(
    content=main_content,
    #bgcolor=colors.ORANGE_300,
    alignment=alignment.center,
    width=300,
    padding = 10,
    expand=False,
        
)



# Text widget to display the selected directory path
directory_path = Text("Select images directory path first! ")
csv_file_path = TextField(label="CSV File Path")
prefix_prompt = TextField(label="Prefix prompt", value="",
    min_lines=1,max_lines=2, multiline=True,color=colors.BLUE_700,)
suffix_prompt = TextField(label="suffix prompt", value=", ultra realistic, candid, social media, avatar image, plain solid background",
    min_lines=1,max_lines=2, multiline=True,color=colors.BLUE_700,)
main_prompt = TextField(label="Main prompt matrix List", value="",
    min_lines=1,max_lines=5, multiline=True,color=colors.BLUE_700,)
enhance_prompt = TextField(label="Enhance prompt matrix List", value="",
    min_lines=1,max_lines=2, multiline=True,color=colors.BLUE_700,)
main_keywords = TextField(label="Keywords", value="line1\nline2",
    min_lines=2,max_lines=5, multiline=True,color=colors.BLUE_700,)
image_title = TextField(label="Title")
image_metadata = Text("Metadata")
image_keywords = TextField(label="Keywords", value="",
    min_lines=2,max_lines=3, multiline=True,color=colors.BLUE_700,)

main_prompt_list = ['Africa', 'Algeria', 'Angola', 'Benin',]
keywords_list = []
images_select_list = []
images_per_prompt = TextField(label="images per prompt", value="4",)
progress_bar = ProgressBar(value=0)


rail = NavigationRail(
    selected_index=0,
    label_type=NavigationRailLabelType.NONE,
    #extended=True,
    min_width=56,
    #min_extended_width=400,
    bgcolor=colors.AMBER_500,
    #leading=IconButton(icon=icons.MENU, ),
    group_alignment=-1.0,
    indicator_shape = CircleBorder,
    destinations=[
        NavigationRailDestination(
            icon=icons.FAVORITE_BORDER, selected_icon=icons.FAVORITE, label=""
        ),
        NavigationRailDestination(
            icon_content=Icon(icons.BOOKMARK_BORDER),
            selected_icon_content=Icon(icons.BOOKMARK),
            label="sssss",
        ),
        NavigationRailDestination(
            icon=icons.SETTINGS_OUTLINED,
            selected_icon_content=Icon(icons.SETTINGS),
            label_content=Text("dddd"),
        ),
        Column([], expand=True),
        NavigationRailDestination(
            icon=icons.ACCOUNT_CIRCLE_OUTLINED,
            selected_icon_content=Icon(icons.ACCOUNT_CIRCLE),
            label_content=Text("Account"),
        ),
        NavigationRailDestination(
            icon=icons.SETTINGS_OUTLINED,
            selected_icon_content=Icon(icons.SETTINGS),
            label_content=Text("Setting"),
        ),
    ],
    on_change=lambda e: print("Selected destination:", e.control.selected_index),
)

async def move_vertical_divider(e: DragUpdateEvent):
        new_width = main_container.width + e.delta_x
        if 100 <= new_width <= 900 and 150 <= right_container.width - e.delta_x:
            main_container.width = new_width
            right_container.width -= e.delta_x
            await main_container.update_async()
            await right_container.update_async()

async def show_draggable_cursor(e: HoverEvent):
        e.control.mouse_cursor = MouseCursor.RESIZE_LEFT_RIGHT
        await e.control.update_async()            

def main(page: Page):
    Page.window_width = 1000
    Page.window_height = 600
    page.padding = 8
    #page.bgcolor=colors.RED,
    
    # Create an instance of AppUi
    app_ui = UIBuilder()
    top_menu_row = app_ui.top_menu_row
    main_menu_col = app_ui.main_menu_col
    bottom_menu_row = app_ui.bottom_menu_row
    web_seg_btt = app_ui.web_seg_btt
    theme_btt = app_ui.theme_btt

    page.add(
        Row([
            main_menu_col,
                Container( content=
                    Column([
                        top_menu_row,
                             
                        Row([
                                ResponsiveRow([
                                    Row(
                                        controls=[
                                            main_container,
                                            GestureDetector(
                                                content=VerticalDivider( color="white"),
                                                drag_interval=10,
                                                on_pan_update=move_vertical_divider,
                                                on_hover=show_draggable_cursor,
                                                ),
                                            right_container,
                                        ],
                                        spacing=0,
                                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                                    ) 
                                ],
                                spacing=0,
                                expand=True,
                                ), ], alignment=MainAxisAlignment.START, expand=True, spacing=0,
                            ),
                        bottom_menu_row,
                    ], 
                    expand=True, spacing=0,),
                    #bgcolor=colors.RED, 
                    expand=True, padding = 0, margin=0
                ),
                    
                        
                
                
                
                
            ],
            expand=True,
            spacing=0,
        )
    )
    
    
    for i in range(0, 60):
        image_content.controls.append(
            Card(content=
                Container(content=
                    Stack([
                        Image(
                            src=f"https://picsum.photos/150/150?{i}",
                            fit=ImageFit.NONE,
                            repeat=ImageRepeat.NO_REPEAT,
                            border_radius=border_radius.all(0),
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
                            on_click=lambda e, image_path="uploads\\aa.jpg", : extract_metadata(image_path),
                        ),
  
                    ]),margin=5,
                ),shape=RoundedRectangleBorder(radius=0),margin=0,color=colors.GREEN,
            )
        )
    
    for i in range(0, 1):
        main_content.controls.append(web_seg_btt)
        main_content.controls.append(theme_btt)
        
    
    page.update()
    
app(target=main)
