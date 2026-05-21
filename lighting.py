import requests
import subprocess
import re

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

def toggle_living_room(state: bool):

    set_light_state("vitalnya", state)

def toggle_kitchen(state: bool):
    set_light_state("kukhnya", state)

def toggle_toilet_light(state: bool):
    set_light_state("Туалет", state)

def toggle_bedroom(state: bool):
    set_light_state("spalnya", state)

def toggle_wardrobe(state: bool):
    set_light_state("garderob", state)

def toggle_bedside_1(state: bool):
    set_light_state("lampa1", state)

def toggle_bedside_2(state: bool):
    set_light_state("lampa2", state)

def toggle_kitchen_counter(state: bool):
    set_light_state("stilnitsya", state)

def toggle_shelf_light(state: bool):
    set_light_state("polytsi", state)