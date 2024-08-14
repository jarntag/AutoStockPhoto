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
    )
from realesrgan import RealESRGANer
import os
from basicsr.archs.rrdbnet_arch import RRDBNet
import numpy as np
from PIL import Image as Imagepil



def get_model_files():
    model_dir = "models"
    model_files = [f for f in os.listdir(model_dir) if f.endswith('.pth')]
    return [os.path.splitext(f)[0] for f in model_files]





def main(page: Page):
    page.title = "Image Upscaler"
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER




    input_image = Image(width=300, height=300, fit=ImageFit.CONTAIN)
    output_image = Image(width=300, height=300, fit=ImageFit.CONTAIN)

    def on_file_picked(e: FilePickerResultEvent):
        if e.files:
            input_image.src = e.files[0].path
            page.update()

    # สร้าง UI components
    file_picker = FilePicker(on_result=on_file_picked)
    page.overlay.append(file_picker)

    model_files = get_model_files()
    model_dropdown = Dropdown(
        options=[dropdown.Option(model) for model in model_files],
        width=200,
    )

    def upscale_image(e):
        if not input_image.src or not model_dropdown.value:
            return

        model_name = model_dropdown.value
        model_path = f"models/{model_name}.pth"

        if "x4plus" in model_name.lower() or "x4fast" in model_name.lower():
            model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
        else:
            pass
        upsampler = RealESRGANer(
            scale=4,
            model_path=model_path,
            model=model,
            tile=0,
            tile_pad=10,
            pre_pad=0,
            half=True
        )

        img = Imagepil.open(input_image.src)
        img_np = np.array(img)

        output, _ = upsampler.enhance(img_np)

        output_img = Imagepil.fromarray(output)
        output_path = "output.png"
        output_img.save(output_path)

        output_image.src = output_path
        page.update()

    upscale_button = ElevatedButton("Upscale", on_click=upscale_image)

    # จัดวาง UI
    page.add(
        Row([ElevatedButton("Choose file", on_click=lambda _: file_picker.pick_files())]),
        Row([input_image, output_image]),
        Row([model_dropdown]),
        Row([upscale_button])
    )

app(target=main)