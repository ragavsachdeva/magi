import subprocess
import cv2
import os
import numpy as np
from glob import glob
import re
from pydub import AudioSegment

def convert_to_video_name_format(name_format: str) -> str:
    return re.sub(r'\{[^}]*\}', '{}', name_format)

def duration_calculation(audio_filename: str) -> float:
    audio = AudioSegment.from_file(audio_filename)
    duration_in_seconds = len(audio) / 1000
    return duration_in_seconds

def create_video_from_images(image_dir: str, audio_dir: str, output_video_path: str, name_format: str, use_padding: bool, fps: int = 24, default_duration: float = 0.5, compressed: bool = False, delete_original: bool = True):
    video_name_format = convert_to_video_name_format(name_format)
    output_video_name = os.path.join(output_video_path, f'video_Padding_{use_padding}.mp4')

    image_files = sorted(glob(os.path.join(image_dir, video_name_format.format('*', '*', '*', '*'))))

    if not image_files:
        print("No modified images found.")
        return

    max_height = 0
    max_width = 0

    for image_file in image_files:
        img = cv2.imread(image_file)
        height, width, _ = img.shape
        max_height = max(max_height, height)
        max_width = max(max_width, width)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_video_name, fourcc, fps, (max_width, max_height))

    for image_file in image_files:
        img = cv2.imread(image_file)

        audio_file = os.path.join(audio_dir, os.path.basename(image_file).replace('.png', '.wav').replace('.jpg', '.wav'))

        if os.path.exists(audio_file):
            duration_per_image = duration_calculation(audio_file)
        else:
            duration_per_image = default_duration

        frames_per_image = int(fps * duration_per_image)

        if use_padding:
            background = np.zeros((max_height, max_width, 3), dtype=np.uint8)
            height, width, _ = img.shape
            x_offset = (max_width - width) // 2
            y_offset = (max_height - height) // 2
            background[y_offset:y_offset + height, x_offset:x_offset + width] = img
        else:
            height, width, _ = img.shape
            scale = min(max_width / width, max_height / height)
            new_width = int(width * scale)
            new_height = int(height * scale)
            resized_img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
            background = np.zeros((max_height, max_width, 3), dtype=np.uint8)
            x_offset = (max_width - new_width) // 2
            y_offset = (max_height - new_height) // 2
            background[y_offset:y_offset + new_height, x_offset:x_offset + new_width] = resized_img

        for _ in range(frames_per_image):
            video_writer.write(background)

    video_writer.release()
    print(f"Video saved as: {output_video_name}")
    
    merge_audio_with_video(output_video_name, audio_dir, image_files, default_duration, delete_original)

def merge_audio_with_video(video_file: str, audio_dir: str, image_files: list, default_duration: float, delete_original: bool = True):
    audio_segments = []

    for image_file in image_files:
        audio_file = os.path.join(audio_dir, os.path.basename(image_file).replace('.jpg', '.wav'))
        if os.path.exists(audio_file):
            audio_segments.append(AudioSegment.from_file(audio_file))
        else:
            # Append silence for the default duration if audio file not found
            silence_segment = AudioSegment.silent(duration=default_duration * 1000)  # Duration in milliseconds
            audio_segments.append(silence_segment)

    # Concatenate all audio segments
    final_audio = sum(audio_segments)

    # Save the combined audio to a temporary file
    temp_audio_file = os.path.join(os.path.dirname(video_file), 'temp_audio.wav')
    final_audio.export(temp_audio_file, format='wav')

    # Merge audio with video
    base_name = os.path.splitext(os.path.basename(video_file))[0]  # Get the file name without extension
    output_with_audio = os.path.join(os.path.dirname(video_file), f"{base_name}_audio.mp4")

    command = [
        'ffmpeg',
        '-i', video_file,
        '-i', temp_audio_file,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-strict', 'experimental',
        '-shortest',
        output_with_audio,
        '-y'  # Overwrite if it exists
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Audio merged successfully into video saved as: {output_with_audio}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while merging audio and video: {e}")

    if delete_original:
        os.remove(temp_audio_file)
        os.remove(video_file)
        print(f"Temporary audio file '{temp_audio_file}' deleted. Original video '{video_file}' deleted.")

if __name__ == "__main__":
    # image_dir = "./data_test/code/test_lab/panel_images_full_chapter"
    # image_dir = "./data_test/code/test_lab/panel_images"
    image_dir = "./data_test/code/test_lab/full_image"
    audio_dir = "./data_test/code/test_lab/audio_results"
    name_format = "page_{:04}_panel_{:04}_bubble_{:04}{}"

    create_video_from_images(image_dir=image_dir, audio_dir=audio_dir, output_video_path=image_dir, name_format=name_format, use_padding=True)
