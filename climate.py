def default(state):
    if not state:
        set_floor_power(0, 0)



def set_floor_power(state: bool, power):
    """Керування живленням підлоги"""
    if state:
        power = int(power)
        print(f"[CLIMATE] Тепла підлога: ON")
        if 0 <= power <= 100:
            print(f"[CLIMATE] Встановлено температуру: {power}°C")
        else:
            print("[CLIMATE] Помилка: Некоректна температура")
    else:
        print(f"[CLIMATE] Тепла підлога: OFF")