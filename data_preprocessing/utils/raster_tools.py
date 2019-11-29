import os
from itertools import product
import numpy as np
import rasterio as rio
import rasterio.windows as wnd
import rasterio.mask
from rasterio import features
import fiona


"""
This function is used to read a window (or segment) of an entire raster tile.

@param string file_path: The path to the raster dataset
@param int width: Width of the desired window in number of pixels
@param int height: Height of the desired window in number of pixels
@param int col_off: The column offset of the top left corner of the desired window
                    from the input raster origin. 
@param int row_off: The row offset of the top left corner of the desired window
                    from the input raster origin. 

@returns tuple (np_array, rasterio_dataset_metadata) array of size (width, height, input_raster_depth)
"""
def get_window(file_path, width=512, height=512, col_off=0, row_off=0):
    with rio.open(file_path) as data:
        meta = data.meta.copy()

        ncols, nrows = meta['width'], meta['height']
        offsets = product(range(0, ncols, width), range(0, nrows, height))

        full_image = wnd.Window(col_off=0, row_off=0, width=ncols, height=nrows)

        window = wnd.Window(col_off=col_off * width, row_off=row_off * height,
                            width=width, height=height).intersection(full_image)

        transform = wnd.transform(window, meta['transform'])

        meta['transform'] = transform
        meta['width'], meta['height'] = window.width, window.height

        return data.read(window=window).transpose(1, 2, 0), meta


"""
Creates a binary raster. 1s represent pixels intersecting with the input shape. 0s represent
pixels disjoint from the input shape.
"""
def rasterize_label(raster_path, vector_path):
    with fiona.open(vector_path) as vectors:
        shapes = [features['geometry'] for features in vectors]

    with rio.open(raster_path) as base:
        meta = base.meta.copy()
        output = (rasterio.mask.mask(base, shapes, crop=True, indexes=1)[0] > 0).astype(rio.uint8)
        output = np.expand_dims(output, axis=0)
    return output, meta

