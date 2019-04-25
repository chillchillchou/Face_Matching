from gpiozero import LED, Button
from time import sleep

led1 = LED(23)
led2 = LED(24)
button = Button(25)
while True:
    button.wait_for_press()
    print("button pressed")
    led1.blink()
    led2.on()
    sleep(2)
    led1.off()
    led2.off()
    sleep(1)
