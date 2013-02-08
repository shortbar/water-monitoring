import yaml

def get_file_handle():
    return file('state.yaml', 'r')

def get_file_state():
    saved_state_file = get_file_handle()
    obj = yaml.load(saved_state_file)
    