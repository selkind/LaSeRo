import os
import json

import numpy as np


def calculate_results(diff_histogram):
    """
    @param diff_histogram: np.histogram of a 2-class diff raster between a model prediction
    and the underlying ground-truth

    @returns dict: lots of metrics that describe the quality of the prediction

    **NOTE** This will eventually need to be generalized to an n-class diff raster
    """

    stats = {}
    stats["total_pixels"] = diff_histogram[0] + diff_histogram[1] + diff_histogram[2] + diff_histogram[3]
    stats["correct"] = diff_histogram[0] + diff_histogram[3]
    stats["incorrect"] = diff_histogram[1] + diff_histogram[2]
    
    stats["notrock"] = diff_histogram[0]
    stats["false_notrock"] = diff_histogram[1]
    stats["false_rock"] = diff_histogram[2]
    stats["rock"] = diff_histogram[3]
                    
    stats["accuracy"] = stats["correct"] / stats["total_pixels"]
    stats["classification_accuracy"] = stats["rock"] / (stats["rock"] + stats["false_rock"] + stats["false_notrock"])
    stats["rock_omission"] = diff_histogram[1] / (diff_histogram[1] + diff_histogram[3])
    stats["rock_commission"] = diff_histogram[2] / (diff_histogram[2] + diff_histogram[3])
    stats["notrock_omission"] = diff_histogram[2] / (diff_histogram[0] + diff_histogram[2])
    stats["notrock_commission"] = diff_histogram[1] / (diff_histogram[0] + diff_histogram[1])
    stats["f1_rock"] = 2 * ((stats["rock_omission"] * stats["rock_commission"]) / (stats["rock_omission"] + stats["rock_commission"]))

    stats["rock_producers"] = diff_histogram[3] / (diff_histogram[1] + diff_histogram[3]) * 100
    stats["notrock_producers"] = diff_histogram[0] / (diff_histogram[0] + diff_histogram[2]) * 100
    stats["rock_users"] = diff_histogram[3] / (diff_histogram[2] + diff_histogram[3]) * 100
    stats["notrock_users"] = diff_histogram[0] / (diff_histogram[0] + diff_histogram[1]) * 100

    return stats

class TestRegion:
    def __init__(self, test_region_window_path, groundtruth_source_dir='/content/drive/My Drive/qc/manual_labels'):
        self.window_path = test_region_window_path
        self.window = self.load_window(self.window_path)

        self.groundtruth_source_dir = groundtruth_source_dir
        self.groundtruth = {}

    @staticmethod
    def load_window(path):
        with open(path, 'r') as f:
            return json.load(f)

    def load_groundtruth(self):
        for i in self.window:
            self.groundtruth[i] = np.load(os.path.join(self.groundtruth_source_dir, f'{i}_man.npy'))


    def assemble_test_region_mosaic(self, raster_source_dir, test_region_window, source_suffix='output'):
        row_vals = [i[0] for i in test_region_window['chunks']]
        col_vals = [i[1] for i in test_region_window['chunks']]
        row_range = (min(row_vals), max(row_vals))
        col_range = (min(col_vals), max(col_vals))
    
        mosaic_rows = []
        for i in range(row_range[0], row_range[1] + 1):
            row = []
            for j in range(col_range[0], col_range[1] + 1):
                row.append(np.load(os.path.join(raster_source_dir, "chunk_{}_{}{}.npy".format(i, j, source_suffix))))
            
            mosaic_rows.append(np.concatenate(tuple(row), axis=1))
        
        mosaic = np.concatenate(tuple(mosaic_rows), axis=0)
        
        return mosaic[test_region_window["row"]: test_region_window["row"] + test_region_window["height"],
                                test_region_window["col"]: test_region_window["col"] + test_region_window["width"]]


    def load_output_mosaics(self, output_dir):
        """
        @param output_dir: string, the path to the directory where rasters generated by a model's
        predictions are stored in directories by scene_id/chunk_row_col_output.npy
        
        @returns dict containing numpy arrays
        """
        mosaics = {}
        
        for i in self.window:
            if i == 'ryder_bay_abj':
                scene_dir = os.path.join(output_dir, "LC82201072015017LGN0")
            else:
                scene_dir = os.path.join(output_dir, i)

            if os.path.exists(scene_dir) and len(os.listdir(scene_dir)) > 0:
                mosaics[i] = self.assemble_test_region_mosaic(scene_dir, self.window[i])

        return mosaics
