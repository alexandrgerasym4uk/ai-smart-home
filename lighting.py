import requests
import subprocess
import re
import json


STATE_FILE = "state.json"

def load_state():
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

def lookup_mac_in_cache(target_mac):
    output = subprocess.check_output(("arp", "-a")).decode("ascii")
    pattern = r"\((.*?)\) at " + target_mac.lower()
    match = re.search(pattern, output.lower())

    if match:
        return match.group(1)
    return None


ip = lookup_mac_in_cache('e8:68:e7:c8:45:fe')


def set_light_state(room_name, state):
    status = "on" if state else "off"

    print(f"[LIGHT] {room_name}: {status}")

    requests.get(f"http://{ip}/sw/{room_name}/{status}")

    data = load_state()
    data["lighting"][room_name] = int(state)
    save_state(data)

    print("[STATE UPDATED]", data)



def toggle_living_room(state: bool, *args):
    set_light_state("vitalnya", state)


def toggle_kitchen(state: bool, *args):
    set_light_state("kukhnya", state)


def toggle_bedroom(state: bool, *args):
    set_light_state("spalnya", state)


def toggle_wardrobe(state: bool, *args):
    set_light_state("garderob", state)


def toggle_bedside_1(state: bool, *args):
    set_light_state("lampa1", state)


def toggle_bedside_2(state: bool, *args):
    set_light_state("lampa2", state)


def toggle_kitchen_counter(state: bool, *args):
    set_light_state("stilnitsya", state)


def toggle_shelf_light(state: bool, *args):
    set_light_state("polytsi", state)


def default(state):
    funcs = [
        toggle_living_room,
        toggle_kitchen,
        toggle_bedroom,
        toggle_wardrobe,
        toggle_bedside_1,
        toggle_bedside_2,
        toggle_kitchen_counter,
        toggle_shelf_light
    ]

    for func in funcs:
        func(1 if state else 0)