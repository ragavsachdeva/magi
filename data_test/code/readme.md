# Datasets

Disclaimer: In adherence to copyright regulations, we are unable to _publicly_ distribute the manga images that we've collected. The test images, however, are available freely, publicly and officially on [Manga Plus by Shueisha](https://mangaplus.shueisha.co.jp/).

**Download Instructions**
```
pip install jsonargparse mloader
python download_test_sets.py --path_to_dataset_folder <destination>
```

**Visualise to Verify**
```
python popmanga_test_set.py --path_to_dataset <destination> --split [seen/unseen]
```

## Other notes
- Request to download Manga109 dataset [here](http://www.manga109.org/en/download.html).
- Download a large scale dataset from Mangadex using [this tool](https://github.com/EMACC99/mangadex).
- The Manga109 test splits are available here: [detection](https://github.com/barisbatuhan/DASS_Det_Inference/blob/main/dass_det/data/datasets/manga109.py#L109), [character clustering](https://github.com/kktsubota/manga-face-clustering/blob/master/dataset/test_titles.txt). Be careful that some background characters have the same label even though they are not the same character, [see](https://github.com/kktsubota/manga-face-clustering/blob/master/script/get_other_ids.py).

