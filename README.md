# LaSeRo
## Landsat 8 Segmentation of Rock Outcrops

This is a research framework for geospatial analysis of Landsat 8 imagery. 

### Repository components
The framework consists of two sets of components. The first set of components make up
a data-preprocessing pipeline that is designed to prepare Landsat 8 imagery of Antarctica
for training with a Segnet semantic segmentation model. 

### The pre-processing steps are:
1. Download Landsat 8 scenes using tools from [landsat-utils](https://github.com/developmentseed/landsat-util).
 **This repository is due to be deprecated soon. We are only using a single component of it, so we have included that component directly in this repository in [this directory](https://github.com/selkind/LaSeRo/tree/master/data_preprocessing/landsat_download)**
2. (Optional) Correct the raw DN values and brightness temperature values in each scene to TOA reflectance
and TOA brightness temperature values using the formulae described [here](https://www.usgs.gov/land-resources/nli/landsat/using-usgs-landsat-level-1-data-product)
3. Generate labels for each Landsat scene by converting feature shapefiles into raster layers. A tool to burn shapefile features into a raster that has the same spatial extent of any downloaded scene. These rasterized features serve as labels of the Segnet training data. The rasterize function is located in data_preprocessing/utils/raster_tools.py
4. Combine all band TIFs from a scene into a stacked numpy array and break the stack and label layer into chunks of 512 X 512 pixels and save them as pickled .npy files. A function to do this step is in data_preprocessing/utils/raster_tools.py.

#### Once the scenes are stacked and chunked into .npy files, they are ready for model training.

### The training steps are:
1. Generate a model data text file that contains all paths to the chunks that will be used for training.
