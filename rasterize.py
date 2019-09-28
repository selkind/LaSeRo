import os
from osgeo import gdal, ogr

src_dir = "/home/dsa/DSA/images/"

img_dirs = os.listdir(src_dir)

for i in img_dirs:
    band_files_names = [src_dir + i + "/" + j for j in os.listdir(src_dir + i) if j[-4:] == ".TIF"]

    for k in band_files_names:
        print(k)

tile = "/home/dsa/DSA/LC08_LIGT_209117_20140101_20170427_01_T2.tar/"