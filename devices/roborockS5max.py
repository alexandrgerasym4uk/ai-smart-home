from time import sleep

class VirtualRoborockS5Max:
    def __init__(self):
        self.name = "Roborock S5 Max (Virtual)"
        self.state = "idle"  # idle, cleaning, returning, charging, paused
        self.fan_power = 102 # 101: Quiet, 102: Balanced, 103: Turbo, 104: Max
        self.water_level = 201 # 200: Off, 201: Low, 202: Medium, 203: High
        
    def _log(self, message):
        print(f"[DEVICE: {self.name}] >>> {message}")


    def app_start(self):
        if self.state == "cleaning":
            self._log("Вже прибираю. Команду ігноровано.")
        else:
            self.state = "cleaning"
            self._log("СТАРТ: Починаю повне прибирання оселі.")
        return {"status": "ok"}

    def app_stop(self):
        self.state = "idle"
        self._log("СТОП: Прибирання зупинено, очікую наступних команд.")
        return {"status": "ok"}

    def app_pause(self):
        if self.state == "cleaning":
            self.state = "paused"
            self._log("ПАУЗА: Роботу призупинено.")
        else:
            self._log("Неможливо поставити на паузу (пилосос не працює).")
        return {"status": "ok"}

    def app_charge(self):
        self.state = "returning"
        self._log("БАЗА: Повертаюсь до станції зарядки.")
        sleep(3)
        self._log("БАЗА: На зарядній станції")
        self.state = "charging"
        return {"status": "ok"}

    def set_custom_mode(self, level):
        modes = {101: "Quiet", 102: "Balanced", 103: "Turbo", 104: "Max"}
        if level in modes:
            self.fan_power = level
            self._log(f"РЕЖИМ: Потужність встановлена на {modes[level]}.")
            return {"status": "ok"}
        return {"status": "error", "message": "Invalid mode"}

    def set_water_box_custom_mode(self, level):
        levels = {200: "Off", 201: "Low", 202: "Medium", 203: "High"}
        if level in levels:
            self.water_level = level
            self._log(f"ВОДА: Рівень подачі води встановлено на {levels[level]}.")
            return {"status": "ok"}
        return {"status": "error", "message": "Invalid level"}

    def get_status(self):
        status_data = {
            "state": self.state,
            "fan_power": self.fan_power,
            "water_level": self.water_level,
            "model": "S5 Max"
        }
        return status_data

