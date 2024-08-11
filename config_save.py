import configparser

def serialize_image_data(image_data):
    """Convert a dictionary to a serialized string format."""
    return '|'.join([f"{key}:{value}" for key, value in image_data.items()])

def deserialize_image_data(data_str):
    """Convert a serialized string format back to a dictionary."""
    return {item.split(':')[0]: item.split(':')[1] for item in data_str.split('|')}

# Create configuration object
config = configparser.ConfigParser()

# Add sections and settings
config['DEFAULT'] = {
    'Theme': 'LIGHT',
    'SavePath': 'save/sample_images.csv',
    'ImagesPerPrompt': '4',
    'PrefixPrompt': '',
    'MainPrompt': 'Africa\nAlgeria\nAngola\nBenin',
    'EnhancePrompt': '',
    'SubfixPrompt': '',
    'MainKeywords': '',
    'AdobeCategories': ', '.join([
        "Animals", "Buildings and Architecture", "Business", "Drinks", "The Environment", 
        "States of Mind", "Food", "Graphic Resources", "Hobbies and Leisure", "Industry", 
        "Landscape", "Lifestyle", "People", "Plants and Flowers", "Culture and Religion", 
        "Science", "Social Issues", "Sports", "Technology", "Transport", "Travel"
    ]),
    'imagedata': serialize_image_data({
        "Filename": "image1.jpg",
        "Title": "Beautiful Sunset",
        "Keywords": "sunset, nature, beauty",
        "Category": "Nature",
        "Releases": "2024-07-18"
    },),
}
config['USER'] = {
    'Theme': 'LIGHT',
    'SavePath': 'save/sample_images.csv',
    'ImagesPerPrompt': '4',
    'PrefixPrompt': '',
    'MainPrompt': 'Africa\nAlgeria\nAngola\nBenin',
    'EnhancePrompt': '',
    'SubfixPrompt': '',
    'MainKeywords': '',
    'AdobeCategories': ', '.join([
        "Animals", "Buildings and Architecture", "Business", "Drinks", "The Environment", 
        "States of Mind", "Food", "Graphic Resources", "Hobbies and Leisure", "Industry", 
        "Landscape", "Lifestyle", "People", "Plants and Flowers", "Culture and Religion", 
        "Science", "Social Issues", "Sports", "Technology", "Transport", "Travel"
    ]),
    'imagedata': serialize_image_data({
        "Filename": "image1.jpg",
        "Title": "Beautiful Sunset",
        "Keywords": "sunset, nature, beauty",
        "Category": "Nature",
        "Releases": "2024-07-18"
    },),
}

# Save the configuration to an INI file
with open('config.ini', 'w') as configfile:
    config.write(configfile)

print("Configuration saved to 'config.ini'")
