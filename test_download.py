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

    data_dir_path = "/proj/DBCal/"
    img_dir_path = "landsat_images"

    db_path = "/users/dibu25/workspace/img_metadata/scenes.db"

    db = LandsatDBCreator(db_path)
    db.initalize_cursor()

    scene_id_query = """
                    SELECT ID FROM
                    scene_ids
                    LIMIT 1
			"""

    db.cursor.execute(scene_id_query)




    test_scene_id = db.cursor.fetchone()[0]
    print(test_scene_id)
    data_dir_path = "/proj/DBCal/"
    img_dir_path = "landsat_images"
    downloader = Downloader(download_dir=data_dir_path + img_dir_path)

    downloader.download([test_scene_id])
