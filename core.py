import os
import json
import lighting
from hardware import DEVICE_MAP, STATE_MAP, ADDITIONAL_MAP, PARAMETERS_MAP
import re

def tokenize(text):
    return re.findall(r"\d+|%|°|[а-яіїєґa-zA-Z]+", text.lower())

class Command:
    def __init__(self):
        self.device = None
        self.parameters = None
        self.state = None
        self.additional = None

    def build(self):
        return [self.device, self.parameters, self.state, self.additional]
    

class HomeCore:
    def translate_command(self, code_str):
        cmd = Command()
        print("Отримано команду: ", code_str)
        words = tokenize(code_str.lower())
        print(words)
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
        
        print(cmd.build())


# core = HomeCore()
# code_str = input("введіть команду ")
# core.translate_command(code_str)