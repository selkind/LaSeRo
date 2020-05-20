import os

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