import os
from itertools import product
import numpy as np
import rasterio as rio
import rasterio.windows as wnd
import rasterio.mask
from rasterio import features
import fiona
from progress.bar import FillingSquaresBar


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


"""
For a single scene: Create band stacks, load labels, break stacks and labels into chunks of N X M pixels.
Saves output as pickled numpy arrays. 
"""
def make_stacked_chunks(data_manager, scene_id, chunk_width=512, chunk_height=512):
    label_path = os.path.join(data_manager.label_dir, i + "_label.TIF")
    with rio.open(label_path) as label_file:
        label = label_file.read(1)

    band_rasters = []
    for b in bands:
        band_path = os.path.join(data_manager.raw_image_dir, i, "{}_B{}.TIF".format(i, b))
        with rio.open(band_path) as band_file:
            band_rasters.append(band_file.read(1))

    band_stack = np.stack(band_rasters, axis=0).transpose(1,2,0)
    band_rasters.clear()

    scene_height = band_stack.shape[0]
    scene_width = band_stack.shape[1]

    vertical_chunks = scene_height // chunk_height
    horizontal_chunks = scene_width // chunk_width

    scene_chunk_dir = os.path.join(data_manager.stack_dir, i)
    if not os.path.exists(scene_chunk_dir):
        os.mkdir(scene_chunk_dir)

    with FillingSquaresBar('Processing', max=vertical_chunks * horizontal_chunks) as bar:
        for j in range(vertical_chunks):
            for k in range(horizontal_chunks):
                row_index = j * chunk_height
                col_index = k * chunk_width

                band_chunk = band_stack[row_index: row_index + chunk_height, col_index: col_index + chunk_width, :]
                label_chunk = label[row_index: row_index + chunk_height, col_index: col_index + chunk_width]

                data_pixels = np.where(band_chunk > 0)
                data_pixel_count = np.sum(data_pixels)

                band_chunk_path = os.path.join(scene_chunk_dir, "chunk_{}_{}.npy".format(j, k))
                label_chunk_path = os.path.join(scene_chunk_dir, "chunk_{}_{}_label.npy".format(j, k))

                if data_pixel_count > 0:
                    np.save(band_chunk_path, band_chunk, allow_pickle=True)
                    np.save(label_chunk_path, label_chunk, allow_pickle=True)
                bar.next()
