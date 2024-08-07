# [The Manga Whisperer: Automatically Generating Transcriptions for Comics (CVPR'24)](http://arxiv.org/abs/2401.10224)

[![Static Badge](https://img.shields.io/badge/arXiv-2401.10224-blue)](http://arxiv.org/abs/2401.10224)
[![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fhuggingface.co%2Fapi%2Fmodels%2Fragavsachdeva%2Fmagi%3Fexpand%255B%255D%3Ddownloads%26expand%255B%255D%3DdownloadsAllTime&query=%24.downloadsAllTime&label=%F0%9F%A4%97%20Downloads)](https://huggingface.co/ragavsachdeva/magi)

[Ragav Sachdeva](https://ragavsachdeva.github.io/), [Andrew Zisserman](https://scholar.google.com/citations?hl=en&user=UZ5wscMAAAAJ)

TODOs (by first week of Aug 2024): 
- [ ] Upload Magiv2 model,
- [ ] provide new annotations,
- [ ] open-source PopCharacters dataset,
- [ ] release evaluation scripts.

### TLDR
- The model is available at 🤗 [HuggingFace Model Hub](https://huggingface.co/ragavsachdeva/magi).
- Try it out for yourself using this 🤗 [HuggingFace Spaces Demo](https://huggingface.co/spaces/ragavsachdeva/the-manga-whisperer/) (no GPU, so slow).
- Dataset info is available [here](datasets/).
- Basic model usage is provided below. Inspect [this file](https://huggingface.co/ragavsachdeva/magi/blob/main/modelling_magi.py) for more info.

![Magi_teaser](https://github.com/ragavsachdeva/magi/assets/26804893/0a6d44bc-12ef-4545-ab9b-577c77bdfd8a)


### Usage
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

### License and Citation
The provided model and datasets are available for unrestricted use in personal, research, non-commercial, and not-for-profit endeavors. For any other usage scenarios, kindly contact me via email, providing a detailed description of your requirements, to establish a tailored licensing arrangement. My contact information can be found on [my website](https://ragavsachdeva.github.io/).

```
@misc{sachdeva2024manga,
      title={The Manga Whisperer: Automatically Generating Transcriptions for Comics}, 
      author={Ragav Sachdeva and Andrew Zisserman},
      year={2024},
      eprint={2401.10224},
      archivePrefix={arXiv},
      primaryClass={cs.CV}
}
```
