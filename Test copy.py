import flet 
from flet import icons


def main(page: Page):
    page.window_max_height = 520
    page.window_max_width = 400
    page.window_frameless = True
    page.spacing = 0
    page.padding = 0
    # DETECT WIDTH
    widthsrc = page.window_width

    def maximize_win(e):
        # docs: https://flet.dev/docs/controls/page#window_maximized
        page.window_maximized = True
        page.update()

    page.add(
        ResponsiveRow([
            WindowDragArea(
                Container(
                    width=widthsrc,
                    bgcolor="blue",
                    padding=15,
                    content=Row([
                        Text("MyHome", size=30, color="white"),
                        Container(content=Row([
                            IconButton(icons.CHECK_BOX_OUTLINE_BLANK, icon_color="white",
                                       on_click=maximize_win),
                            IconButton(icons.CLOSE, icon_color="white",
                                       on_click=lambda e: page.window_close()),
                        ]))
                    ], alignment="spaceBetween")
                ),
            )
        ])
    )

flet.app(target=main)