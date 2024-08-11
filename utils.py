import cv2
import requests
import configparser
import csv
import openai
import os
from dotenv import load_dotenv

# ฟังก์ชันสำหรับประมวลผลภาพ
def process_image(image_path): 
    # ... (โค้ดสำหรับประมวลผลภาพ)
    img = cv2.imread(image_path)
    # ประมวลผลภาพ (เช่น upscale, resize)
    # ...
    return img

# อ่าน API Key จากไฟล์ config


load_dotenv()  # Load environment variables from .env file
openai.api_key = os.getenv('OPENAI_API_KEY')

# ฟังก์ชันสำหรับเรียก Gemini API
def call_gemini_api(prompt):
    config = configparser.ConfigParser()
    config.read('config.ini')
    api_key = config['API']['gemini_api_key']
    url = "https://api.openai.com/v1/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": "text-davinci-003",
        "prompt": prompt,
        "max_tokens": 150,  # Adjust based on desired keyword/title length
        "n": 1,
        "stop": None,
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data["choices"][0]["text"].strip()
    else:
        raise Exception(f"API call failed with status code: {response.status_code}")

# Function to create CSV data dictionary
def create_csv_data(filename, title, keywords, category, releases, description):
  return {
      "Filename": filename,
      "Title": title,
      "Keywords": keywords,
      "Category": category,
      "Releases": releases,
      "Description": description
  }

# ฟังก์ชันสำหรับสร้างไฟล์ CSV
def create_csv(data, filepath):
  with open(filepath, 'w', newline='') as csvfile:
    fieldnames = data.keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow(data) 


def generate_keywords_and_title(image):
    # สร้าง prompt สำหรับส่งไปยัง OpenAI
    prompt = f"Generate keywords and a descriptive title for this image: {image}"

    # ส่ง prompt ไปยัง OpenAI
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7
    )

    # ดึงผลลัพธ์
    keywords_and_title = response.choices[0].text.split('\n')
    return keywords_and_title    