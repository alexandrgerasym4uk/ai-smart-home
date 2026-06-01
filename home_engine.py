import os
import time
import requests
from datetime import datetime
import subprocess
import re
from core import dispatch


def lookup_mac_in_cache(target_mac):
    output = subprocess.check_output(("arp", "-a")).decode("ascii")
    pattern = r"\((.*?)\) at " + target_mac.lower()
    match = re.search(pattern, output.lower())

    if match:
        return match.group(1)
    return None


ip = lookup_mac_in_cache('B0:67:B5:B2:7B:2D')

def check_human_presence(ip_address):
    response = os.system(f"ping -c 1 -t 2 {ip_address} > /dev/null 2>&1")
    return response == 0


import requests

def get_outside_temp():
    LATITUDE = "50.6199"
    LONGITUDE = "26.2516"
    
    with open("weather.txt", "r", encoding="utf-8") as file:
        api_key = file.read().strip() 
            
    openweather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={LATITUDE}&lon={LONGITUDE}&appid={api_key}&units=metric"
        
    res = requests.get(openweather_url, timeout=4)
    return res.json()["main"]["temp"]



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

def main():
    print("=== Контролер Розумного Будинку запущено ===")
    
    while True:
        current_time = datetime.now().strftime("%H:%M")
        print(f"\n[{current_time}] Перевірка стану будинку...")
        
        is_home = check_human_presence(ip)
    
        
        if is_home:
            print("Олександр вдома")
            
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

        if is_home:
            time.sleep(10) #300
        else:
            time.sleep(20) #900

if __name__ == "__main__":
    main()