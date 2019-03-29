from gpiozero import Button
button = Button(2)
#button.wait_for_press()
old_input_state = True

while True:
	new_input_state=button.is_pressed()
	button.wait_for_press()
	print("pressed")
	button.wait_for_release()
	print("Released")
