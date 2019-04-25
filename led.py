from gpiozero import LED
from time import sleep
led = LED(24)
while True:
    led.on
    sleep(5)
    led.off()
    sleep(1)
