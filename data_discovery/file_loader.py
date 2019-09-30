import csv
import os


def load_scene_id_file(path):
    data = []
    with open(path, "r") as f:
        reader = csv.reader(f, delimiter='\t')
        data = [i for i in reader if i[0] != ""]
    return data


if __name__ == "__main__":
    scene_id_path = "/home/dsa/DSA/tc-10-1665-2016-supplement/Supplementary Material/Burton_Johnson_Tile_IDs.txt"

    scenes = load_scene_id_file(scene_id_path)
    for i in scenes:
        print(i)
