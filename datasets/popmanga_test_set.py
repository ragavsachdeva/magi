import os
import random
import numpy as np
import torch
from PIL import Image
from torch.utils.data import Dataset
import json

class PopMangaTest(Dataset):
    def __init__(self, path_to_dataset, split):
        self.path_to_dataset = path_to_dataset
        image_path_file = os.path.join(path_to_dataset, f"popmanga_test_annotations_released/{split}.txt")
        with open(image_path_file, "r") as fh:
            self.image_paths = [x.strip() for x in fh.readlines()]
    
    def __len__(self):
        return len(self.image_paths)

    def read_image(self, path_to_image):
        with open(path_to_image, "rb") as file:
            image = Image.open(file).convert("L").convert("RGB")
            image = np.array(image)
        return image
    
    def __getitem__(self, item_index):
        path_to_image = os.path.join(self.path_to_dataset, "popmanga_test", self.image_paths[item_index])
        page = self.read_image(path_to_image)
        annotations_path = os.path.join(self.path_to_dataset, "popmanga_test_annotations_released", self.image_paths[item_index]+".json")
        with open(annotations_path, "r") as fh:
            annotations = json.load(fh)
        magi_annotations = annotations["bbox_annotations"]
        character_clusters = annotations["character_clusters"]
        text_char_matches = annotations["text_to_character_matches"]
        return page, magi_annotations, character_clusters, text_char_matches
    
    def collate_fn(self, batch):
        return zip(*batch)

def visualise_dataset(
        path_to_dataset: str = "./",
        split: str = "unseen",
        num_images_to_visualise: int = 10,
):
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from tqdm import tqdm

    dataset = PopMangaTest(path_to_dataset, split)
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=4, shuffle=False, collate_fn=dataset.collate_fn, num_workers=0)
    for b, batch in enumerate(tqdm(dataloader)):
        image, magi_annotations, character_clusters, text_char_matches = batch

        all_labels = magi_annotations[0]["labels"]
        num_chars = all_labels.count(0)
        num_texts = all_labels.count(1)
        
        figure, subplot = plt.subplots(1, 1, figsize=(10, 10))
        subplot.imshow(image[0])

        bbox_colors = ["b", "r", "g"]
        for bbox, label in zip(magi_annotations[0]["bboxes_as_x1y1x2y2"], magi_annotations[0]["labels"]):
            x1, y1, x2, y2 = bbox
            subplot.add_patch(patches.Rectangle((x1, y1), x2 - x1, y2 - y1, linewidth=1, edgecolor=bbox_colors[label], facecolor="none"))
        
        for i, j in text_char_matches[0]:
            text_bbox = magi_annotations[0]["bboxes_as_x1y1x2y2"][i + num_chars]
            cxi, cyi = (text_bbox[0] + text_bbox[2]) / 2, (text_bbox[1] + text_bbox[3]) / 2
            char_bbox = magi_annotations[0]["bboxes_as_x1y1x2y2"][j]
            cxj, cyj = (char_bbox[0] + char_bbox[2]) / 2, (char_bbox[1] + char_bbox[3]) / 2
            subplot.plot([cxi, cxj], [cyi, cyj], color="green", linewidth=2, linestyle="solid")

        COLOURS = [
            "#b7ff51", # green
            "#f50a8f", # pink
            "#4b13b6", # purple
            "#ddaa34", # orange
            "#bea2a2", # brown
        ]
        colour_index = 0
        character_cluster_labels = character_clusters[0]
        unique_label_sorted_by_frequency = sorted(list(set(character_cluster_labels)), key=lambda x: character_cluster_labels.count(x), reverse=True)
        for label in unique_label_sorted_by_frequency:
            root = None
            others = []
            for i in range(num_chars):
                if character_cluster_labels[i] == label:
                    if root is None:
                        root = i
                    else:
                        others.append(i)
            if colour_index >= len(COLOURS):
                random_colour = COLOURS[0]
                while random_colour in COLOURS:
                    random_colour = "#" + "".join([random.choice("0123456789ABCDEF") for j in range(6)])
            else:
                random_colour = COLOURS[colour_index]
                colour_index += 1
            bbox_i = magi_annotations[0]["bboxes_as_x1y1x2y2"][root]
            x1 = bbox_i[0] + (bbox_i[2] - bbox_i[0]) / 2
            y1 = bbox_i[1] + (bbox_i[3] - bbox_i[1]) / 2
            subplot.plot([x1], [y1], color=random_colour, marker="o", markersize=5)
            for j in others:
                # draw line from centre of bbox i to centre of bbox j
                bbox_j = magi_annotations[0]["bboxes_as_x1y1x2y2"][j]
                x1 = bbox_i[0] + (bbox_i[2] - bbox_i[0]) / 2
                y1 = bbox_i[1] + (bbox_i[3] - bbox_i[1]) / 2
                x2 = bbox_j[0] + (bbox_j[2] - bbox_j[0]) / 2
                y2 = bbox_j[1] + (bbox_j[3] - bbox_j[1]) / 2
                subplot.plot([x1, x2], [y1, y2], color=random_colour, linewidth=2)
                subplot.plot([x2], [y2], color=random_colour, marker="o", markersize=5)

        plt.savefig(f"{b}.png", bbox_inches="tight", pad_inches=0)
        if b >= num_images_to_visualise:
            break

if __name__ == "__main__":
    from jsonargparse import CLI

    CLI(visualise_dataset)