import csv
from data_discovery.db_config import LandsatDBCreator


def load_scene_id_file(path):
    data = []
    with open(path, "r") as f:
        reader = csv.reader(f, delimiter='\t')
        data = [i for i in reader if i[0] != ""]
    return data


def format_value(row):
    return "({},{},{},{},{},{},{},{}),".format(row[0],row[1],row[2],row[3],row[4],row[5],
                                              row[6],row[7])


def populate_scene_id_table(db_manager, data):
    query = """
    INSERT INTO scene_ids 
                (scene, WRS_Path, WRS_Row, Date, TIME, Solar_Azimuth, Solar_Elev, Cloud_Cover)
            VALUES
            """
    for i in data:
        query += format_value(i) + "\n"
    query = query[:-2] + ";"
    db_manager.cursor.execute(query)
    db_manager.commit()


if __name__ == "__main__":
    scene_id_path = "/home/dsa/DSA/tc-10-1665-2016-supplement/Supplementary Material/Burton_Johnson_Tile_IDs.txt"
    db_dir = "/home/dsa/DSA/db/Image_IDs.db"
    db_manager = LandsatDBCreator(db_dir)
    db_manager.initialize_connection()
    db_manager.initalize_cursor()

    scenes = load_scene_id_file(scene_id_path)
    populate_scene_id_table(db_manager, scenes)

    db_manager.cursor.execute("SELECT * FROM scene_ids")
    results = db_manager.cursor.fetchall()
    for i in results:
        print(i)

