import yaml

def get_file_handle(state_file):
    f = open(state_file, 'r')
    return f

def parse_state_file(state_file):
    saved_state_file = get_file_handle(state_file)
    state_info = yaml.load(saved_state_file)
    return state_info

    
    