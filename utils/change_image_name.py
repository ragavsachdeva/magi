import os
import shutil


def rename_image_to_correct_format(images_folder, new_folder, num_digits: int =3):
    original_image_path_list = []
    new_image_path_list = []

    # Create the new folder if it doesn't exist
    os.makedirs(new_folder, exist_ok=True)

    for idx, image_path in enumerate(os.listdir(images_folder)):
        original_path = os.path.join(images_folder, image_path)
        if os.path.isfile(original_path):  # Ensure it's a file
            original_image_path_list.append(image_path)
            original_ext = os.path.splitext(image_path)[1]
            new_name = f"{idx:0{num_digits}}{original_ext}"
            new_path = os.path.join(new_folder, new_name)
            shutil.copy2(original_path, new_path)
            new_image_path_list.append(new_name)

    print(f"original_image_path_list: {original_image_path_list}")
    print(f"new_image_path_list: {new_image_path_list}")