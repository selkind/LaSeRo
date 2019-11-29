# LaSeRo
## Landsat 8 Segmentation of Rock Outcrops

This is a research framework for geospatial analysis of Landsat 8 imagery. 

### Repository components
The framework consists of two sets of components. The first set of components make up
a data-preprocessing pipeline that is designed to prepare Landsat 8 imagery of Antarctica
for training with a Segnet semantic segmentation model. 

### The pre-processing steps are:
1. Download Landsat 8 scenes using tools from [landsat-utils](https://github.com/developmentseed/landsat-util).
 **This repository is due to be deprecated soon. We are only using a single component of it, so we have included that component directly in this repository**
2. Correct the raw DN values and brightness temperature values in each scene to TOA reflectance
and TOA brightness temperature values using the formulae described [here](https://www.usgs.gov/land-resources/nli/landsat/using-usgs-landsat-level-1-data-product)
3. A tool to burn shapefile features into a raster that has the same spatial extent of any
downloaded Landsat scenes. These rasterized features serve as labels of the Segnet training data.
