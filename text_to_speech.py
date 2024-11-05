import os
import random
import re
import shutil
import argparse
import torch
from TTS.api import TTS
from unittest.mock import patch
import re
from utils.utils import create_save_folder, generate_name_format, get_digit_number_for_name_format

# Function to parse the transcript from a text file
def parse_transcript(transcript_path):
    pages = []
    current_page = None

    with open(transcript_path, 'r') as file:
        content = file.readlines()
    
    for line in content:
        if line.startswith("<page>"):
            # Start a new page
            if current_page is not None:
                pages.append(current_page)
            current_page = {"page": re.search(r'<page>(\d+)<endpage>', line).group(1), "lines": []}   
        elif line.startswith("<name>") and current_page is not None:
            # Extract character name and dialogue
            match = re.match(r"<name>([^<]+)<endname>:\s*(.+)", line)
            if match:
                character = match.group(1).lower()  # Lowercase for consistency
                dialogue = match.group(2)
                current_page["lines"].append((character, dialogue))

    # Add the last page if it exists
    if current_page is not None:
        pages.append(current_page)
        
    return pages

# Function to get all voice files from the specified directory
def get_voice_files(directory):
    all_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".wav"):
                all_files.append(os.path.join(root, file))
    return all_files

# Function to filter voice files into male and female categories
def filter_voice_files(files):
    male_files = []
    female_files = []
    
    for file in files:
        # Extract the actor number from the filename
        match = re.search(r"(\d{2})\.wav$", file)
        if match:
            actor_number = int(match.group(1))
            if actor_number % 2 == 0:  # Even numbers are female
                female_files.append(file)
            else:  # Odd numbers are male
                male_files.append(file)
                
    return male_files, female_files

# Function to randomly select voice files for characters
def select_voice_files_for_characters(characters, male_characters, voice_bank):
    all_files = get_voice_files(voice_bank)
    male_files, female_files = filter_voice_files(all_files)

    selected_files = {}
    used_files = set()  # To keep track of used voice files

    for character in characters:
        if character in male_characters:
            # Select a random male voice that hasn't been used
            available_male_files = list(set(male_files) - used_files)
            if available_male_files:
                selected_files[character] = random.choice(available_male_files)
                used_files.add(selected_files[character])
        else:
            # Select a random female voice that hasn't been used, if available
            available_female_files = list(set(female_files) - used_files)
            if available_female_files:
                selected_files[character] = random.choice(available_female_files)
                used_files.add(selected_files[character])
            else:
                # Select any remaining file for other characters, ensuring it's not already used
                available_files = list(set(all_files) - used_files)
                if available_files:
                    selected_files[character] = random.choice(available_files)
                    used_files.add(selected_files[character])
    
    return selected_files

# Function to convert text to speech for a character
def voice_character(character, text, page_number, bubble_number, selected_files, save_directory, name_format="page_{:03d}_panel_{:03d}_bubble_{:03d}{}"):
    speaker_wav = selected_files.get(character)

    if speaker_wav:
        audio_output_filename = name_format.format(int(page_number), 0, bubble_number+1, ".wav")
        output_filename = os.path.join(save_directory, audio_output_filename)
        output = tts.tts_to_file(text=text, speaker_wav=speaker_wav, language="en")
        os.rename("output.wav", output_filename)  # Rename the default output file
        return output_filename
    else:
        raise ValueError(f"Character '{character}' not found in voice mapping.")

# Function to process the transcript and create audio files
def text2speech(pages, selected_files, save_directory):
    output_files = []

    create_save_folder(save_directory)

    for page in pages:
        page_number = page["page"]
        for bubble_number, (character, dialogue) in enumerate(page["lines"]):
            try:
                output = voice_character(character, dialogue, page_number, bubble_number, selected_files, save_directory)
                output_files.append(output)
            except ValueError as e:
                print(e)
    print(f"Audio files have been saved to {save_directory}")

    return output_files

def parse_args():
    parser = argparse.ArgumentParser(description="Generate speech from a transcript using pre-recorded voice files.")
    parser.add_argument("-i", "--images_folder", default="input/raw", required=True, type=str, help="Directory containing manga images.")
    parser.add_argument("-v", "--voice_bank", required=True, type=str, help="Directory containing voice files.")
    parser.add_argument("-t", "--transcript", default="output/transcript", required=True, type=str, help="Path to the transcript text file.")
    parser.add_argument("-o", "--output", required=True, type=str, help="Directory to save the generated audio files.")
    
    parser.add_argument("-m", "--male_characters", nargs='+', type=str, help="List of male character names.")

    return parser.parse_args()

if __name__ == "__main__":
    # Parse command-line arguments
    args = parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Running on {device}")
    # Mock input to automatically respond with 'y'
    with patch('builtins.input', return_value='y'):
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

    number_of_digit_for_name = get_digit_number_for_name_format(args.images_folder)
    name_format = generate_name_format(number_of_digit_for_name)

    # Parse the transcript file
    pages = parse_transcript(args.transcript)
    characters = {line[0] for page in pages for line in page["lines"]}

    # Select voice files for characters
    selected_files = select_voice_files_for_characters(characters, args.male_characters, args.voice_bank)

    output_files = text2speech(pages, selected_files, args.output)

    
