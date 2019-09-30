import sqlite3


class LandsatDBCreator:
    SCENE_ID_TABLE = "CREATE TABLE scene_ids(id integer PRIMARY KEY AUTOINCREMENT, scene text," \
                     " WRS_Path integer, WRS_Row integer, Date DATE, Time TIME, Solar_Azimuth FLOAT, " \
                     "Solar_Elev FLOAT, Cloud_Cover FLOAT)"

    def __init__(self, database_path):
        self.db_path = database_path
        self.con = None
        self.cursor = None

    def initialize_connection(self):
        try:
            self.con = sqlite3.connect(self.db_path)
            return True
        except sqlite3.Error as e:
            print(e)
            return False

    def initalize_cursor(self):
        self.cursor = self.con.cursor()

    def create_table(self, table_query):
        cursor = self.con.cursor()
        cursor.execute(self.SCENE_ID_TABLE)
        self.con.commit()

    def create_table_from_headers(self, headers):
        metadata_table_query = """
                                CREATE TABLE metadata
                                (
                              """
        for i in headers:
            metadata_table_query += ","


if __name__ == "__main__":
    db_dir = "/home/dsa/DSA/db/Image_IDs.db"
    db_manager = LandsatDBCreator(db_dir)
    db_manager.initialize_connection()
    db_manager.initalize_cursor()
    db_manager.create_table(db_manager.SCENE_ID_TABLE)
    db_manager.cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
    table_query = db_manager.cursor.fetchall()
    for row in table_query:
        print(row)


