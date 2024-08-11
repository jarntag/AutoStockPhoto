import configparser
import os
import pandas as pd

class DataProcessor:

    def __init__(self):
            pass
    
    def process_image_data(self, image_data):
        # Placeholder for data processing logic
        # This is where you'll implement:
        # - Extracting metadata from image files (if necessary)
        # - Processing existing metadata (e.g., cleaning, categorizing)
        # - Generating keywords based on image content or metadata
        # - Updating image data with processed information

        # Example:
        processed_data = []
        for image in image_data:
            # Extract metadata or process existing data
            processed_image = {
                "Filename": image["Filename"],
                "Title": image.get("Title", ""),
                "Keywords": image.get("Keywords", ""),
                "Category": image.get("Category", ""),
                "Releases": image.get("Releases", ""),
            }
            processed_data.append(processed_image)
        return processed_data
    
    def read_config(config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        global adobe_categories_list
        # Access configuration values
        default_theme = config.get('DEFAULT', 'theme')
        default_savepath = config.get('DEFAULT', 'savepath')
        default_images_per_prompt = config.get('DEFAULT', 'ImagesPerPrompt')
        default_prefix_prompt = config.get('DEFAULT', 'PrefixPrompt')
        default_main_prompt = config.get('DEFAULT', 'MainPrompt')
        default_subfix_prompt = config.get('DEFAULT', 'SubfixPrompt')
        default_main_keywords = config.get('DEFAULT', 'MainKeywords')
        default_categories = config.get('DEFAULT', 'SelectCategories')
        default_adobe_categories_str = config.get('DEFAULT', 'AdobeCategories')
        default_adobe_categories_list = DataProcessor.convert_to_list(default_adobe_categories_str)
        default_image_data_str = config.get('DEFAULT', 'ImageData')
        default_image_data = DataProcessor.deserialize_image_data(default_image_data_str)
        default_images_display = config.get('DEFAULT', 'imagesdisplay')
        default_defaultpath = config.get('DEFAULT', 'defaultpath')

        # Access user-specific configurations
        theme = config.get('USER', 'theme', fallback=default_theme)
        savepath = config.get('USER', 'savepath', fallback=default_savepath)
        images_per_prompt = config.get('USER', 'ImagesPerPrompt', fallback=default_images_per_prompt)
        prefix_prompt = config.get('USER', 'PrefixPrompt', fallback= default_prefix_prompt)
        main_prompt = config.get('USER', 'MainPrompt', fallback=default_main_prompt)
        subfix_prompt = config.get('USER', 'SubfixPrompt', fallback=default_subfix_prompt)
        main_keywords = config.get('USER', 'MainKeywords', fallback=default_main_keywords)
        categories = config.get('USER', 'SelectCategories', fallback=default_categories)
        adobe_categories_str = config.get('USER', 'AdobeCategories', fallback=default_adobe_categories_str)
        adobe_categories_list = DataProcessor.convert_to_list(adobe_categories_str)
        image_data_str = config.get('USER', 'ImageData', fallback=default_image_data_str)
        image_data = DataProcessor.deserialize_image_data(image_data_str)
        images_display = config.get('USER', 'imagesdisplay', fallback=default_images_display)
        defaultpath = config.get('USER', 'defaultpath', fallback=default_defaultpath)

        categories_index = int(categories)

        return {
            'theme': theme,
            'savepath': savepath,
            'ImagesPerPrompt': images_per_prompt,
            'PrefixPrompt': prefix_prompt,
            'MainPrompt': main_prompt,
            'SubfixPrompt': subfix_prompt,
            'MainKeywords': main_keywords,
            'SelectCategories': categories_index,
            'adobe_categories_list': adobe_categories_list,
            'ImageData': image_data,
            'imagesdisplay': images_display,
            'defaultpath': defaultpath,
        }
    
    def serialize_image_data(image_data):
        # Convert a list of dictionaries to a serialized string format.
        return '|'.join([f"{key}:{value}" for key, value in image_data.items()])

    def deserialize_image_data(data_str):
        # Convert a serialized string format back to a list of dictionaries.
        return {item.split(':')[0]: item.split(':')[1] for item in data_str.split('|')}

    def convert_to_list(categories_str):
        # Convert a comma-separated string to a list.
        return [item.strip() for item in categories_str.split(',')]

    def convert_to_string(categories_list):
        # Convert a list to a comma-separated string.
        return ', '.join(categories_list)
    
    def main_prompt_process(main_prompt): 
        main_prompt_list = [line.strip() for line in main_prompt.strip().split('\n') if line.strip()]
        return main_prompt_list
    
    def keywords_process(main_keywords_txf): 
        keywords_list = main_keywords_txf.value.replace("\n", ", ").replace(", ", ",").split(",")
        main_keywords = main_keywords_txf.value.replace("\n", "; ").replace(", ", "; ").split(",")
        return keywords_list,main_keywords
    
    # Function to read CSV and return metadata
    def read_csv(directory):
        # Extract folder name from directory path
        folder_name = os.path.basename(os.path.normpath(directory))
        # Save all data to CSV file with folder name as the file name
        csv_file_path = os.path.join(directory, f"{folder_name}.csv")
        try:
            df = pd.read_csv(csv_file_path)
            metadata_list = df.to_dict(orient='records')
            return metadata_list
        except FileNotFoundError:
            print(f"File '{csv_file_path}' not found. Creating a new file.")
            # Create a new empty DataFrame with specified columns and save it as a CSV file
            all_data = []  # List to store all data
            images = sorted([f for f in os.listdir(directory) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
            for image in images:
                data = {
                    "Filename": image,
                    "Title": "",
                    "Keywords": "",
                    "Category": 0,
                    "Releases": "",
                }
                all_data.append(data)  # Append new data to the list
            df = pd.DataFrame(all_data)
            df.to_csv(csv_file_path, index=False)
            df = pd.read_csv(csv_file_path)
            metadata_list = df.to_dict(orient='records')
            return metadata_list
        
    def extract_csv(image_path):
        
        return None, None
    
    def embed_metadata(path_txt, images_per_prompt, prefix_prompt_txf, main_prompt_txf, subfix_prompt_txf, main_keywords_txf, category_dropdown, stat_txt, progress_bar):
        path=path_txt.value
        main_prompt = main_prompt_txf.value
        images = sorted([f for f in os.listdir(path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
        num = int(images_per_prompt.value)
        process_count = 0  # Initialize image count

        main_prompt_list = DataProcessor.main_prompt_process(main_prompt)
        total_prompt = len(main_prompt_list)
        keywords_list,main_keywords = DataProcessor.keywords_process(main_keywords_txf)

        all_data = []  # List to store all data

        for i, prompt in enumerate(main_prompt_list):
            start_index = i * num
            end_index = start_index + num
            prompt_images = images[start_index:end_index]

            for j, image_file in enumerate(prompt_images):
                image_path = os.path.join(path, image_file)

                title = f"{prefix_prompt_txf.value} {prompt} {subfix_prompt_txf.value}"
                prompt=prompt.replace("\n", " ").replace("'", "")

                # Prepare prompt key
                prompt_words = [word.rstrip('.,!?') for word in prompt.lower().split() if len(word) > 2]

                # Initialize seen set with the correct syntax
                seen = {'the', 'out', 'up', 'with'}
                seen.update(keywords_list)
                unique_words = []

                for word in prompt_words:
                    if word not in seen:
                        unique_words.append(word)
                        seen.add(word)
                prompt_keyp = ', '.join(unique_words)

                keywords = f"{prompt_keyp}, {', '.join(keywords_list)},".rstrip(', ')

                category = category_dropdown.value
                selected_index = adobe_categories_list.index(category)+1  # Adjust to zero-indexed

                data = {
                    "Filename": image_file,
                    "Title": title,
                    "Keywords": keywords,
                    "Category": selected_index,
                    "Releases": None,
                }

                all_data.append(data)  # Append new data to the list

                process_count += 1
                stat_txt.value = f"Total process Images : {process_count}"
                stat_txt.update()
                
                progress_bar.value = process_count/(total_prompt*num)
                progress_bar.update()
                print(keywords)
        
         # Extract folder name from directory path
        folder_name = os.path.basename(os.path.normpath(path))

        # Save all data to CSV file with folder name as the file name
        csv_file_path = os.path.join(path, f"{folder_name}.csv")
        df = pd.DataFrame(all_data)
        df.to_csv(csv_file_path, index=False)
        print(f"CSV file saved in folder: {csv_file_path}")

        print(main_prompt_list,len(main_prompt_list))
        stat_txt.value = f"Total process Images : {process_count}"
        stat_txt.update()
        

     