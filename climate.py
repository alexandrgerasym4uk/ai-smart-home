import json

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
        set_floor_power(False, 0)

        data["climate"]["state"] = 0
        data["climate"]["power"] = 0

        save_state(data)


def set_floor_power(state: bool, power=0):

    data = load_state()

    if state:
        power = int(power)


        data["climate"]["state"] = 1

        if 0 <= power <= 100:
            data["climate"]["power"] = power

    else:
        data["climate"]["state"] = 0

    save_state(data)