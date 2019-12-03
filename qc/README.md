# QC methodology
This framework includes an automated procedure to evaluate the output of any rock classification model against a set of manually labeled images. This method of model evaluation enables direct quantitative and qualitative comparison between different models. The ability to do these direct comparisons is essential to make iterative improvements in the data pre-processing steps, the model methodology, and model tuning.

## QC Data
The manually labeled areas are within 10 different Landsat 8 scenes. The labels were produced by the authors of 

Burton-Johnson, A., Black, M., Fretwell, P. T., and Kaluza-Gilbert, J.: An automated methodology for differentiating rock from snow, clouds and sea in Antarctica from Landsat 8 imagery: a new rock outcrop map and area estimation for the entire Antarctic continent, The Cryosphere, 10, 1665–1677, https://doi.org/10.5194/tc-10-1665-2016, 2016. 

Any work that uses these manual labels must include a reference to the above publication.
Each area is 10 x 10 km (333 x 333 pixels) for a total of 1000km^2 or 1,108,890 pixels. The areas were selected from distal locations across Antarctica and represent a range of geology, geomorphology, and latitutde.

chunk_windows.json contains the relative location of the top left pixel of each manually labeled area within the respective Landsat scene.
