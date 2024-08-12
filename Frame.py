import flet as ft

# Container to hold image components
image_container = ft.GridView( 
    runs_count=5, 
    max_extent=150,
    child_aspect_ratio=1.0, 
    spacing=10,
)
image_container2 = ft.ListView(  
    spacing=10,
)

right_container = ft.Container(
        bgcolor=ft.colors.BROWN_400,
        alignment=ft.alignment.center,
        width=300,  # Start width, adjusted according to total width
        expand=False,
        content=image_container2
    )

main_container = ft.Container(
    content=image_container,
    bgcolor=ft.colors.ORANGE_300,
    alignment=ft.alignment.center,
    width=700,
    expand=True,
        
)

# Text widget to display the selected directory path
directory_path = ft.Text("Select images directory path first! ")
csv_file_path = ft.TextField(label="CSV File Path")
prefix_prompt = ft.TextField(label="Prefix prompt", value="",
    min_lines=1,max_lines=2, multiline=True,color=ft.colors.BLUE_700,)
suffix_prompt = ft.TextField(label="suffix prompt", value=", ultra realistic, candid, social media, avatar image, plain solid background",
    min_lines=1,max_lines=2, multiline=True,color=ft.colors.BLUE_700,)
main_prompt = ft.TextField(label="Main prompt matrix List", value="",
    min_lines=1,max_lines=5, multiline=True,color=ft.colors.BLUE_700,)
enhance_prompt = ft.TextField(label="Enhance prompt matrix List", value="",
    min_lines=1,max_lines=2, multiline=True,color=ft.colors.BLUE_700,)
main_keywords = ft.TextField(label="Keywords", value="line1\nline2",
    min_lines=2,max_lines=5, multiline=True,color=ft.colors.BLUE_700,)
image_title = ft.TextField(label="Title")
image_metadata = ft.Text("Metadata")
image_keywords = ft.TextField(label="Keywords", value="",
    min_lines=2,max_lines=3, multiline=True,color=ft.colors.BLUE_700,)

main_prompt_list = ['Africa', 'Algeria', 'Angola', 'Benin',]
keywords_list = []
images_select_list = []
images_per_prompt = ft.TextField(label="images per prompt", value="4",)
progress_bar = ft.ProgressBar(value=0)

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
    page.window_width = 1000
    page.window_height = 600
    page.add(
        ft.Row([ft.Text("Keywords"),ft.Text("Keywords"),],alignment=ft.MainAxisAlignment.SPACE_BETWEEN,),
        progress_bar,
        ft.Row([
            ft.ResponsiveRow([
                ft.Row(controls=[
                    main_container,
                    ft.GestureDetector(
                        content=ft.VerticalDivider(),
                        drag_interval=10,
                        on_pan_update=move_vertical_divider,
                        on_hover=show_draggable_cursor,
                        
                    ),
                    right_container,
            ],
            spacing=0,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    ) ],spacing=10,
            expand=True,), 
        ],spacing=10,
            expand=True,), 


        image_metadata,             
        image_title,
        image_keywords,

        ft.Row([]),        
        ft.Row([]),
    )

    for i in range(0, 60):
        image_container.controls.append(
            ft.Card(content=
                ft.Container(content=
                    ft.Stack([
                        ft.Image(
                            src=f"https://picsum.photos/150/150?{i}",
                            fit=ft.ImageFit.NONE,
                            repeat=ft.ImageRepeat.NO_REPEAT,
                            border_radius=ft.border_radius.all(0),
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
                            on_click=lambda e, image_path="uploads\\aa.jpg", : extract_metadata(image_path),
                        ),
  
                    ]),margin=5,
                ),shape=ft.RoundedRectangleBorder(radius=0),margin=0,color=ft.colors.GREEN,
            )
        )
    
    for i in range(0, 60):
        image_container2.controls.append(ft.Text(f"Line"))

    page.update()

ft.app(target=main)