import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"

def parse_smart_command(user_phrase):
    """
    Аналізує текст користувача і повертає чітку команду у форматі списку:
    ["category", "function", state_int, additional_param]
    """
    
    system_instruction = (
        "You are a strict Smart Home command converter. Your only job is to translate "
        "the user's phrase in Ukrainian into a raw JSON array with exactly 4 elements:\n"
        "Format: [\"category\", \"function\", state, additional_parameter]\n\n"
        
        "Where:\n"
        "1. 'category' (string): 'climate', 'ac', 'lighting', 'vacuum', 'ventilation', or 'unknown'.\n"
        "2. 'function' (string): the specific action/hardware function name.\n"
        "3. 'state' (int): 1 for ON / active / true, 0 for OFF / inactive / false.\n"
        "4. 'additional_parameter': a string, number, or None if there is no parameter (e.g., temperature, percentage).\n\n"
        
        "MODULE CONFIGURATION (RULES):\n"
        "--- CLIMATE MODULE ---\n"
        "- If user mentions floor heating (тепла підлога): category is 'climate'.\n"
        "  Available functions: 'default' to turn off.\n"
        "  Available functions: 'set_floor_power' to set power.\n"
        "  If user specifies a percentage (e.g., 25%), put the number (25) in additional_parameter. If not, put None.\n\n"
        
        "--- AC MODULE ---\n"
        "- If user mentions air conditioning (кондиціонер): category is 'ac'.\n"
        "  Available functions: 'default' to turn off.\n"
        "  Available functions: 'set_ac_power' to set temperature.\n"
        "  If user specifies degrees (e.g., 27 degrees), put the temperature number (27) in additional_parameter. If not, put null.\n\n"
        
        "--- LIGHTING MODULE ---\n"
        "- If user mentions light (світло): category is 'lighting'.\n"
        "  Available functions: 'default' to turn off.\n"
        "Available functions: \
            'toggle_living_room' to turn on living room, \
            'toggle_kitchen' to turn on kitchen, \
            'toggle_bedroom' to turn on bedroom, \
            'toggle_wardrobe' to turn on wardrobe, \
            'toggle_bedside_1' to turn on bedside lamp 1, \
            'toggle_bedside_2' to turn on bedside lamp 2, \
            'toggle_kitchen_counter' to turn on kitchen counter, \
            'toggle_shelf_light' to turn on shelf light.\n"
        "  Parameters: Always None\n\n"
        
        "--- VACUUM MODULE ---\n"
        "- If user mentions cleaning or Gosha (прибирання, Гоша): category is 'vacuum'.\n"
        "  *REMEMBER*: The vacuum cleaner (Gosha) is a VIRTUAL MODEL for verification purposes, treat it accordingly.\n"
        "  Available functions: 'default' to start clean or turn off.\n"
        "  Available functions: 'go_home' to turn off.\n\n"
        
        "--- VENTILATION MODULE ---\n"
        "- If user mentions ventilation (провітрювання, вентиляція): category is 'ventilation'.\n"
        "  Available functions: 'default' to turn on or turn off.\n\n"
        # =====================================================
        
        "EXAMPLES (PAY CLOSE ATTENTION TO STATE 1 vs 0):\n"
        "Input: 'увімкни підлогу на 25%' -> Output: [\"climate\", \"set_floor_power\", 1, 25]\n"
        "Input: 'вимкни підлогу' -> Output: [\"climate\", \"set_floor_power\", 0, None]\n"
        "Input: 'увімкни світло у вітальні' -> Output: [\"lighting\", \"toggle_living_room\", 1, None]\n"
        "Input: 'вимкни світло у вітальні' -> Output: [\"lighting\", \"toggle_living_room\", 0, None]\n"
        "Input: 'вистав кондиціонер 27 градусів' -> Output: [\"ac\", \"set_ac_power\", 1, 27]\n"
        "Input: 'вимкни кондиціонер' -> Output: [\"ac\", \"set_ac_power\", 0, None]\n"
        "Input: 'запусти Гошу' -> Output: [\"vacuum\", \"default\", 1, None]\n"
        "Input: 'відправ Гошу на базу' -> Output: [\"vacuum\", \"go_home\", 0, None]\n\n"           
        
        "CRITICAL RULE:\n"
        "Respond ONLY with a valid JSON array. No markdown, no text. Example: [\"category\", \"function\", 1, null]"
    )

    try:
        response = requests.post(OLLAMA_URL, json={
            "model": "llama3.2:1b", 
            "prompt": f"{system_instruction}\n\nInput phrase: '{user_phrase}' -> Output:",
            "stream": False,
            "format": "json", 
            "options": {"temperature": 0.0} 
        }, timeout=5)
        
        if response.status_code == 200:
            return json.loads(response.json()['response'])
        else:
            return ["unknown", "error", 0, f"HTTP {response.status_code}"]
            
    except Exception as e:
        return ["unknown", "error", 0, str(e)]



