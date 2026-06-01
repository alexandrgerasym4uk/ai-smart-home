from hardware import DEVICE_MAP, STATE_MAP, PARAMETERS_MAP
import re
import importlib
import requests
from ai_agent import parse_smart_command

def tokenize(text):
    return re.findall(r"\d+|%|°|[а-яіїєґa-zA-Z]+", text.lower())

def is_ollama_running():
    local_url = "http://localhost:11434/"
    try:
        response = requests.get(local_url, timeout=2)
        if response.status_code == 200:
            return True
    except requests.exceptions.ConnectionError:
        return False
    return False

class Command:
    def __init__(self):
        self.device = None
        self.parameters = None
        self.state = None
        self.additional = None

    def build(self):
        return [self.device, self.parameters, self.state, self.additional]
    


def translate_command(code_str):
    cmd = Command()
    print("Отримано команду: ", code_str)
    words = tokenize(code_str.lower())
    print(words)
    if is_ollama_running():
        cmd = parse_smart_command(code_str)
        print(cmd)
        command = [cmd['category'], cmd['function'], cmd['state'], cmd['additional_parameter']]
        print(command)

    else:
        try:
            if not code_str:
                return False, "Порожній код"
            
            for word in words:
                if word.isdigit():
                    cmd.additional = word
                
                    
                for key in DEVICE_MAP:
                        if key in word:
                            cmd.device = DEVICE_MAP[key]

                for key in STATE_MAP:
                    if key in word:
                        cmd.state = STATE_MAP[key]

                for key in PARAMETERS_MAP:
                        if key in word:
                            cmd.parameters = PARAMETERS_MAP[key]

                

        except Exception as e:
            return False, f"Помилка: {str(e)}"
        
        command = cmd.build()
        print(command)


    dispatch(command)

        
def dispatch(command):
    device, parameter, state, additional = command
    module = importlib.import_module(device)

    if parameter is None:
        func = getattr(module, "default")
    else:
        func = getattr(module, parameter)

    if additional is not None:
        return func(state, additional)
    elif state is not None:
        return func(state)
    else:
        return func()
