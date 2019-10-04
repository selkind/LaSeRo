import sqlite3
# set cwd one level up
import sys, os
sys.path.append(os.path.abspath('../landsat-util'))
print(sys.path)
from data_discovery.db_config import LandsatDBCreator
from landsat.downloader import *

