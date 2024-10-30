import json
import os
from PIL import Image, ImageDraw

from .img2mp4 import create_video_from_images


def read_coordinates(json_file_path: str):
    """Read essential text coordinates from the given JSON file."""
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    return [
        text for text, is_essential in zip(data["texts"], data["is_essential_text"]) if is_essential
    ], data["panels"]  # Return text coordinates and panel coordinates

def process_full_page(images_dir: str, json_file_path: str, save_path: str = "./panel_images", name_format: str = "page_{:03}_panel_{:03}_bubble_{:03}{}"):
    os.makedirs(save_path, exist_ok=True)

    # Load the JSON data
    with open(json_file_path, 'r') as f:
        data = json.load(f)

    # Extract the text coordinates
    text_coords, _ = read_coordinates(json_file_path)
    
    total_length_text = len(text_coords)
    image_name_ext = os.path.basename(images_dir)

    # Split the image name and its extension
    image_name, image_extension = os.path.splitext(image_name_ext)
    image_name = int(image_name)

    with Image.open(images_dir) as img:
        # Create a draw object on the original image copy
        draw = ImageDraw.Draw(img)

        # Initialize the modified panel image path
        modified_panel_image_path = os.path.join(save_path, name_format)
        text_order = total_length_text

        # Save the modified panel image with the last computed bubble index
        img.save(modified_panel_image_path.format(image_name, 0, text_order, image_extension))

        # Loop through each set of coordinates in reverse order
        for box_index, box in enumerate(reversed(text_coords)):
            x1, y1, x2, y2 = map(int, box)  # Ensures all values are integers

            # Initialize max color and max value
            max_color = (0, 0, 0)  # Start with black
            max_value = 0

            # Iterate through the box's pixels
            for y in range(y1, y2):
                for x in range(x1, x2):
                    # Get the pixel color using absolute coordinates
                    color = img.getpixel((x, y))
                    color_value = sum(color[:3])  # Sum RGB values

                    # Update max color if the current pixel's value is higher
                    if color_value > max_value:
                        max_value = color_value
                        max_color = color

            # Fill the rectangle with the max color
            draw.rectangle(box, fill=max_color)

            # Save modified image path for the current chat bubble
            text_order = total_length_text - (box_index + 1)
            modified_image_path = modified_panel_image_path.format(image_name, 0, text_order, image_extension)

            # Instead of saving here, save it once at the end
            img.save(modified_image_path, format='JPEG')

    print(f"Processed and saved modified full page images for: {image_name_ext}")

def process_panel_view(images_dir: str, json_file_path: str, save_path: str = "./panel_images", name_format: str = "page_{:03}_panel_{:03}_bubble_{:03}{}"):
    os.makedirs(save_path, exist_ok=True)

    text_coords, panel_coords = read_coordinates(json_file_path)
    total_length_text = len(text_coords)
    image_name_ext = os.path.basename(images_dir)

    # Split the image name and its extension
    image_name, image_extension = os.path.splitext(image_name_ext)
    image_name = int(image_name)

    with Image.open(images_dir) as img:
        # Create a copy of the image for drawing
        original_img = img.copy()

        # Loop through each panel
        for panel_index, panel in enumerate(panel_coords):
            # Create a panel-specific image by cropping the original image
            panel_box = (panel[0], panel[1], panel[2], panel[3])  # box format: (x1, y1, x2, y2)
            panel_image = original_img.crop(panel_box)

            # Create a draw object on the panel image copy
            draw = ImageDraw.Draw(panel_image)

            # Initialize the modified panel image path
            modified_panel_image_path = os.path.join(save_path, name_format)
            text_order = total_length_text

            # Save the modified panel image with the last computed bubble index
            panel_image.save(modified_panel_image_path.format(image_name, panel_index, text_order, '.jpg'))
            
            # Loop through each set of coordinates in reverse order
            for box_index, box in enumerate(reversed(text_coords)):
                # Calculate the center point of the chatbox
                x_center = (box[0] + box[2]) // 2
                y_center = (box[1] + box[3]) // 2

                # Check if the center point is inside the panel
                if panel[0] <= x_center <= panel[2] and panel[1] <= y_center <= panel[3]:
                    # Calculate the position of the box relative to the panel
                    relative_box = (
                        box[0] - panel[0],
                        box[1] - panel[1],
                        box[2] - panel[0],
                        box[3] - panel[1]
                    )

                    # Get the coordinates of the relative box and convert to integers
                    x1, y1, x2, y2 = map(int, relative_box)  # Ensures all values are integers

                    # Initialize max color and max value
                    max_color = (0, 0, 0)  # Start with black
                    max_value = 0

                    # Iterate through the box's pixels
                    for y in range(y1, y2):
                        for x in range(x1, x2):
                            # Get the pixel color using absolute coordinates
                            color = original_img.getpixel((x + panel[0], y + panel[1]))
                            color_value = sum(color[:3])  # Sum RGB values

                            # Update max color if the current pixel's value is higher
                            if color_value > max_value:
                                max_value = color_value
                                max_color = color

                    # Fill the rectangle with the max color
                    draw.rectangle(relative_box, fill=max_color)

                    # Save modified image path for the current chat bubble
                    text_order = total_length_text - (box_index + 1)
                    modified_image_path = modified_panel_image_path.format(image_name, panel_index, text_order, '.jpg')

                    # Instead of saving here, save it once at the end
                    panel_image.save(modified_image_path, format='JPEG')

    print(f"Processed and saved modified panel view images for: {image_name_ext}")

def process_all_images_and_jsons(images_folder: str, json_folder: str, save_path: str = "./panel_images", name_format: str = "page_{:03}_panel_{:03}_bubble_{:03}{}", nuke: bool = False, panel_view: bool = False):
    
    if nuke:
        try:
            image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}

            for filename in os.listdir(save_path):
                # Check if the file has an image extension
                if os.path.splitext(filename)[1].lower() in image_extensions:
                    file_path = os.path.join(save_path, filename)
                    os.remove(file_path)
            print(f"Deleted images")
        except FileNotFoundError as e:
            print(f"Error: {e}")

    # Get all image and json file names
    image_files = [f for f in os.listdir(images_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
    json_files = [f for f in os.listdir(json_folder) if f.lower().endswith('.json')]
    if len(image_files) != len(json_files):
        print("Number of images and json files do not match!")
    else:
        for image_file in image_files:
            # Construct full image path
            image_path = os.path.join(images_folder, image_file)

            # Corresponding json file name (assuming they have the same base name)
            json_file_name = os.path.splitext(image_file)[0] + '.json'
            if json_file_name in json_files:
                json_path = os.path.join(json_folder, json_file_name)

                # Process the image and json based on panel_view flag
                if panel_view:
                    process_panel_view(image_path, json_path, save_path, name_format)
                else:
                    process_full_page(image_path, json_path, save_path, name_format)


if __name__ == "__main__":
    images_folder = '../data_test/personal_data/Ruri_Dragon/raw'
    json_folder = '../data_test/personal_data/Ruri_Dragon/json_results'
    save_path = "../data_test/code/test_lab/panel_images_full_chapter"
    # save_path = "./data_test/code/test_lab/panel_images"
    name_format = "page_{:03}_panel_{:03}_bubble_{:03}{}"
    nuke_option = True
    panel_view_option = False

    # process_all_images_and_jsons(images_folder, json_folder, save_path, name_format, nuke_option, panel_view_option)

    create_video_from_images(image_dir=save_path, output_video_path=save_path, name_format=name_format, use_padding=True)

