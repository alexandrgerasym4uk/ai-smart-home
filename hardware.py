DEVICE_MAP = {
    "світл": "lighting",
    "пилосос": "vacuum",
    "кондиціонер": "ac",
    "вентиляц": "ventilation",
    "тепл": "climate",
    "підлог": "climate",
    "гоша": "vacuum"
}

STATE_MAP = {
    "вімкн": 1,
    "включ": 1,
    "вимкн": 0,
    "виключ": 0,
    "запуст": 1,
    "зупини": 0,
    "приб": 1
}

PARAMETERS_MAP = {
    "вітальн": "toggle_living_room",
    "кухн": "toggle_kitchen",
    "спальн": "toggle_bedroom",
    "гардероб": "toggle_wardrobe",
    "стільн": "toggle_kitchen_counter",
    "пол": "toggle_shelf_light",
    "лів": "toggle_bedside_1",
    "прав": "toggle_bedside_2",
    "%": "set_floor_power",
    "°": "set_ac_power",
    "додом": "go_home",
    # "": "ac_mode",
    # "": "power_vaccum",
    # "": "power_water"
}
