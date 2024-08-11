
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
)
from event_handler import EventHandler

class AppUi(UserControl):

    def __init__(self,):
        super().__init__()
        images_display = "table"

        self.top_menu_open_btt = TextButton("Open Directory", icon=icons.SETTINGS_OUTLINED)
        self.top_menu_stat_txt = Text("stat",)
        self.top_menu_path_txt = Text("path",)
        self.top_menu_row = Row([
            self.top_menu_path_txt, 
            self.top_menu_stat_txt, 
            self.top_menu_open_btt], 
            spacing=0, alignment=MainAxisAlignment.SPACE_BETWEEN,)
        
        self.select_all_btt = IconButton(
            icon=icons.CHECK_BOX_OUTLINED,
            tooltip="Select All",
            on_click=lambda _: EventHandler.select_all())
        
        self.table_view_btt = IconButton(
            icon=(icons.TABLE_ROWS if images_display == "table" else icons.TABLE_ROWS_OUTLINED),
            tooltip="Table View",
            on_click=lambda _: EventHandler.list_view(self.table_view_btt, "table", self.view_btt_list))
        self.thumb_view_btt = IconButton(
            icon=(icons.DATASET if images_display == "thumbnail" else icons.DATASET_OUTLINED),
            tooltip="Thumb View",
            on_click=lambda _: EventHandler.list_view(self.thumb_view_btt, "thumbnail", self.view_btt_list))
        self.list_view_btt = IconButton(
            icon=(icons.BALLOT if images_display == "list" else icons.BALLOT_OUTLINED),
            tooltip="List View",
            on_click=lambda _: EventHandler.list_view(self.list_view_btt, "list", self.view_btt_list))
        self.view_btt_list = [self.table_view_btt, self.thumb_view_btt, self.list_view_btt]
        self.bottom_menu_row = Row([
            self.select_all_btt,
            VerticalDivider(),
            self.table_view_btt, 
            self.thumb_view_btt, 
            self.list_view_btt], 
            spacing=0, alignment=MainAxisAlignment.END,)

        # Container to hold image components
        self.image_content = GridView( 
            runs_count=5, 
            max_extent=150,
            child_aspect_ratio=1.0, 
            spacing=10,
        )
        self.main_content = ListView(  
            spacing=10,
        )

        self.right_container = Container(
            # bgcolor=ft.colors.BROWN_400,
                alignment=alignment.center,
                width=700,  # Start width, adjusted according to total width
                expand=True,
                content=self.top_menu_open_btt,
                padding = 10,
        )
        self.main_container = Container(
            content=self.main_content,
            #bgcolor=ft.colors.ORANGE_300,
            alignment=alignment.center,
            width=300,
            padding = 10,
            expand=False,
        )

        self.toggle_menu_btt = IconButton(icon=icons.MENU,)
        self.images_mass_btt = IconButton(icon=icons.DATASET_OUTLINED)
        self.upscale_btt = IconButton(icon=icons.IMAGE_SEARCH)
        self.remove_bg_btt = IconButton(icon=icons.HIDE_IMAGE)
        self.account_btt = IconButton(icon=icons.ACCOUNT_CIRCLE_OUTLINED)
        self.setting_btt = IconButton(icon=icons.SETTINGS_OUTLINED)

        self.main_menu_top_items = [self.toggle_menu_btt, self.images_mass_btt, self.upscale_btt, self.remove_bg_btt]
        self.main_menu_bottom_items = [self.account_btt, self.setting_btt]
        
        
        

        self.main_col = Column([],expand=True, spacing=0,)
        self.main_ctn = Container(expand=True, padding = 0, margin=0)
        self.main_menu_col = Column([])
        self.main_row = Row([], expand=True, spacing=0,)

    

    def main_menu_icon(self, menu_style):

        def main_menu_toggle(menu_style):
            main_menu_build(menu_style)
            print(menu_style)

        def main_menu_build(menu_style):
            if menu_style == "icon":
                self.toggle_menu_btt = IconButton(icon=icons.MENU, on_click=lambda e: main_menu_toggle("text"))
                self.images_mass_btt = IconButton(icon=icons.DATASET_OUTLINED)
                self.upscale_btt = IconButton(icon=icons.IMAGE_SEARCH)
                self.remove_bg_btt = IconButton(icon=icons.HIDE_IMAGE)
                self.account_btt = IconButton(icon=icons.ACCOUNT_CIRCLE_OUTLINED)
                self.setting_btt = IconButton(icon=icons.SETTINGS_OUTLINED)
            else:
                self.toggle_menu_btt = TextButton("Menu", icon=icons.MENU, on_click=lambda e: main_menu_toggle("icon"))
                self.images_mass_btt = TextButton("Massive Metadata", icon=icons.DATASET_OUTLINED)
                self.upscale_btt = TextButton("Images Upscale", icon=icons.IMAGE_SEARCH)
                self.remove_bg_btt = TextButton("Remove Background", icon=icons.HIDE_IMAGE)
                self.account_btt = TextButton("Account", icon=icons.ACCOUNT_CIRCLE_OUTLINED)
                self.setting_btt = TextButton("Setting", icon=icons.SETTINGS_OUTLINED)

            self.main_menu_col = Column([
                self.toggle_menu_btt,
                self.images_mass_btt,
                self.upscale_btt,
                self.remove_bg_btt,
                Column([], expand=True),
                self.account_btt,
                self.setting_btt

            ])
            
            return self.main_menu_col

        return  main_menu_build(menu_style)

    
    def build_ui(self,):
        
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

        # Create UI elements and add them to containers
        self.main_row.controls.append(self.main_menu_col)
        self.main_row.controls.append(self.main_ctn)
        self.main_ctn.content = self.main_col
        self.main_col.controls.append(self.top_menu_row)

        self.top_menu_row.controls.append(self.top_menu_path_txt)
        self.top_menu_row.controls.append(self.top_menu_stat_txt)
        self.top_menu_row.controls.append(self.top_menu_open_btt)


        
        ui = Row([
                self.main_menu_col,
                Container( content=
                    Column([
                        self.top_menu_row,
                        Row([
                                ResponsiveRow([
                                    Row(
                                        controls=[
                                            self.main_container,
                                            GestureDetector(
                                                content=VerticalDivider( color="white"),
                                                drag_interval=10,
                                                on_pan_update=move_vertical_divider,
                                                on_hover=show_draggable_cursor,
                                                ),
                                            self.right_container,
                                        ],
                                        spacing=0,
                                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                                    ) 
                                ],
                                spacing=0,
                                expand=True,
                                ), ], alignment=MainAxisAlignment.START, expand=True, spacing=0,
                            ),
                        Row([
                            IconButton(icon=icons.MENU,),
                            IconButton(icon=icons.MENU,),
                            ], spacing=0, alignment=MainAxisAlignment.END,),       
                        ], 
                        expand=True, spacing=0,
                    ),
                    #bgcolor=colors.RED, 
                    expand=True, padding = 0, margin=0
                ),
            ],
            expand=True,
            spacing=0,
        )
        return ui
    
    def images_display(path, listtype) : pass
    
    