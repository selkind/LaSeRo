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