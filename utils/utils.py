import math
import os
import re
import shutil


def get_digit_number_for_name_format(directory_path, buffer_number: int = 2):
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp', '.heif', '.ico')
    num_images = len([name for name in os.listdir(directory_path) if name.lower().endswith(image_extensions)])
     
    if num_images > 0:
        number_of_digit_for_name = math.ceil(math.log10(num_images+1)) + buffer_number
    else: 
        number_of_digit_for_name = buffer_number
    return number_of_digit_for_name

def generate_name_format(number_of_digit_for_name: int):
    name_format = f"page_{{:0{number_of_digit_for_name}}}_panel_{{:0{number_of_digit_for_name}}}_bubble_{{:0{number_of_digit_for_name}}}{{}}"
    return name_format

def rename_image_to_correct_format(images_folder, new_folder, num_digits: int =3):
    if os.path.exists(new_folder):
        shutil.rmtree(new_folder)

    os.makedirs(new_folder, exist_ok=True)

    sorted_images = sort_files(images_folder)

    for idx, image_path in enumerate(sorted_images):
        original_path = os.path.join(images_folder, image_path)
        if os.path.isfile(original_path):  # Ensure it's a file
            original_ext = os.path.splitext(image_path)[1]
            new_name = f"{idx:0{num_digits}}{original_ext}"
            new_path = os.path.join(new_folder, new_name)
            shutil.copy2(original_path, new_path)
    return new_folder

def sort_files(directory):
    files = []
    
    for file in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file)):
            files.append(file)

    sorted_list = sorted(files, key=lambda filename: [int(part) if part.isdigit() else part for part in re.split(r'(\d+)', filename)])
    return sorted_list