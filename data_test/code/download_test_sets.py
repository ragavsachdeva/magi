import os

manga_plus_links = [
        "https://mangaplus.shueisha.co.jp/viewer/1000001",
        "https://mangaplus.shueisha.co.jp/viewer/1000002",
        "https://mangaplus.shueisha.co.jp/viewer/1000177",
        "https://mangaplus.shueisha.co.jp/viewer/1000178",
        "https://mangaplus.shueisha.co.jp/viewer/1000390",
        "https://mangaplus.shueisha.co.jp/viewer/1000391",
        "https://mangaplus.shueisha.co.jp/viewer/1001249",
        "https://mangaplus.shueisha.co.jp/viewer/1001250",
        "https://mangaplus.shueisha.co.jp/viewer/1000260",
        "https://mangaplus.shueisha.co.jp/viewer/1000261",
        "https://mangaplus.shueisha.co.jp/viewer/1000762",
        "https://mangaplus.shueisha.co.jp/viewer/1000763",
        "https://mangaplus.shueisha.co.jp/viewer/1000338",
        "https://mangaplus.shueisha.co.jp/viewer/1000339",
        "https://mangaplus.shueisha.co.jp/viewer/1000346",
        "https://mangaplus.shueisha.co.jp/viewer/1000347",
        "https://mangaplus.shueisha.co.jp/viewer/1001279",
        "https://mangaplus.shueisha.co.jp/viewer/1001280",
        "https://mangaplus.shueisha.co.jp/viewer/1000303",
        "https://mangaplus.shueisha.co.jp/viewer/1000304",
        "https://mangaplus.shueisha.co.jp/viewer/1000397",
        "https://mangaplus.shueisha.co.jp/viewer/1000398",
        "https://mangaplus.shueisha.co.jp/viewer/1000486",
        "https://mangaplus.shueisha.co.jp/viewer/1000487",
        "https://mangaplus.shueisha.co.jp/viewer/1000601",
        "https://mangaplus.shueisha.co.jp/viewer/1000602",
        "https://mangaplus.shueisha.co.jp/viewer/1000184",
        "https://mangaplus.shueisha.co.jp/viewer/1000185",
        "https://mangaplus.shueisha.co.jp/viewer/1000326",
        "https://mangaplus.shueisha.co.jp/viewer/1000327",
        "https://mangaplus.shueisha.co.jp/viewer/1000227",
        "https://mangaplus.shueisha.co.jp/viewer/1000228",
        "https://mangaplus.shueisha.co.jp/viewer/1000310",
        "https://mangaplus.shueisha.co.jp/viewer/1000311",
        "https://mangaplus.shueisha.co.jp/viewer/1000665",
        "https://mangaplus.shueisha.co.jp/viewer/1000666",
        "https://mangaplus.shueisha.co.jp/viewer/1008468",
        "https://mangaplus.shueisha.co.jp/viewer/1008469",
        "https://mangaplus.shueisha.co.jp/viewer/1000442",
        "https://mangaplus.shueisha.co.jp/viewer/1000443",
        "https://mangaplus.shueisha.co.jp/viewer/1000549",
        "https://mangaplus.shueisha.co.jp/viewer/1000550",
        "https://mangaplus.shueisha.co.jp/viewer/1013146",
        "https://mangaplus.shueisha.co.jp/viewer/1013149",
        "https://mangaplus.shueisha.co.jp/viewer/1018870",
        "https://mangaplus.shueisha.co.jp/viewer/1018858",
        "https://mangaplus.shueisha.co.jp/viewer/1001834",
        "https://mangaplus.shueisha.co.jp/viewer/1001835",
        "https://mangaplus.shueisha.co.jp/viewer/1001296",
        "https://mangaplus.shueisha.co.jp/viewer/1001297",
    ]

def download_test_set(
        path_to_dataset_folder: str = "./"
    ):

    os.makedirs(path_to_dataset_folder, exist_ok=True)
    print("Downloading images from MangaPlus. Temporarily stored in ./mloader_downloads.")
    for link in manga_plus_links:
        os.system(f"mloader {link} --raw --chapter-subdir")
    
    os.system("mv mloader_downloads popmanga_test")
    
    print(f"Moving images to {path_to_dataset_folder}")
    os.system(f"mv popmanga_test {path_to_dataset_folder}")
    
    print("Downloading annotations...")
    os.system(f"wget https://thor.robots.ox.ac.uk/magi/popmanga_test_annotations_released_13_03_24.tar.gz")
    
    print("Extracting annotations...")
    os.system(f"tar -xvzf popmanga_test_annotations_released_13_03_24.tar.gz")
    os.system(f"rm popmanga_test_annotations_released_13_03_24.tar.gz")
    
    print("Moving annotations to the dataset folder...")
    os.system(f"mv popmanga_test_annotations_released {path_to_dataset_folder}")
    
    print("Done.")

if __name__ == "__main__":
    from jsonargparse import CLI

    CLI(download_test_set)
