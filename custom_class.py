from flet import (
    icons,
    colors,
    Text,
    Card,
    Container,
    Stack,
    Image,
    alignment,
    ImageFit,
    Row,
    CircleAvatar,
    padding,
    RoundedRectangleBorder,
    Icon,
    MainAxisAlignment,
    border_radius,
    Column,
    Dropdown,
    TextField,
    dropdown,
    CrossAxisAlignment,
)
class ImageCard(Card):
    def __init__(self, image_path, filename, keywordlen, checkcolor):
        super().__init__(
            content=Container(
                content=Stack([
                    Image(
                        src=image_path,
                        border_radius=border_radius.all(0),
                        tooltip=filename,
                        fit=ImageFit.COVER,
                        width=150,
                        height=150,
                    ),
                    Container(
                        content=Container(
                            content=Row([
                                Row([
                                    Icon(name=icons.LABEL, size=12),
                                    Text(value=keywordlen, size=10),
                                    ], alignment=MainAxisAlignment.START,
                                ),
                                CircleAvatar(bgcolor=checkcolor, radius=4),
                                ], alignment=MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            bgcolor=colors.GREY_50,
                            opacity=0.5,
                            height=24,
                            alignment=alignment.bottom_right,
                            margin=0,
                            padding=5,
                        ),
                        alignment=alignment.bottom_center,
                        margin=0,
                        opacity=0.5,
                    ),
                    Container(
                        alignment=alignment.bottom_right,
                        margin=0,
                        ink=True,
                        padding=padding.only(0),
                        on_click=None,  # Set to None initially
                    ),
                    ],
                ),
                margin=3,
            ),
            shape=RoundedRectangleBorder(radius=0),
            margin=0,
            #color=colors.GREY_50,
        )

class ImageCardList(Card):
    def __init__(self, image_path, filename, keywordlen, checkcolor, image_metadata, adobe_categories_list):
        # Extracting metadata for display
        category = image_metadata.get('Category')
        if category is not None and category > 0:
            image_category = adobe_categories_list[int(category) - 1]
        else:
            image_category = "Selected Category"

        # Create the card content
        card_content = Container(
            content=Stack([
                Image(
                    src=image_path,
                    border_radius=RoundedRectangleBorder(radius=0),
                    tooltip=filename,
                    fit=ImageFit.COVER,
                    width=100,
                    height=100,
                ),
                Container(
                    content=Container(
                        content=Row([
                            Row([
                                Icon(name=icons.SELL, size=12),
                                Text(value="10", size=10),
                            ], alignment=MainAxisAlignment.START),
                            CircleAvatar(bgcolor=colors.GREY, radius=4),
                        ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                        bgcolor=colors.GREY_50,
                        opacity=0.5,
                        height=24,
                        alignment=alignment.bottom_right,
                        margin=0,
                        padding=5,
                    ),
                    alignment=alignment.bottom_center,
                    margin=0,
                ),
                Container(
                    alignment=alignment.bottom_right,
                    margin=0,
                    ink=True,
                    padding=padding.only(0),
                    on_click=None,  # Set to None initially
                ),
            ]),
            margin=3,
        )

        # Create the right-side content
        right_content = Column([
            Dropdown(
                label=None,
                options=[dropdown.Option(key=f"{category}") for index, category in enumerate(adobe_categories_list)],
                hint_text=f"{image_category}",
                on_change=self.on_change_category_dropdown
            ),
            TextField(
                label="Title",
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
                Text((f"{image_metadata.get('Releases', '')}")),
            ]),
        ], expand=True)

        # Row container with the card and right-side content
        row_content = Row([
            card_content,
            right_content,
        ], alignment=MainAxisAlignment.START, vertical_alignment=CrossAxisAlignment.CENTER, expand=True)

        # Initialize the Card with content
        super().__init__(
            content=row_content,
            shape=RoundedRectangleBorder(radius=0),
            margin=0,
            color=colors.GREY_50,
            width=100,
            height=100,
        )

        # Set the on_click handler for the container inside the card
        card_content.content.controls[2].on_click = lambda e: self.handle_click(e, image_path, filename)

    def handle_click(self, e, image_path, filename):
        # Your click handling logic
        print(f"Clicked on image {filename} with path {image_path}")

    def on_change_category_dropdown(self, e):
        # Handle the category dropdown change event
        print(f"Category changed to {e.control.value}")