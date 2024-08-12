import configparser

def serialize_image_data(image_data):
    """Convert a dictionary to a serialized string format."""
    return '|'.join([f"{key}:{value}" for key, value in image_data.items()])

def deserialize_image_data(data_str):
    """Convert a serialized string format back to a dictionary."""
    return {item.split(':')[0]: item.split(':')[1] for item in data_str.split('|')}

# Create configuration object
config = configparser.ConfigParser()

# Load configuration from file
config.read('config.ini')

# Access data from the DEFAULT section
app_theme = config['DEFAULT'].get('theme', 'LIGHT')
save_path = config['DEFAULT'].get('savepath', 'default/path')
images_per_prompt = config['DEFAULT'].get('imagesperprompt', '4')
prefix_prompt = config['DEFAULT'].get('prefixprompt', '')
main_prompt = config['DEFAULT'].get('mainprompt', '')
enhance_prompt = config['DEFAULT'].get('enhanceprompt', '')
suffix_prompt = config['DEFAULT'].get('suffixprompt', '')
main_keywords = config['DEFAULT'].get('mainkeywords', '')
adobe_categories = config['DEFAULT'].get('adobecategories', '')
image_data_str = config['DEFAULT'].get('imagedata', '')
image_data = deserialize_image_data(image_data_str)

# Access data from the USER section
app_theme = config['USER'].get('theme', 'LIGHT')
user_save_path = config['USER'].get('savepath', 'default/user/path')
user_images_per_prompt = config['USER'].get('imagesperprompt', '4')
user_prefix_prompt = config['USER'].get('prefixprompt', '')
user_main_prompt = config['USER'].get('mainprompt', '')
user_enhance_prompt = config['USER'].get('enhanceprompt', '')
user_suffix_prompt = config['USER'].get('suffixprompt', '')
user_main_keywords = config['USER'].get('mainkeywords', '')
user_adobe_categories = config['USER'].get('adobecategories', '')
user_image_data_str = config['USER'].get('imagedata', '')
user_image_data = deserialize_image_data(user_image_data_str)

# Print current USER section data
print("Current USER section data:")
print("Save Path:", user_save_path)
print("Images Per Prompt:", user_images_per_prompt)
print("Image Data:", user_image_data)

# Update USER section with new data
def update_user_section():
    config['USER'] = {
        'savepath': 'save/new_user_images.csv',
        'imagesperprompt': '6',
        'prefixprompt': 'Updated User Prompt',
        'mainprompt': 'Updated User Main Prompt',
        'enhanceprompt': 'Updated User Enhance Prompt',
        'suffixprompt': 'Updated User suffix Prompt',
        'mainkeywords': 'Updated User Keywords',
        'adobecategories': 'Updated Category1, Updated Category2',
        'imagedata': serialize_image_data({
            'Filename': 'updated_image.jpg',
            'Title': 'Updated Sunset',
            'Keywords': 'updated sunset, updated nature',
            'Category': 'Updated Nature',
            'Releases': '2024-07-21'
        })
    }

def save_config():
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

# Update user section
update_user_section()

# Save the updated configuration before closing the app
save_config()
