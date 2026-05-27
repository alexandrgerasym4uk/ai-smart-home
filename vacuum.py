import json
from devices.roborockS5max import VirtualRoborockS5Max

STATE_FILE = "state.json"

vacuum = VirtualRoborockS5Max()



def load_state():
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)



def default(state):
    data = load_state()

    if state:
        vacuum.app_start()
        data["vacuum"]["state"] = vacuum.state
    else:
        vacuum.app_stop()
        data["vacuum"]["state"] = vacuum.state

    save_state(data)


def go_home(*args):
    data = load_state()

    vacuum.app_charge()
    data["vacuum"]["state"] = vacuum.state

    save_state(data)

def set_vacuum_additional(param_type, param_value):
    data = load_state()
    if param_type == "fan":
        vacuum.set_custom_mode(param_value)
        data["vacuum"]["fan_power"] = param_value
    elif param_type == "water":
        vacuum.set_water_box_custom_mode = param_value
        data["vacuum"]["water_level"] = param_value
    save_state(data) 

