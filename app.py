from flask import Flask, render_template, jsonify, request

import lighting
import climate as climate_module
import ventilation

from devices.roborockS5max import VirtualRoborockS5Max
from devices.cooperHunter import VirtualCooperHunterAC

app = Flask(__name__)

rooms_light = {
    "Vitalnya": False, "Spalnya": False, "Garderob": False,
    "Kukhnya": False, "Stilnytsya": False, "Polytsi": False,
    "Lampa_1": False, "Lampa_2": False, "Toilet_Light": False
}

fans = {"Toilet_Fan": False}

climate_data = {
    "floor": {"val": 30, "active": False}
}

active_users = []

vacuum = VirtualRoborockS5Max()
ac = VirtualCooperHunterAC()


@app.route('/')
def index():
    full_climate = {
        "floor": climate_data['floor'],
        "ac": ac.get_status()
    }
    return render_template('index.html', lights=rooms_light, climate=full_climate, fans=fans)

@app.route('/toggle/<room>')
def toggle_light(room):
    if room in rooms_light:
        rooms_light[room] = not rooms_light[room]
        state = rooms_light[room]
        if room == "Vitalnya": lighting.toggle_living_room(state)
        elif room == "Kukhnya": lighting.toggle_kitchen(state)
        elif room == "Spalnya": lighting.toggle_bedroom(state)
        elif room == "Garderob": lighting.toggle_wardrobe(state)
        elif room == "Lampa_1": lighting.toggle_bedside_1(state)
        elif room == "Lampa_2": lighting.toggle_bedside_2(state)
        elif room == "Stilnytsya": lighting.toggle_kitchen_counter(state)
        elif room == "Polytsi": lighting.toggle_shelf_light(state)
        return jsonify(success=True)
    return jsonify(success=False), 404

@app.route('/toggle_fan/<fan>')
def toggle_fan(fan):
    if fan in fans:
        fans[fan] = not fans[fan]
        ventilation.toggle_toilet_fan(fans[fan])
        return jsonify(success=True)
    return jsonify(success=False), 404

@app.route('/set_climate', methods=['POST'])
def set_climate():
    data = request.json
    dev = data.get('device')
    
    if dev == 'ac':
        if 'active' in data:
            ac.toggle(data['active'])
        if 'value' in data:
            ac.set_temperature(data['value'])
            
    elif dev == 'floor':
        if 'active' in data:
            state = data['active']
            climate_data['floor']['active'] = state
            climate_module.set_floor_power(state)
        if 'value' in data:
            val = int(data['value'])
            climate_data['floor']['val'] = val
            climate_module.set_floor_temperature(val) 
            
    return jsonify(success=True)

@app.route('/api/ac/params', methods=['POST'])
def ac_params():
    data = request.json
    p_type = data.get('type')
    p_val = data.get('value')

    if p_type == 'temp':
        ac.set_temperature(p_val)
    elif p_type == 'mode':
        ac.set_mode(p_val)
    elif p_type == 'swing':
        ac.set_swing(p_val)

    return jsonify(success=True)

@app.route('/api/vacuum/command/<cmd>', methods=['POST'])
def vacuum_command(cmd):
    if cmd == 'start': vacuum.app_start()
    elif cmd == 'stop' or cmd == 'pause': vacuum.app_stop()
    elif cmd == 'home': vacuum.app_charge()
    return jsonify(success=True)

@app.route('/api/vacuum/params', methods=['POST'])
def vacuum_params():
    data = request.json
    param_type = data.get('type')
    param_value = data.get('value')

    if param_type == 'fan':
        vacuum.set_custom_mode(int(param_value))
    elif param_type == 'water':
        vacuum.set_water_box_custom_mode(int(param_value))
    return jsonify(success=True)

@app.route('/api/status')
def status():
    return jsonify({
        "active_users": active_users,
        "anyone_home": len(active_users) > 0,
        "lights": rooms_light,
        "climate": {
            "floor": climate_data['floor'],
            "ac": ac.get_status() 
        },
        "fans": fans,
        "vacuum": vacuum.get_status()
    })

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8000)