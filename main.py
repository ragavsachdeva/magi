# # images_folder = 'test_output_coloring'
# # json_folder = 'magi_functional/data_test/personal_data/Ruri_Dragon/json_results'
# # save_path = "test_output_final"

# images_folder = 'data_test/personal_data/Ruri_Dragon/raw'
# json_folder = 'data_test/personal_data/Ruri_Dragon/json_results'
# save_path = "data_test/code/test_lab/panel_images_full_chapter"

    
import os
import argparse
import shutil
from utils.img2mp4 import create_video_from_images
from utils.process_raw_from_json import process_all_images_and_jsons

from utils.utils import rename_image_to_correct_format, get_digit_number_for_name_format, generate_name_format

def main(images_folder, json_folder, save_path, audio_dir, process_image=True, process_video=True, panel_view_option = True, nuke_option = True):
    """
    Main function to process manga images and generate video with speech bubbles.

    :param images_folder: Path to the folder containing raw images.
    :param json_folder: Path to the folder containing JSON files with dialogue data.
    :param save_path: Path where the processed images and video will be saved.
    :param process_image: Flag to process images and generate speech bubbles (default: True).
    :param process_video: Flag to create a video from the processed images (default: True).
    """
    # Generate the correct name format based on the number of digits in filenames
    number_of_digit_for_name = get_digit_number_for_name_format(images_folder)
    name_format = generate_name_format(number_of_digit_for_name)

    # Create folder paths for renamed images and JSONs
    formated_image_path = os.path.join(images_folder, 'renamed')
    formated_images_folder = rename_image_to_correct_format(images_folder, formated_image_path, num_digits=number_of_digit_for_name)

    formated_json_path = os.path.join(json_folder, 'renamed')
    formated_json_folder = rename_image_to_correct_format(json_folder, formated_json_path, num_digits=number_of_digit_for_name)
    

    # Process images and generate speech bubbles if flag is set
    if process_image:
        process_all_images_and_jsons(
            images_folder=formated_images_folder,
            json_folder=formated_json_folder,
            save_path=save_path,
            name_format=name_format,
            nuke=nuke_option,
            panel_view=panel_view_option
        )

    # Create video from processed images if flag is set
    if process_video:
        create_video_from_images(
            image_dir=save_path,
            audio_dir=audio_dir,
            output_video_path=save_path,
            name_format=name_format,
            use_padding=True
        )
def parse_args():
    parser = argparse.ArgumentParser(description="Process manga images and generate a video with speech bubbles.")
    parser.add_argument('-i', '--image', type=str, default="output/colorized/rename", help="Path to the folder containing raw manga images.")
    parser.add_argument('-j', '--json', type=str, default="output/json", help="Path to the folder containing JSON files with dialogue data.")
    parser.add_argument('-a', '--audio', type=str, default="output/audio", help="Path to the folder containing audio files.")

    # Use type=str to accept True or False as strings
    parser.add_argument('-panel', '--panel_view', type=str, choices=['True', 'False'], default='True', help="Flag to enable panel view. Use 'True' or 'False'.")
    parser.add_argument('-nuke', '--nuke_option', type=str, choices=['True', 'False'], default='True', help="Flag to enable nuking. Use 'True' or 'False'.")

    parser.add_argument('-s', '--save', type=str, default="output/output_final", help="Path to save the processed images and output video.")

    # Flags for processing image and video
    parser.add_argument('-pi', '--process_image', type=str, choices=['True', 'False'], default='True', help="Flag to process images and generate speech bubbles.")
    parser.add_argument('-pv', '--process_video', type=str, choices=['True', 'False'], default='True', help="Flag to create a video from processed images.")

    args = parser.parse_args()

    # Convert 'True'/'False' strings to actual booleans
    args.panel_view = args.panel_view == 'True'
    args.nuke_option = args.nuke_option == 'True'
    args.process_image = args.process_image == 'True'
    args.process_video = args.process_video == 'True'

    return args

def create_save_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    os.makedirs(folder_path, exist_ok=True)
    
if __name__ == "__main__":
    args = parse_args()

    create_save_folder(args.save)

    # Call the main function with parsed arguments
    main(
        images_folder=args.image,
        json_folder=args.json,
        save_path=args.save,
        audio_dir=args.audio,
        process_image=args.process_image,
        process_video=args.process_video,
        panel_view_option=args.panel_view,
        nuke_option=args.nuke_option
    )

# HOW TO USE
# python main.py -i test_output_coloring -j magi_functional/data_test/personal_data/Ruri_Dragon/json_results -s test_output_final -panel True  