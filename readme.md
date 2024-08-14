# Magi, The Manga Whisperer

![Static Badge](https://img.shields.io/badge/V1-blue) 
[![Static Badge](https://img.shields.io/badge/arXiv-2401.10224-blue)](http://arxiv.org/abs/2401.10224)
[![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fhuggingface.co%2Fapi%2Fmodels%2Fragavsachdeva%2Fmagi%3Fexpand%255B%255D%3Ddownloads%26expand%255B%255D%3DdownloadsAllTime&query=%24.downloadsAllTime&label=%F0%9F%A4%97%20Downloads)](https://huggingface.co/ragavsachdeva/magi)

![Static Badge](https://img.shields.io/badge/V2-blue) 
[![Static Badge](https://img.shields.io/badge/arXiv-2408.00298-blue)](https://arxiv.org/abs/2408.00298)
[![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fhuggingface.co%2Fapi%2Fmodels%2Fragavsachdeva%2Fmagiv2%3Fexpand%255B%255D%3Ddownloads%26expand%255B%255D%3DdownloadsAllTime&query=%24.downloadsAllTime&label=%F0%9F%A4%97%20Downloads)](https://huggingface.co/ragavsachdeva/magiv2)

TODOs: 
- [x] Upload Magiv2 model,
- [ ] provide new annotations,
- [ ] open-source PopCharacters dataset,
- [ ] release evaluation scripts.

## Magiv1
- The model is available at 🤗 [HuggingFace Model Hub](https://huggingface.co/ragavsachdeva/magi).
- Try it out for yourself using this 🤗 [HuggingFace Spaces Demo](https://huggingface.co/spaces/ragavsachdeva/the-manga-whisperer/) (no GPU, so slow).
- Basic model usage is provided below. Inspect [this file](https://huggingface.co/ragavsachdeva/magi/blob/main/modelling_magi.py) for more info.

![Magi_teaser](https://github.com/ragavsachdeva/magi/assets/26804893/0a6d44bc-12ef-4545-ab9b-577c77bdfd8a)

### V1 Usage
```python
from transformers import AutoModel
import numpy as np
from PIL import Image
import torch
import os

images = [
        "path_to_image1.jpg",
        "path_to_image2.png",
    ]

def read_image_as_np_array(image_path):
    with open(image_path, "rb") as file:
        image = Image.open(file).convert("L").convert("RGB")
        image = np.array(image)
    return image

images = [read_image_as_np_array(image) for image in images]

model = AutoModel.from_pretrained("ragavsachdeva/magi", trust_remote_code=True).cuda()
with torch.no_grad():
    results = model.predict_detections_and_associations(images)
    text_bboxes_for_all_images = [x["texts"] for x in results]
    ocr_results = model.predict_ocr(images, text_bboxes_for_all_images)

for i in range(len(images)):
    model.visualise_single_image_prediction(images[i], results[i], filename=f"image_{i}.png")
    model.generate_transcript_for_single_image(results[i], ocr_results[i], filename=f"transcript_{i}.txt")
```

## Magiv2
- The model is available at 🤗 [HuggingFace Model Hub](https://huggingface.co/ragavsachdeva/magiv2).
- A HuggingFace demo coming soon.
- Basic model usage is provided below. Inspect [this file](https://huggingface.co/ragavsachdeva/magiv2/blob/main/modelling_magiv2.py) for more info.

![magiv2](https://github.com/user-attachments/assets/e0cd1787-4a0c-49a5-a9d8-be2911d5ec08)

### V2 Usage
```python
from PIL import Image
import numpy as np
from transformers import AutoModel
import torch

model = AutoModel.from_pretrained("ragavsachdeva/magiv2", trust_remote_code=True).cuda().eval()


def read_image(path_to_image):
    with open(path_to_image, "rb") as file:
        image = Image.open(file).convert("L").convert("RGB")
        image = np.array(image)
    return image

chapter_pages = ["page1.png", "page2.png", "page3.png" ...]
character_bank = {
    "images": ["char1.png", "char2.png", "char3.png", "char4.png" ...],
    "names": ["Luffy", "Sanji", "Zoro", "Ussop" ...]
}

chapter_pages = [read_image(x) for x in chapter_pages]
character_bank["images"] = [read_image(x) for x in character_bank["images"]]

with torch.no_grad():
    per_page_results = model.do_chapter_wide_prediction(chapter_pages, character_bank, use_tqdm=True, do_ocr=True)

transcript = []
for i, (image, page_result) in enumerate(zip(chapter_pages, per_page_results)):
    model.visualise_single_image_prediction(image, page_result, f"page_{i}.png")
    speaker_name = {
        text_idx: page_result["character_names"][char_idx] for text_idx, char_idx in page_result["text_character_associations"]
    }
    for j in range(len(page_result["ocr"])):
        if not page_result["is_essential_text"][j]:
            continue
        name = speaker_name.get(j, "unsure") 
        transcript.append(f"<{name}>: {page_result['ocr'][j]}")
with open(f"transcript.txt", "w") as fh:
    for line in transcript:
        fh.write(line + "\n")
```

### License and Citation
The provided models and datasets are available for unrestricted use in personal, research, non-commercial, and not-for-profit endeavors. For any other usage scenarios, kindly contact me via email, providing a detailed description of your requirements, to establish a tailored licensing arrangement. My contact information can be found on [my website](https://ragavsachdeva.github.io/).

```
@InProceedings{magiv1,
    author    = {Sachdeva, Ragav and Zisserman, Andrew},
    title     = {The Manga Whisperer: Automatically Generating Transcriptions for Comics},
    booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
    month     = {June},
    year      = {2024},
    pages     = {12967-12976}
}

@misc{magiv2,
      title={Tails Tell Tales: Chapter-Wide Manga Transcriptions with Character Names}, 
      author={Ragav Sachdeva and Gyungin Shin and Andrew Zisserman},
      year={2024},
      eprint={2408.00298},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2408.00298}, 
}
```
