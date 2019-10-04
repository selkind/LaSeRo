import sqlite3
# set cwd one level up
import sys, os

sys.path.append(os.path.abspath('../landsat-util'))
from data_discovery.db_config import LandsatDBCreator
from landsat.downloader import *


def load_api_key(path):
    key = []
    with open(path, 'r') as f:
        key.append(f.readline()[:-1])
        key.append(f.readline()[:-1])
    return key


if __name__ == "__main__":
    key_store_path = "/home/dsa/Documents/project/lasero/keys/"
    usgs_key_file = "usgs.key"

    data_dir_path = "/home/dsa/DSA/"
    db_path = "db/Image_IDs.db"
    img_dir_path = "images"

    usgs_key = load_api_key(key_store_path + usgs_key_file)

    db = LandsatDBCreator(data_dir_path + db_path)
    db.initialize_connection()
    db.initalize_cursor()

    downloader = Downloader(download_dir=data_dir_path + img_dir_path, usgs_user=usgs_key[0], usgs_pass=usgs_key[1])
    print(downloader.usgs_user)
