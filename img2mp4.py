import cv2
import os
import numpy as np
from glob import glob

import re

def convert_to_video_name_format(name_format: str) -> str:
    # Replace anything between { and } with {}
    return re.sub(r'\{[^}]*\}', '{}', name_format)

def create_video_from_images(image_dir: str, output_video_path: str, name_format: str, use_padding: bool, fps: int = 30, duration_per_image: float = 0.5, reverse_order: bool = False):

    video_name_format = convert_to_video_name_format(name_format)

    output_video_name = os.path.join(output_video_path, f'video_Padding_{use_padding}.mp4')
    # Calculate the total frames for each image based on desired display duration
    frames_per_image = int(fps * duration_per_image)

    # Get all the modified images sorted in reverse order using the provided video_name_format
    image_files = sorted(glob(os.path.join(image_dir, video_name_format.format('*', '*', '*', '*'))), reverse=reverse_order)

    # Check if there are any image files
    if not image_files:
        print("No modified images found.")
        return

    # Find the largest dimensions among the images
    max_height = 0
    max_width = 0

    for image_file in image_files:
        img = cv2.imread(image_file)
        height, width, _ = img.shape
        max_height = max(max_height, height)
        max_width = max(max_width, width)

    # Create a VideoWriter object for MP4 with the maximum dimensions
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for MP4
    video_writer = cv2.VideoWriter(output_video_name, fourcc, fps, (max_width, max_height))

    # Loop through the images and write them to the video
    for image_file in image_files:
        img = cv2.imread(image_file)

        # Create a black background image with max dimensions if padding is needed
        if use_padding:
            background = np.zeros((max_height, max_width, 3), dtype=np.uint8)

            # Get the dimensions of the current image
            height, width, _ = img.shape
            
            # Calculate the position to place the current image on the background
            x_offset = (max_width - width) // 2
            y_offset = (max_height - height) // 2
            
            # Place the current image on the background
            background[y_offset:y_offset + height, x_offset:x_offset + width] = img
        else:
            # For no padding, fit the image to max dimensions
            height, width, _ = img.shape
            
            # Calculate the scaling factor to fit the image to the maximum width or height
            scale = min(max_width / width, max_height / height)
            new_width = int(width * scale)
            new_height = int(height * scale)

            # Resize the image
            resized_img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_LINEAR)

            # Create a black background image with max dimensions
            background = np.zeros((max_height, max_width, 3), dtype=np.uint8)
            
            # Calculate the position to place the resized image on the background
            x_offset = (max_width - new_width) // 2
            y_offset = (max_height - new_height) // 2
            
            # Place the resized image on the background
            background[y_offset:y_offset + new_height, x_offset:x_offset + new_width] = resized_img

        for _ in range(frames_per_image):
            video_writer.write(background)  # Write the (padded) image multiple times for the duration

    # Release the video writer
    video_writer.release()

    print(f"Video saved as: {output_video_name}")

# Example usage
# image_dir = "./data_test/code/test_lab/panel_images_full_chapter"
image_dir = "./data_test/code/test_lab/panel_images"
# image_dir = "./data_test/code/test_lab/full_image"
name_format = "page_{:03}_panel_{:03}_bubble_{:03}{}"

# Create video with padding
create_video_from_images(image_dir=image_dir, output_video_path=image_dir, name_format=name_format, use_padding=True)