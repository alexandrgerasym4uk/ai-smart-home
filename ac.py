import json
from devices.cooperHunter import VirtualCooperHunterAC

ac = VirtualCooperHunterAC()

STATE_FILE = "state.json"

def load_state():
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def default(state):
    data = load_state()

    if not state:
        set_ac_power(False, 0)

        data["ac"]["is_on"] = False

        save_state(data)

def set_ac_power(state: bool, temp=0):

    data = load_state()

    if state:
        temp = int(temp)

        ac.toggle(True)
        data["ac"]["is_on"] = True

        if 16 <= temp <= 30:
            ac.set_temperature(temp)
            data["ac"]["temperature"] = temp

    elif state == 0:

        ac.toggle(False)
        data["ac"]["is_on"] = False

    else:
        ac.set_temperature(temp)

    save_state(data)

def set_ac_additional(param_type, param_value):
    data = load_state()
    if param_type == "mode":
        ac.set_mode(param_value)
        data["ac"]["mode"] = param_value
    elif param_type == "fan_speed":
        ac.fan_speed = param_value
        data["ac"]["fan_speed"] = param_value
    elif param_type == "swing":
        ac.set_swing(param_value)
        data["ac"]["swing"] = param_value
    save_state(data)
