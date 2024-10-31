import os
import re
import shutil


def rename_image_to_correct_format(images_folder, new_folder, num_digits: int =3):
    if os.path.exists(new_folder):
        shutil.rmtree(new_folder)

    os.makedirs(new_folder, exist_ok=True)

    for idx, image_path in enumerate(os.listdir(images_folder)):
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