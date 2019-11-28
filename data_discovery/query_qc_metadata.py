import csv
from db_config import LandsatDBCreator
import json


db_path = "/home/dsa/DSA/db/Image_IDs.db"
scene_file_path = "/home/dsa/DSA/qc_ids.txt"

db = LandsatDBCreator(db_path)
db.initialize_connection()
db.initialize_cursor()

with open(scene_file_path) as f:
    reader = csv.reader(f)
    scenes = [i[0] for i in reader if i]

print(scenes)
scene_match = "("
for i in scenes:
    scene_match += "'{}',".format(i)
scene_match = scene_match[:-1] + ")"
print(scene_match)

query = """
        SELECT * 
        FROM metadata
        WHERE sceneID in {}
        """.format(scene_match)
res = db.cursor.execute(query)
out = [i for i in res.fetchall()]
print(out)
