
def set_floor_power(state: bool):
    """Керування живленням кондиціонера"""
    print(f"[CLIMATE] Тепла підлога: {'ON' if state else 'OFF'}")

def set_floor_temperature(power: int):
    
    if 0 <= power <= 100:
        print(f"[CLIMATE] Встановлено температуру: {power}°C")
    else:
        print("[CLIMATE] Помилка: Некоректна температура")

""" Не використовуються """
def set_ac_power(state: bool):
    """Керування живленням кондиціонера"""
    print(f"[CLIMATE] Кондиціонер: {'ON' if state else 'OFF'}")

def set_ac_temperature(temp: int):
    """Встановлення цільової температури (16-30°C)"""
    if 16 <= temp <= 30:
        print(f"[CLIMATE] Встановлено температуру: {temp}°C")
    else:
        print("[CLIMATE] Помилка: Некоректна температура")

def set_ac_mode(mode: str):
    """Режими: 'cool', 'heat', 'dry', 'fan'"""
    print(f"[CLIMATE] Режим змінено на: {mode}")
