# stateready.py
# Patrick Souza <souza.patrick@gmail.com> for Prefiat LLC
# Opens system state file and parses parameters for operation.

import yaml
import states

class InvalidStateFileError(Exception):
    pass 

class MissingStateFileError(Exception):
    pass

def get_file_handle(state_file):
    try:
        file_handle = open(state_file, 'r')
        return file_handle
    except IOError:
        raise MissingStateFileError()

def parse_state_file(state_file):
    saved_state_file = get_file_handle(state_file)
            
    try:
        state_info = yaml.load(saved_state_file)
        
        since = state_info["since_local"]
        message = state_info["message"]
    
        if state_info["state"] == "okay":
            current_state = states.OKState(since, message)
        elif state_info["state"] == "warning":
            current_state = states.WarningState(since, message)
        elif state_info["state"] == "action":
            current_state = states.ActionState(since, message)
    except:
        raise InvalidStateFileError()
    
    saved_state_file.close()
    
    return current_state

# ToDo: Raise exception if type(since) != datetime


def open_file_for_save(state_file):
    file_handle = open(state_file, 'w')
    return file_handle

def yaml_dump(current_state):
    
    return yaml.dump({"state" : current_state.__class__.__name__, "since_local" : current_state.since, "message" : current_state.message}) 

def write_state_file(state_file, current_state):
    
    f = open_file_for_save(state_file)
    f.write(yaml_dump(current_state))
    f.close()