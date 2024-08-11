
import os
import pandas as pd


class ImageManager:
    def __init__(self, directory,):
        self.directory = directory
        self.image_data = self.load_image_data()

    def load_image_data(self):
        try:
            folder_name = os.path.basename(os.path.normpath(self.directory))
            csv_path = os.path.join(self.directory, f"{folder_name}.csv")
            df = pd.read_csv(csv_path)
            return df.to_dict(orient="records")
        except FileNotFoundError as e:
            print(f"CSV file not found: {e}")
            return self.create_empty_data(self.directory)  # Call the defined function
        except pd.errors.ParserError as e:
            print(f"Error parsing CSV file: {e}")
            return []  # Or handle the error differently
        except Exception as e:
            print(f"Unexpected error while reading CSV: {e}")
            # Handle unexpected errors

    def create_empty_data(self, directory):
        # Define logic to create an empty data structure (e.g., empty list or dictionary)
        # This function should return the empty data structure
        return []  # Example: return an empty list

    