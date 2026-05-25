from devices.roborockS5max import VirtualRoborockS5Max

vacuum = VirtualRoborockS5Max()

def default(state):
    if state:
        vacuum.app_start()
    else:
        vacuum.app_stop()

def go_home():
    vacuum.app_charge()
    