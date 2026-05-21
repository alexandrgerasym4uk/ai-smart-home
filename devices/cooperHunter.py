class VirtualCooperHunterAC:
    def __init__(self):
        self.is_on = False
        self.temperature = 22
        self.mode = "cool"     # cool, heat, dry, fan
        self.fan_speed = "auto" # low, medium, high, auto
        self.swing = "fixed"   # fixed, vertical, horizontal, full

    def toggle(self, state=None):
        """Вмикання або вимикання"""
        if state is not None:
            self.is_on = state
        else:
            self.is_on = not self.is_on
        print(f"[C&H] Живлення: {'ON' if self.is_on else 'OFF'}")

    def set_temperature(self, temp):
        """Встановлення температури (зазвичай 16-30°C)"""
        if 16 <= int(temp) <= 30:
            self.temperature = int(temp)
            print(f"[C&H] Температура: {self.temperature}°C")
        else:
            print(f"[C&H] Помилка: Температура {temp} поза межами (16-30)")

    def set_mode(self, mode):
        """Зміна режиму роботи"""
        valid_modes = ["cool", "heat", "dry", "fan"]
        if mode in valid_modes:
            self.mode = mode
            print(f"[C&H] Режим змінено на: {self.mode}")
        else:
            print(f"[C&H] Помилка: Режим {mode} не підтримується")

    def set_swing(self, direction):
        """Напрямок потоку повітря"""
        valid_directions = ["fixed", "vertical", "horizontal", "full"]
        if direction in valid_directions:
            self.swing = direction
            print(f"[C&H] Напрямок повітря (Swing): {self.swing}")
        else:
            print(f"[C&H] Помилка: Напрямок {direction} невідомий")

    def get_status(self):
        return {
            "active": self.is_on,
            "val": self.temperature,
            "mode": self.mode,
            "swing": self.swing,
            "fan_speed": self.fan_speed
        }
    


