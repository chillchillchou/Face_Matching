from gpiozero import Button
button = Button(2)
#button.wait_for_press()
while True:
	button.wait_for_press()
	print("pressed")
	button.wait_for_release()
	print("Released")
