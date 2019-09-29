import os
from osgeo import gdal, ogr

img_src_dir = "/home/dsa/DSA/images/"
vector_src_dir = "/home/dsa/DSA/vectors/"
label_src_dir = "/home/dsa/DSA/labels/"


def get_image_paths(src_dir):
    img_dirs = os.listdir(img_src_dir)

    paths = {}

    for i in img_dirs:
        paths[i] = [img_src_dir + i + "/" + j for j in os.listdir(img_src_dir + i) if j[-4:] == ".TIF"]

    return paths


def get_vector_paths(src_dir):
    return [vector_src_dir + i for i in os.listdir(vector_src_dir) if i[-4:] == ".shp"]


def rasterize_label(raster_path, vector_path, label_path):
    raster_band = gdal.Open(raster_path, gdal.GA_ReadOnly)

    # Extract raster spatial metadata
    transform_parameters = raster_band.GetGeoTransform()
    projection = raster_band.GetProjection()

    raster_driver = gdal.GetDriverByName("GTiff")

    vector_layer_src = ogr.Open(vector_path)
    vector_layer = vector_layer_src.GetLayer()

    label_raster = raster_driver.Create(label_path,
                                        raster_band.RasterXSize,
                                        raster_band.RasterYSize,
                                        1,  # Raster band
                                        gdal.GDT_Float32)

    assert label_raster is not None

    label_raster.SetGeoTransform(transform_parameters)
    label_raster.SetProjection(projection)

    label_tile = label_raster.GetRasterBand(1)
    label_tile.Fill(0)

    gdal.RasterizeLayer(label_raster, [1], vector_layer, options=["ATTRIBUTE=GRIDCODE"])


img_paths = get_image_paths(img_src_dir)
vector_paths = get_vector_paths(vector_src_dir)

test_img_path = img_paths[list(img_paths.keys())[0]][0]

test_vector_path = vector_paths[0]

test_label_path = label_src_dir + list(img_paths.keys())[0] + "_label.tif"

rasterize_label(test_img_path, test_vector_path, test_label_path)

