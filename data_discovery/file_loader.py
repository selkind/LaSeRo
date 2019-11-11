import csv
from data_discovery.db_config import LandsatDBCreator


def load_scene_id_file(path, delimiter):
    with open(path, "r") as f:
        reader = csv.reader(f, delimiter=delimiter)
        data = [i for i in reader if i[0] != ""]
    return data


def load_headers(path, delimiter):
    with open(path, "r") as f:
        reader = csv.reader(f, delimiter=delimiter)
        return next(reader, None)


"""
Takes array of data loaded from Burton-Johnson scene id file
available in the supplementary material
download here: https://www.the-cryosphere.net/10/1665/2016/
@:param db_manager LandsatDBCreator instance with table scene_ids
table created
@:param data list Data loaded from file
@:returns void

"""


def populate_scene_id_table(db_manager, data):
    query = """
    INSERT INTO scene_ids 
                (scene, WRS_Path, WRS_Row, Date, TIME, Solar_Azimuth, Solar_Elev, Cloud_Cover)
            VALUES (? ?,?,?,?,?,?,?)
            """
    for i in data:
        db_manager.cursor.execute(query, i)
    db_manager.con.commit()


def initialize_db(path):
    scene_db_manager = LandsatDBCreator(path)
    scene_db_manager.initialize_connection()
    scene_db_manager.initialize_cursor()
    return scene_db_manager


def load_data(scene_id_file_path, metadata_file_path, db_path):
    scenes = load_scene_id_file(scene_id_file_path, '\t')
    scene_db = initialize_db(db_path)

    # omit header line from insert statement
    populate_scene_id_table(scene_db, scenes[1:])


if __name__ == "__main__":
    base_dir = "/home/dsa/DSA/"
    scene_id_path = base_dir + "tc-10-1665-2016-supplement/Supplementary Material/Burton_Johnson_Tile_IDs.txt"
    db_dir = base_dir + "db/Image_IDs.db"
    metadata_path = base_dir + "LANDSAT_8_C1.csv"
    headers = load_headers(metadata_path, ',')
    print(len(headers))

    # load_data(scene_id_path, None, db_dir)


