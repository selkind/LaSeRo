import os
import csv

def create_session_paths(session_name, base_dir='/content/drive/My Drive'):
    models_dir = os.path.join(base_dir, 'models')
    session_dir = os.path.join(models_dir, session_name)

    if not os.path.isdir(session_dir):
        os.mkdir(session_dir)
    
    model = os.path.join(session_dir, f'{session_name}.h5')
    history = os.path.join(session_dir, 'history.json')
    training_log = os.path.join(session_dir, 'logs.csv')
    training_config = os.path.join(session_dir, 'config.json')
    classification_report = os.path.join(session_dir, 'classification_report.txt')

    return {'model': model,
            'history': history,
            'logs': training_log,
            'config': training_config,
            'classification_report': classification_report}

def get_image_list(metadata_file_path):
    with open(metadata_file_path, 'r') as f:
        return [i for i in csv.reader(f) if i]

def make_segnet_imput_file(chunk_dir, scene_ids, out_path):
    """
    This script takes a list of scene ids and creates a file that can be used as input for a segnet model
    @param string chunk_dir: The abspath base directory where each set of chunks for a scene has its own dir named with its sceneID
    @param list scene_ids: A list of sceneIDs that exist in the chunk_dir. The chunks of these scenes will be used in the file.
    @param string out_path: The abspath where the resulting file should be saved.
    @return int lines_written: the total number of lines (corresponding to a data and label chunk path) in the file.
    file format:
    /path/to/scene_chunk.npy,/path/to/scene_chunk_label.npy
    /path/to/scene_chunk.npy,/path/to/scene_chunk_label.npy
    /path/to/scene_chunk.npy,/path/to/scene_chunk_label.npy
    ...
    """
    existing_scenes = [i for i in os.listdir(chunk_dir) if os.path.isdir(os.path.join(chunk_dir, i))]
    # filter out ids that don't exist in the given dir
    scene_ids = [i for i in scene_ids if i in existing_scenes]
    print(scene_ids)

    lines_to_write = []

    for i in scene_ids:
        scene_dir = os.path.join(chunk_dir, i)
        for j in os.listdir(scene_dir):
            if j[-9:] != "label.npy":
                data_path = os.path.join(scene_dir, j)
                file_split = os.path.splitext(j)
                label_path = os.path.join(scene_dir, file_split[0] + "_label" + file_split[1])

                lines_to_write.append("{},{}\n".format(data_path, label_path))

    with open(out_path, 'w+') as output:
        output.writelines(lines_to_write)

    return len(lines_to_write)