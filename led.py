from gpiozero import LED
from time import sleep

led1 = LED(23)
led2 = LED(24)
button = Button(25)
buttom.wati_for_press()
print("button pressed")
led1.on()
led2.on()
sleep(3)
led1.off()
led2.off()
