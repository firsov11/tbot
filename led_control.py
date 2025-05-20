import time
from machine import Pin

# Инициализация встроенного светодиода
led = Pin(22, Pin.OUT)

def tripl_led():
    for i in range(0, 3):
        led.value(0)
        time.sleep(1)
        led.value(1)
        time.sleep(1)
