import requests
import subprocess
import re


def default(state):
    if state:
        toggle_living_room(1)
        toggle_kitchen(1)
        toggle_bedroom(1)
        toggle_wardrobe(1)
        toggle_bedside_1(1)
        toggle_bedside_2(1)
        toggle_kitchen_counter(1)
        toggle_shelf_light(1)
    else:
        toggle_living_room(0)
        toggle_kitchen(0)
        toggle_bedroom(0)
        toggle_wardrobe(0)
        toggle_bedside_1(0)
        toggle_bedside_2(0)
        toggle_kitchen_counter(0)
        toggle_shelf_light(0)


def lookup_mac_in_cache(target_mac):
    output = subprocess.check_output(("arp", "-a")).decode("ascii")
    pattern = r"\((.*?)\) at " + target_mac.lower()
    match = re.search(pattern, output.lower())
    
    if match:
        return match.group(1)
    return None

ip = lookup_mac_in_cache('e8:68:e7:c8:45:fe')

def set_light_state(room_name, state):
    """Універсальна функція для надсилання команди на реле/контролер"""
    status = "on" if state else "off"
    
    print(f"[LIGHT] {room_name}: {status}")
    requests.get(f"http://{ip}/sw/{room_name}/{status}")

def toggle_living_room(state: bool, *args):
    set_light_state("vitalnya", state)

def toggle_kitchen(state: bool, *args):
    set_light_state("kukhnya", state)

# def toggle_toilet_light(state: bool):
#     set_light_state("Туалет", state)

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