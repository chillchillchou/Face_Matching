from gpiozero import LED, Button
from time import sleep

led1 = LED(23)
led2 = LED(24)
button = Button(25)
button.wait_for_press()
print("button pressed")
led1.on()
led2.on()
sleep(1)
led1.off()
led2.off()
sleep(1)
