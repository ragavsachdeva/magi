from utils.img2mp4 import create_video_from_images
from utils.process_raw_from_json import process_all_images_and_jsons


if __name__ == "__main__":
    images_folder = './data_test/personal_data/Ruri_Dragon/raw'
    json_folder = './data_test/personal_data/Ruri_Dragon/json_results'
    save_path = "./data_test/code/test_lab/panel_images_full_chapter"
    # save_path = "./data_test/code/test_lab/panel_images"
    name_format = "page_{:03}_panel_{:03}_bubble_{:03}{}"
    nuke_option = True
    panel_view_option = False

    # process_all_images_and_jsons(images_folder, json_folder, save_path, name_format, nuke_option, panel_view_option)

    create_video_from_images(image_dir=save_path, output_video_path=save_path, name_format=name_format, use_padding=True)