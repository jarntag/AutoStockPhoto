import os
import subprocess
import re

def process_images(directory_path, regions, age, disc_string, keywords_list):
  """Processes images in batches based on regions, adding metadata.

  Args:
    directory_path: The directory containing images.
    regions: A list of region strings.
    age: The age string.
    disc_string: The base description string.
    keywords_list: A list of keywords.
  """

  images = sorted([f for f in os.listdir(directory_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
  num_images_per_region = 4

  for i, region in enumerate(regions):
    start_index = i * num_images_per_region
    end_index = start_index + num_images_per_region
    region_images = images[start_index:end_index]

    for j, image_file in enumerate(region_images):
      image_path = os.path.join(directory_path, image_file)
      title = f"{disc_string} {region} {age}, ultra realistic, candid, social media, avatar image, plain solid background"
      keywords = f"{region}; {age}; {'; '.join(keywords_list)}"
      metadata = {'Title': title, 'XMP:Subject': keywords}
      add_metadata_to_image(image_path, metadata)
      print(title)

def add_metadata_to_image(image_path, metadata):
  """Adds title and keywords to an image using exiftool.

  Args:
    image_path: Path to the image file.
    metadata: A dictionary containing title and keywords.
  """

  try:
    command = ['exiftool', '-overwrite_original']
    for field, value in metadata.items():
      command.extend([f'-{field}={value}'])
    command.append(image_path)
    subprocess.run(command, check=True)
  except subprocess.CalledProcessError as e:
    print(f"Error processing {image_path}: {e}")

# Example usage
directory_path = 'E:\Test'
regions = [
    # Africa
    'Africa', 'Algeria', 'Angola', 'Benin', 'Botswana', 'Burkina Faso', 'Burundi', 'Cabo Verde', 'Cameroon',
    'Central African Republic', 'Chad', 'Comoros', 'Congo', 'Democratic Republic of the Congo', 'Republic of the Congo',
    'Côte d Ivoire', 'Djibouti', 'Egypt', 'Equatorial Guinea', 'Eritrea', 'Eswatini', 'Ethiopia', 'Gabon', 'Gambia',
    'Ghana', 'Guinea', 'Guinea-Bissau', 'Kenya', 'Lesotho', 'Liberia', 'Libya', 'Madagascar', 'Malawi', 'Mali',
    'Mauritania', 'Mauritius', 'Morocco', 'Mozambique', 'Namibia', 'Niger', 'Nigeria', 'Rwanda', 'São Tomé and Príncipe',
    'Senegal', 'Seychelles', 'Sierra Leone', 'Somalia', 'South Africa', 'South Sudan', 'Sudan', 'Tanzania', 'Togo',
    'Tunisia', 'Uganda', 'Zambia', 'Zimbabwe',

    # Asia
    'Asia', 'Afghanistan', 'Armenia', 'Azerbaijan', 'Bahrain', 'Bangladesh', 'Bhutan', 'Brunei', 'Cambodia', 'China',
    'Cyprus', 'East Timor', 'Georgia', 'India', 'Indonesia', 'Iran', 'Iraq', 'Israel', 'Japan', 'Jordan', 'Kazakhstan',
    'North Korea', 'South Korea', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Lebanon', 'Malaysia', 'Maldives', 'Mongolia',
    'Myanmar', 'Nepal', 'Oman', 'Pakistan', 'Palestine', 'Philippines', 'Qatar', 'Russia', 'Saudi Arabia', 'Singapore',
    'Sri Lanka', 'Syria', 'Tajikistan', 'Thailand', 'Turkey', 'Turkmenistan', 'United Arab Emirates', 'Uzbekistan',
    'Vietnam', 'Yemen',

    # Europe
    'Europe', 'Albania', 'Andorra', 'Austria', 'Belarus', 'Belgium', 'Bosnia and Herzegovina', 'Bulgaria', 'Croatia',
    'Cyprus', 'Czech Republic', 'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary', 'Iceland',
    'Ireland', 'Italy', 'Kosovo', 'Latvia', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Malta', 'Moldova', 'Monaco',
    'Montenegro', 'Netherlands', 'North Macedonia', 'Norway', 'Poland', 'Portugal', 'Romania', 'Russia', 'San Marino',
    'Serbia', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'Turkey', 'Ukraine', 'United Kingdom',
    'Vatican City',

    # North America
    'North America', 'Antigua and Barbuda', 'Bahamas', 'Barbados', 'Belize', 'Canada', 'Costa Rica', 'Cuba', 'Dominica',
    'Dominican Republic', 'El Salvador', 'Grenada', 'Guatemala', 'Haiti', 'Honduras', 'Jamaica', 'Mexico', 'Nicaragua',
    'Panama', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'United States',

    # Oceania
    'Oceania', 'Australia', 'Fiji', 'Kiribati', 'Marshall Islands', 'Federated States of Micronesia', 'Nauru',
    'New Zealand', 'Palau', 'Papua New Guinea', 'Samoa', 'Solomon Islands', 'Tonga', 'Tuvalu', 'Vanuatu',

    # South America
    'South America', 'Argentina', 'Bolivia', 'Brazil', 'Chile', 'Colombia', 'Ecuador', 'Guyana', 'Paraguay', 'Peru',
    'Suriname', 'Uruguay', 'Venezuela'
]

age = 'old man'
disc_string = 'Portrait view of a regular happy smiling'
keywords_list = ['people', 'person', 'portrait', 'Country', 'region', 'nationality', 'Continent', 'world population', 'age', 'face', 'energetic', 'innocent', 'playful', 'lifestyle', 'authentic', 'model', 'genuine', 'vibrant', 'positive', 'candid', 'carefree', 'one', 'expression', 'joy', 'happiness', 'casual', 'studio', 'smiling', 'smile', 'happy', 'joyful', 'laughing', 'cheerful', 'fun', 'eyes', 'child', 'teenager', 'man', 'male', 'youth', 'handsome', 'cute', 'woman', 'children', 'beauty', 'young', 'childhood']

process_images(directory_path, regions, age, disc_string, keywords_list)