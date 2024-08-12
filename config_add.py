import configparser
import json

# Create configuration data
config = configparser.ConfigParser()

config['DEFAULT'] = {
    'SavePath': 'save/sample_images.csv',
    'ImagesPerPrompt': '4',
    'PrefixPrompt': '',
    'MainPrompt': 'Africa\nAlgeria\nAngola\nBenin',
    'EnhancePrompt': '',
    'SuffixPrompt': '',
    'MainKeywords': '',
    'AdobeCategories': ', '.join([
        "Animals", "Buildings and Architecture", "Business", "Drinks", "The Environment", 
        "States of Mind", "Food", "Graphic Resources", "Hobbies and Leisure", "Industry", 
        "Landscape", "Lifestyle", "People", "Plants and Flowers", "Culture and Religion", 
        "Science", "Social Issues", "Sports", "Technology", "Transport", "Travel"
    ])
}

# Sample data
data = [
    {
        "Filename": "image1.jpg",
        "Title": "Beautiful Sunset",
        "Keywords": "sunset, nature, beauty",
        "Category": "Nature",
        "Releases": "2024-07-18"
    }
]

# Add image data to DEFAULT section as JSON string
config['DEFAULT']['ImageData'] = json.dumps(data)

# Write configuration to file
with open('config.ini', 'w') as configfile:
    config.write(configfile)

print("Configuration saved to config.ini")
