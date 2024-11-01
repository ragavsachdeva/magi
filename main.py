import os
from utils.img2mp4 import create_video_from_images
from utils.process_raw_from_json import process_all_images_and_jsons
from utils.utils import rename_image_to_correct_format, get_digit_number_for_name_format, generate_name_format

def main(process_image=True, create_video=True):
    images_folder = 'test_output_coloring'
    json_folder = 'magi_functional/data_test/personal_data/Ruri_Dragon/json_results'

    save_path = "test_output_final"
    number_of_digit_for_name = get_digit_number_for_name_format(images_folder)
    name_format = generate_name_format(number_of_digit_for_name)

    formated_image_path = os.path.join(images_folder, 'renamed')
    formated_images_folder = rename_image_to_correct_format(images_folder, formated_image_path, num_digits=number_of_digit_for_name)
    formated_json_path = os.path.join(json_folder, 'renamed')
    formated_json_folder = rename_image_to_correct_format(json_folder, formated_json_path, num_digits=number_of_digit_for_name)

    nuke_option = True
    panel_view_option = False

    if process_image:
        process_all_images_and_jsons(images_folder = formated_images_folder, json_folder = formated_json_folder, save_path = save_path, name_format = name_format, nuke = nuke_option, panel_view = panel_view_option)

    if create_video:
        create_video_from_images(image_dir=save_path, output_video_path=save_path, name_format=name_format, use_padding=True)

if __name__ == "__main__":
    main(process_image=True, create_video=False)