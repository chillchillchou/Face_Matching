from gpiozero import LED, Button
from time import sleep
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from time import sleep # Import the sleep function from the time module
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(23, GPIO.OUT, initial=GPIO.LOW) # Set pin 8 to be an output pin and set initial value to low (off)
button=Button(25)
button.wati_for_press()
print("button pressed")
GPIO.output(23, GPIO.HIGH) # Turn on
sleep(1) # Sleep for 1 second
GPIO.output(23, GPIO.LOW) # Turn off
sleep(1) # Sleep for 1 second
