import flet as ft

adobe_categories = [
    "Animals",
    "Buildings and Architecture",
    "Business",
    "Drinks",
    "The Environment",
    "States of Mind",
    "Food",
    "Graphic Resources",
    "Hobbies and Leisure",
    "Industry",
    "Landscape",
    "Lifestyle",
    "People",
    "Plants and Flowers",
    "Culture and Religion",
    "Science",
    "Social Issues",
    "Sports",
    "Technology",
    "Transport",
    "Travel"
]

def main(page: ft.Page):
    page.title = "Adobe Categories Dropdown"

    def on_change_category_dropdown(event):
        selected_index = int(event.control.value.split(" : ")[0])  # Extract index from key
        selected_category = adobe_categories[selected_index]
        print("Selected category:", selected_category)
        print(f"Selected category: {selected_category} (Index: {selected_index})")
        page.update()  # Ensure the page updates if necessary

    # Create dropdown menu for categories
    category_dropdown = ft.Dropdown(
        label="Select Category",
        options=[ft.dropdown.Option(key=f"{str(index)} : {category}") for index, category in enumerate(adobe_categories)],
        on_change=on_change
    )

    page.add(category_dropdown)
ft.app(target=main)
