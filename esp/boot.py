import network
import time

def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Підключення до мережі...')
        sta_if.active(True)
        sta_if.connect('happy_house', 'ilomilo22')
        
        attempts = 0
        while not sta_if.isconnected() and attempts < 10:
            time.sleep(1)
            attempts += 1
            
    if sta_if.isconnected():
        print('Успіх! Мережеві дані:', sta_if.ifconfig())
    else:
        print('Помилка: не вдалося підключитися.')

do_connect()