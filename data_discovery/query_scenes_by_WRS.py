import csv
from db_config import LandsatDBCreator


db_path = "/home/dsa/DSA/db/Image_IDs.db"
scene_file_path = "/home/dsa/DSA/good_scenes.txt"

db = LandsatDBCreator(db_path)
db.initialize_connection()
db.initialize_cursor()

WRS_combo_path = "/home/dsa/DSA/vectors/WRS_vals.csv"

# combine path and row values into a single string
with open(WRS_combo_path, 'r') as wrs_file:
    reader = csv.reader(wrs_file)
    next(reader)
    wrs_combos = [i[0] + i[1] for i in reader if i]

print(len(wrs_combos))
# format list of strings into single string appropriate for "WHERE in ()" sql query
wrs_match = "("
for i in wrs_combos:
    wrs_match += "'{}',".format(i)
wrs_match = wrs_match[:-1] + ')'

query = """
        SELECT ID 
        FROM scene_ids 
        WHERE WRS_Path || WRS_Row in {} 
        AND cast(Cloud_Cover AS FLOAT) < 10""".format(wrs_match)
res = db.cursor.execute(query)
scenes = [i[0] for i in res.fetchall()]

# output scenes to file
with open(scene_file_path, 'w+') as out_file:
    for i in scenes:
        out_file.write(i + "\n")
