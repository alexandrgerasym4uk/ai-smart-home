import time

def toggle_toilet_fan(state: bool):
    """Ввімкнути/вимкнути витяжку в туалеті"""
    print(f"[VENT] Витяжка в туалеті: {'ПРАЦЮЄ' if state else 'ЗУПИНЕНО'}")
