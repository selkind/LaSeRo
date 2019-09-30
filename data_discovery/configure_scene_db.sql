.mode csv
/* import scene_id data to non-existing table scene_ids */
.separator "\t"
/* update file path before use */
.import "/home/dsa/DSA/tc-10-1665-2016-supplement/Supplementary Material/Burton_Johnson_Tile_IDs.txt" scene_ids

/* import Landsat Bulk Metadata to non-existing table metadata */
.separator ","
.import /home/dsa/DSA/Landsat_8_C1.csv metadata

