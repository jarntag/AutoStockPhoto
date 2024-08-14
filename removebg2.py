import flet as ft
from PIL import Image
import numpy as np

def main(page: ft.Page):

    input_image = ft.Image(width=300, height=300, fit=ft.ImageFit.CONTAIN)
    def remove_background(event):
        # รับภาพจาก user
        image = Image.open(f"{input_image.src}")
        # แปลงภาพเป็น numpy array สำหรับประมวลผล
        img_array = np.array(image)
        # ที่นี่คือส่วนที่คุณจะเขียนอัลกอริทึมในการลบพื้นหลัง
        # ตัวอย่างง่ายๆ โดยการตั้งค่าพิกเซลที่เป็นสีขาวให้โปร่งใส
        img_array[np.where((img_array == [255, 255, 255]).all(axis=2))] = [0, 0, 0, 0]
        # แปลงกลับเป็น Image และแสดงผล
        result_image = Image.fromarray(img_array)
        result_image.save("result.png")
        image_result.src = "result.png"
        page.update()

    def on_file_picked(e: ft.FilePickerResultEvent):
        if e.files:
            input_image.src = e.files[0].path
            print(input_image.src)
            page.update()

    file_picker = ft.FilePicker(on_result=on_file_picked)
    button1 = ft.ElevatedButton(text="เลือกภาพ", on_click=file_picker.pick_files)
    image_result = ft.Image(width=200, height=200)
    button = ft.ElevatedButton(text="ลบพื้นหลัง", on_click=remove_background)
    
    page.overlay.append(file_picker)
    page.add(
        button1,
        button,
        input_image,
        image_result,
    )

ft.app(target=main)
