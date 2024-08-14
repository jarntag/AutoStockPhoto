

from flet import (
    app,
    Page,
    MainAxisAlignment,
    CrossAxisAlignment,
    ElevatedButton,
    icons,
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
    Slider,
    Divider,
    )

from realesrgan import RealESRGANer
import warnings
import torch

# Suppress the FutureWarning related to torch.load
warnings.filterwarnings("ignore", category=FutureWarning)

def load_model(model_path):
    try:
        loadnet = torch.load(model_path, map_location=torch.device('cpu'))
        return loadnet
    except Exception as ex:
        raise ValueError(f"Failed to load model state_dict: {ex}")

def upscale_image(model_name, image_path):
    # Initialize the correct model
    model = None
    if model_name == "REALESRGAN-X4PLUS":
        model = RealESRGANer(
                scale=4,
                model_path="models/RealESRGAN_x4plus.pth",
                dni_weight=None,
                model="RealESRGAN_x4plus",
                tile=0,
                tile_pad=10,
                pre_pad=10,
                half=False,
                device=None,
                gpu_id=None)
    elif model_name == "REALESRGAN-X4FAST":
        model = RealESRGANer(model_name="RealESRGAN_x4fast")
    elif model_name == "REMACRI":
        model = RealESRGANer(model_name="REMACRI")
    elif model_name == "ULTRAMIX_BALANCED":
        model = RealESRGANer(model_name="UltraMix_Balanced")
    elif model_name == "ULTRASHARP":
        model = RealESRGANer(model_name="UltraSharp")
    elif model_name == "REALESRGAN-X4PLUS-ANIME":
        model = RealESRGANer(model_name="RealESRGAN_x4plus_anime")
    
    # Load and upscale the image
    upscaled_image = model.process(image_path)
    return upscaled_image

def main(page: Page):
    page.title = "Image Upscaler"
    page.vertical_alignment = MainAxisAlignment.START
    page.horizontal_alignment = CrossAxisAlignment.CENTER

    input_image = Image(width=300, height=300, fit=ImageFit.CONTAIN)
    output_image = Image(width=300, height=300, fit=ImageFit.CONTAIN)

    scale_slider = Slider(min=2, max=4, value=4, label="Scale")
    denoise_slider = Slider(min=0, max=1, value=0.5, label="Denoise Strength")
    upscale_button = ElevatedButton(text="Upscale", on_click=lambda e: upscale_image(model_dropdown.value, input_image, scale_slider.value, denoise_slider.value))

    def on_file_picked(e: FilePickerResultEvent):
        if e.files:
            input_image.src = e.files[0].path
            page.update()

    # สร้าง UI components
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
        upscaled_image = upscale_image(model_name, image_path)
        # Save or display upscaled_image
        # (Implement saving or displaying the image here)        
    
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
                Divider(),

                scale_slider,
                denoise_slider,
                

            
                
            ]
        )
    )

app(target=main)
