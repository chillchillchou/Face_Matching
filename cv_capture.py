import cv2
import os
import datetime
import re

# Camera 0 is the integrated web cam on my netbook
camera_port = 0

#Number of frames to throw away while the camera adjusts to light levels
ramp_frames = 30

# initialize the camera capture object with the cv2.VideoCapture class.
camera = cv2.VideoCapture(camera_port)


# Captures a single image from the camera and returns it in PIL format
def get_image():
 # read is the easiest way to get a full image out of a VideoCapture object.
 retval, im = camera.read()
 return im

# Ramp the camera - these frames will be discarded and are only used to allow v4l2
# to adjust light levels, if necessary
for i in range(ramp_frames):
 temp = get_image()
print("Taking image...")
# Take the actual image we want to keep
camera_capture = get_image()
t = str(datetime.datetime.now())
fileName=re.sub(r'\D',"",t)[4:12]
# print(fileName)
file = "img_cap/img"+fileName+".jpeg"

# A nice feature of the imwrite method is that it will automatically choose the
# correct format based on the file extension you provide. Convenient!
cv2.imwrite(file, camera_capture)
os.system("say Hello 'processing picture'")

# You'll want to release the camera, otherwise you won't be able to create a new
# capture object until your script exits
del(camera)
