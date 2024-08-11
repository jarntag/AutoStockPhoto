import flet as ft
from utils import process_image, call_gemini_api, create_csv, generate_keywords_and_title

# ... (โค้ดสร้างอินเทอร์เฟซด้วย Flet)

def main(page: ft.Page): pass
    # ... (โค้ดสำหรับจัดการเหตุการณ์ต่างๆ)
    # เช่น เมื่อผู้ใช้อัปโหลดไฟล์, กดปุ่มสร้าง CSV

    # ส่วนหลักของโปรแกรม
if __name__ == "__main__":
    image_path = "path/to/your/image.jpg"
    category = "Your Category"
    releases = "Your Releases"
    description = "Your Description"

    # ประมวลผลภาพ
    processed_image = process_image(image_path)

    # สร้าง Keyword และ Title
    keywords, title = generate_keywords_and_title(processed_image)

    # สร้างไฟล์ CSV
    create_csv("output.csv", title, keywords, category, releases, description)

ft.app(target=main)