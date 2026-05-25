from devices.cooperHunter import VirtualCooperHunterAC

ac = VirtualCooperHunterAC()

def default(state):
    if not state:
        set_ac_power(0, 0)

def set_ac_power(state: bool, temp):
    """Керування живленням кондиціонера"""

    if state:
        temp = int(temp)

        print(f"[CLIMATE] Кондиціонер: ON")
        ac.toggle(state)
        ac.set_temperature(temp)

    else:
        print(f"[CLIMATE] Кондиціонер: OFF")
        ac.toggle(state)