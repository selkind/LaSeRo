.mode csv
/* import scene_id data to non-existing table scene_ids */
.separator "\t"
/* update file path before use */
.import "/users/dibu25/workspace/img_metadata/Burton_Johnson_scenes.txt" scene_ids

/* import Landsat Bulk Metadata to non-existing table metadata 
.separator ","
.import /home/dsa/DSA/Landsat_8_C1.csv metadata
*/

