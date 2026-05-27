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

    data["ventilation"] = int(state)

    print(f"[VENT] Витяжка в туалеті: {'ПРАЦЮЄ' if state else 'ЗУПИНЕНО'}")

    save_state(data)