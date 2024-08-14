import warnings
import torch
from PIL import Image as PILImage
from realesrgan import RealESRGANer
from flet import (
    app,
    Page,
    MainAxisAlignment,
    CrossAxisAlignment,
    ElevatedButton,
    FilePickerFileType,
    FilePicker,
    FilePickerResultEvent,
    Dropdown,
    dropdown,
    TextButton,
    Column,
    Text,
    Image,
    ImageFit,
    Row,
)

# Suppress the FutureWarning related to torch.load
warnings.filterwarnings("ignore", category=FutureWarning)

def load_model(model_path):
    try:
        loadnet = torch.load(model_path, map_location=torch.device('cpu'))
        return loadnet
    except Exception as ex:
        raise ValueError(f"Failed to load model state_dict: {ex}")

def upscale_image(model_name, image_path):
    # Initialize the correct model path
    model_path = None

    if model_name == "REALESRGAN-X4PLUS":
        model_path = "models/RealESRGAN_x4plus.pth"
    elif model_name == "REALESRGAN-X4FAST":
        model_path = "models/RealESRGAN_x4fast.pth"
    # Add paths for other models as necessary

    if model_path:
        # Load the model
        model = RealESRGANer(
            scale=4,
            model_path=model_path,
            dni_weight=None,
            model="RealESRGAN_x4plus",
            tile=0,
            tile_pad=10,
            pre_pad=10,
            half=False,
            device=None,
            gpu_id=None
        )

        # Load and upscale the image
        img = PILImage.open(image_path).convert("RGB")
        upscaled_image, _ = model.enhance(img)
        return upscaled_image
    else:
        raise ValueError("Model path not set.")

def main(page: Page):
    page.title = "Image Upscaler"
    page.vertical_alignment = MainAxisAlignment.START
    page.horizontal_alignment = CrossAxisAlignment.CENTER

    input_image = Image(width=300, height=300, fit=ImageFit.CONTAIN)
    output_image = Image(width=300, height=300, fit=ImageFit.CONTAIN)

    def on_file_picked(e: FilePickerResultEvent):
        if e.files:
            input_image.src = e.files[0].path
            page.update()

    # Create UI components
    file_picker = FilePicker(on_result=on_file_picked)
    page.overlay.append(file_picker)

    model_dropdown = Dropdown(
        options=[
            dropdown.Option("REALESRGAN-X4PLUS"),
            dropdown.Option("REALESRGAN-X4FAST"),
            dropdown.Option("REMACRI"),
            dropdown.Option("ULTRAMIX_BALANCED"),
            dropdown.Option("ULTRASHARP"),
            dropdown.Option("REALESRGAN-X4PLUS-ANIME"),
        ]
    )

    def on_upscale(e):
        model_name = model_dropdown.value
        image_path = input_image.src
        if image_path and model_name:
            try:
                upscaled_image = upscale_image(model_name, image_path)
                upscaled_image.save("upscaled_image.png")  # Save the upscaled image
                output_image.src = "upscaled_image.png"
                page.update()
            except Exception as ex:
                print(f"Error during upscaling: {ex}")

    upscale_button = TextButton("Upscale Image", on_click=on_upscale)

    page.add(
        Column(
            [
                Text("Select Model:"),
                model_dropdown,
                Text("Select Image:"),
                Row([ElevatedButton("Choose file", on_click=lambda _: file_picker.pick_files(file_type=FilePickerFileType.IMAGE,))]),
                input_image,
                output_image,
                upscale_button,
            ]
        )
    )

app(target=main)
