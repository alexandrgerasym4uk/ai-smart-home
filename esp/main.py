import machine
import socket
import time

switches_config = {
    'vitalnya': 14,
    'kukhnya': 12,
    'spalnya': 13,
    'garderob': 15,
    'stilnitsya': 2,
    'polytsi': 0,
    'lampa1': 4,
    'lampa2': 5
}

pins = {}
for name, pin_num in switches_config.items():
    pins[name] = machine.Pin(pin_num, machine.Pin.OUT)
    pins[name].value(1)

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(5)

print('Сервер 8-канального контролера запущено...')

while True:
    try:
        res, addr = s.accept()
        request = res.recv(1024).decode('utf-8')
        
        for name in switches_config.keys():
            if f'/sw/{name}/on' in request:
                pins[name].value(0) # On
                print(f'{name} ON')
            elif f'/sw/{name}/off' in request:
                pins[name].value(1) # Off
                print(f'{name} OFF')

        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nOK"
        res.send(response)
        res.close()
    except Exception as e:
        print("Error:", e)