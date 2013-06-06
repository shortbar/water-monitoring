# statemanager.py
# Patrick Souza <souza.patrick@gmail.com> for Prefiat LLC
# Contains methods for operating state files

import yaml
import states

class InvalidStateFileError(Exception):
    pass 

class MissingStateFileError(Exception):
    pass

def parse_state_file(state_file):
    saved_state_file = _get_file_handle(state_file)
            
    try:
        current_state = yaml.load(saved_state_file)
    except:
        raise InvalidStateFileError()
    finally:
        saved_state_file.close()
    
    if isinstance(current_state, states.SystemState):
        return current_state
    else:
        raise InvalidStateFileError()

def write_state_file(state_file, current_state):
    f = _open_file_for_save(state_file)
    f.write(yaml.dump(current_state))
    f.close()
    
def write_state_stdout(current_state):
    print(yaml.dump(current_state))

def _get_file_handle(state_file):
    try:
        file_handle = open(state_file, 'r')
        return file_handle
    except IOError:
        raise MissingStateFileError()

# ToDo: Raise exception if type(since) != datetime

def _open_file_for_save(state_file):
    file_handle = open(state_file, 'w')
    return file_handle
