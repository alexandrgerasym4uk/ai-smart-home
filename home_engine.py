import os
import time
import requests
from datetime import datetime
import subprocess
import re
import json
import threading 
from core import dispatch

STATE_FILE = "state.json"
TARGET_MAC = 'B0:67:B5:B2:7B:2D'

def load_state():
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

def lookup_mac_in_cache(target_mac):
    try:
        output = subprocess.check_output(("arp", "-a")).decode("ascii")
        pattern = r"\((.*?)\) at " + target_mac.lower()
        match = re.search(pattern, output.lower())
        if match:
            return match.group(1)
    except Exception as e:
        print(f"[ARP Error]: {e}")
    return None

def check_human_presence(ip_address):
    if not ip_address:
        return False
    response = os.system(f"ping -c 1 -t 2 {ip_address} > /dev/null 2>&1")
    return response == 0

def get_outside_temp():
    LATITUDE = "50.6199"
    LONGITUDE = "26.2516"
    try:
        with open("weather.txt", "r", encoding="utf-8") as file:
            api_key = file.read().strip() 
        openweather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={LATITUDE}&lon={LONGITUDE}&appid={api_key}&units=metric"
        res = requests.get(openweather_url, timeout=4)
        if res.status_code == 200:
            return res.json()["main"]["temp"]
    except Exception as e:
        print(f"[Weather Error]: {e}")
    return 15.0 

def is_dark_outside():
    hour = datetime.now().hour
    month = datetime.now().month
    
    if month in [12, 1, 2]: season = "Winter"
    elif month in [6, 7, 8]: season = "Summer"
    else: season = "MidSeason"
    
    if season == "Winter" and (hour >= 17 or hour <= 7): return True
    if season == "Summer" and (hour >= 21 or hour <= 5): return True
    if season == "MidSeason" and (hour >= 19 or hour <= 6): return True
    return False


def automation_loop():    
    while True:
        current_ip = lookup_mac_in_cache(TARGET_MAC)
        is_home = check_human_presence(current_ip)
        
        state = load_state()
        current_time = datetime.now().strftime("%H:%M")
        print(f"\n[{current_time}] Перевірка стану будинку...")   

        if not state.get("manual_control"):
            if is_home:
                dispatch(["lighting", "toggle_living_room", 0, None])
                dispatch(["lighting", "toggle_bedroom", 0, None])
                dispatch(["lighting", "toggle_kitchen_counter", 0, None])
                dispatch(["lighting", "toggle_bedside_1", 0, None])
                dispatch(["lighting", "toggle_bedside_2", 0, None])
                dispatch(["ventilation", None, 0, None])
                dispatch(["ac", "set_ac_power", 1, 23])
                
                outside_temp = get_outside_temp()
                if outside_temp < 15:
                    dispatch(["climate", "set_floor_power", 1, 20])
                else:
                    dispatch(["climate", None, 0, None])
                    
                if is_dark_outside():
                    dispatch(["lighting", "toggle_kitchen", 1, None])
                    dispatch(["lighting", "toggle_wardrobe", 1, None])
                    dispatch(["lighting", "toggle_shelf_light", 1, None])
                else:
                    dispatch(["lighting", None, 0, None])
            else:
                dispatch(["lighting", None, 0, None])
                dispatch(["climate", None, 0, None])
                dispatch(["ac", None, 0, None])
        else:
            print("Автоматику заблоковано користувачем")

        sleep_time = 5 if is_home else 20
        time.sleep(sleep_time)


def reset_timer_loop():
    TIMEOUT_LIMIT = 30
    seconds_counter = 0

    while True:
        state = load_state()

        time.sleep(2)
        
        new_state = load_state()

        if state != new_state:
            seconds_counter = 0
            
            if new_state.get("manual_control") == 0:
                new_state["manual_control"] = 1
                save_state(new_state)

        else:
            if new_state.get("manual_control") == 1:
                seconds_counter += 1
                
                if seconds_counter >= TIMEOUT_LIMIT:
                    current_state = load_state()
                    current_state["manual_control"] = 0
                    save_state(current_state)
                    
                    seconds_counter = 0

            else:
                seconds_counter = 0


def main():
    t1 = threading.Thread(target=automation_loop, name="AutomationThread")
    t2 = threading.Thread(target=reset_timer_loop, name="ResetTimerThread")

    t1.daemon = True
    t2.daemon = True
    
    t1.start()
    t2.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nЗупинено")

if __name__ == "__main__":
    main()