from flask import Flask, jsonify
import json
import os
from flask import request
from flask import Flask, jsonify, request, render_template
from core import dispatch
from ac import *
from vacuum import *

app = Flask(__name__)

STATE_FILE = "state.json"

def load_state():
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


@app.route('/api/status')
def get_status():
    return jsonify(load_state())


@app.route('/toggle/<room>')
def toggle_room(room):
    state = load_state()
    current_state = state["lighting"].get(room, 0)
    

    new_state = 0 if current_state == 1 else 1

    room_commands = {
        "vitalnya": "toggle_living_room",
        "kukhnya": "toggle_kitchen",
        "spalnya": "toggle_bedroom",
        "garderob": "toggle_wardrobe",
        "stilnitsya": "toggle_kitchen_counter",
        "polytsi": "toggle_shelf_light",
        "lampa1": "toggle_bedside_1",
        "lampa2": "toggle_bedside_2"
    }
    
    cmd_code = room_commands.get(room)
    if cmd_code:
        dispatch([ 'lighting', cmd_code, new_state, None ])

        return jsonify(success=True, room=room, new_state=new_state)
    

    save_state(state)

    return jsonify(success=False, error="Кімнату не знайдено"), 404


@app.route('/toggle_fan')
def toggle_fan():
    state = load_state()

    if state["ventilation"] == 0:
        state["ventilation"] = 1
        dispatch([ 'ventilation', None, 1, None ])
        
    else:
        state["ventilation"] = 0
        dispatch([ 'ventilation', None, 0, None ])

    save_state(state)

    return jsonify(success=True, new_fan_state=state["ventilation"])


@app.route('/set_climate', methods=['POST'])
def set_climate():
    data = request.json
    
    dev = data.get("device")
    
    state = load_state()
    commands_to_send = []

    if dev == "ac":
        if "active" in data:
            state["ac"]["is_on"] = bool(data["active"])
            is_on_val = 1 if data["active"] else 0
            current_temp = str(state["ac"]["temperature"])
            commands_to_send.append('ac')
            commands_to_send.append('set_ac_power')
            commands_to_send.append(is_on_val)
            commands_to_send.append(current_temp)
        
        if "value" in data:
            state["ac"]["temperature"] = int(data["value"])
            temp_val = int(data["value"])
            commands_to_send.append('ac')
            commands_to_send.append('set_ac_power')
            commands_to_send.append(None)
            commands_to_send.append(temp_val)


    elif dev == "floor":
        if "active" in data:
            state["climate"]["state"] = 1 if data["active"] else 0
            state_val = 1 if data["active"] else 0
            current_power = str(state["climate"]["power"])
            commands_to_send.append('climate')
            commands_to_send.append('set_floor_power')
            commands_to_send.append(state_val)
            commands_to_send.append(current_power)
        
        if "value" in data:
            state["climate"]["power"] = int(data["value"])
            power_val = int(data["value"])
            commands_to_send.append('climate')
            commands_to_send.append('set_floor_power')
            commands_to_send.append(power_val)
            commands_to_send.append(str(power_val))
            
    else:
        return jsonify(success=False, error="Невідомий пристрій клімату"), 404

    save_state(state)
    if commands_to_send:
        dispatch(commands_to_send)
        return jsonify(success=True)

    return jsonify(success=False, error="Немає даних для зміни"), 400

@app.route('/api/ac/params', methods=['POST'])
def ac_params():
    data = request.json
    
    param_type = data.get("type") 
    param_value = data.get("value") 
    
    state = load_state()

    if param_type in state["ac"]:
        state["ac"][param_type] = param_value
        set_ac_additional(param_type, param_value)

        save_state(state)
        
        return jsonify(success=True)
        
    else:
        return jsonify(success=False, error="Невідомий параметр кондиціонера"), 404
    
@app.route('/api/vacuum/command/<cmd>')
def vacuum_command(cmd):
    state = load_state()
    
    if cmd == "start":
        dispatch(['vacuum', None, 1, None])
        state["vacuum"]["state"] = "cleaning"
    elif cmd in ["stop", "pause"]:
        state["vacuum"]["state"] = "paused"
        dispatch(['vacuum', None, 0, None])
    elif cmd == "home":
        state["vacuum"]["state"] = "returning"
        dispatch(['vacuum', "go_home", None, None])
    else:
        return jsonify(success=False, error="Невідома команда для пилососа"), 400
        
    save_state(state)
    return jsonify(success=True, current_state=state["vacuum"]["state"])

@app.route('/api/vacuum/params', methods=['POST'])
def vacuum_params():
    data = request.json
    param_type = data.get("type")   # 'fan' або 'water'
    param_value = data.get("value") # Числове значення
    
    state = load_state()
    
    if param_type == "fan":
        state["vacuum"]["fan_power"] = int(param_value)
        set_vacuum_additional(param_type, int(param_value))
    elif param_type == "water":
        state["vacuum"]["water_level"] = int(param_value)
        set_vacuum_additional(param_type, int(param_value))
    else:
        return jsonify(success=False, error="Невідомий параметр пилососа"), 404

        
    save_state(state)
    return jsonify(success=True)

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)