# [The Manga Whisperer: Automatically Generating Transcriptions for Comics](http://arxiv.org/abs/2401.10224)

[[arXiv]](http://arxiv.org/abs/2401.10224)

[Ragav Sachdeva](https://ragavsachdeva.github.io/), [Andrew Zisserman](https://scholar.google.com/citations?hl=en&user=UZ5wscMAAAAJ)

### TLDR
- The model is available at 🤗 [HuggingFace Model Hub](https://huggingface.co/ragavsachdeva/magi).
- Try it out for yourself using this 🤗 [HuggingFace Spaces Demo](https://huggingface.co/spaces/ragavsachdeva/the-manga-whisperer/).
- Dataset is coming soon.
- Basic model usage is provided below, more details to follow.

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

### Citation
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
