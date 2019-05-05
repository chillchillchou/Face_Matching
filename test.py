
import io
from PIL import Image
from pprint import pprint
import os
import datetime
import re
import time
import picamera
from gpiozero import LED, Button,OutputDevice
from time import sleep
motor = OutputDevice(18)
led_red = LED(25)
led_green = LED(4)

def do_something_when_pressed():
    print("button pressed")

# define button pin
button1 = Button(23)
button2 = Button(24)

# take a picture and save as a local file


# def take_picture(camera, stream):
#
#     print("Taking image...")
#     # Take the actual image we want to keep
#     stream.seek(0)
#     stream.truncate()
#     camera.capture(stream, format="jpeg")
#     os.system("espeak \"Hello Hello, I am processing your pictures\"  --stdout | aplay -D bluealsa:HCI=hci0,DEV=30:C0:1B:8D:BF:7F,PROFILE=a2dp")
#     return Image.open(stream)
#     #return(file)

# upload the captured picture to aws and search for matching face
# def findName(stream):
#     # stream = io.BytesIO()
#     # image.save(stream, format="JPEG")
#     #image_binary = stream.getvalue()
#     response = rekognition.detect_faces(
#         Image={'Bytes':  stream.getvalue()}
#     )
#
#     all_faces = response['FaceDetails']
#
#     # Initialize list object
#     boxes = []
#
#     image = Image.open(stream)
#     # Get image diameters
#     image_width = image.size[0]
#     image_height = image.size[1]
#
#     # Crop face from image
#     for face in all_faces:
#         box = face['BoundingBox']
#         x1 = int(box['Left'] * image_width) * 0.9
#         y1 = int(box['Top'] * image_height) * 0.9
#         x2 = int(box['Left'] * image_width + box['Width'] * image_width) * 1.10
#         y2 = int(box['Top'] * image_height
#                  + box['Height'] * image_height) * 1.10
#         image_crop = image.crop((x1, y1, x2, y2))
#
#         stream = io.BytesIO()
#         image_crop.save(stream, format="JPEG")
#         image_crop_binary = stream.getvalue()
#
#         # Submit individually cropped image to Amazon Rekognition
#         response = rekognition.search_faces_by_image(
#             CollectionId='itpFaces',
#             Image={'Bytes': image_crop_binary}
#         )
#         face_found = len((response["FaceMatches"]))
#         if face_found:
#             print('found ' + str(face_found) + 'face')
#             matchedFile = response["FaceMatches"][0]["Face"]["ExternalImageId"]
#             # b = matchedFile.index(".")
#             # returnName = matchedFile[:b]
#             return matchedFile
#         if not face_found:
#             return
#
#
# def detectEmotion():
#
#     response = client.detect_faces(
#         Image={'S3Object': {'Bucket': BUCKET, 'Name': photo}}, Attributes=['ALL'])
#
#     print('Detected faces for ' + photo)
#     for faceDetail in response['FaceDetails']:
#         for emotion in faceDetail['Emotions']:
#             if emotion['Confidence'] > 60:
#                 print(str(emotion['Type']) + ', ' + str(emotion['Confidence']))
#
#
# def uploadSingleImg(stream, name):
#     # file = open(fileName, 'rb')
#     t = str(datetime.datetime.now())
#     fileName = re.sub(r'\D', "", t)[4:12] + ".jpeg"
#
#     object = s3.Object('itpface', fileName)
#     ret = object.put(Body=stream.getvalue(),
#                      Metadata={'FullName': name}
#                      )
#     response = client.index_faces(CollectionId=COLLECTION_ID,
#                                   Image={'S3Object': {
#                                       'Bucket': BUCKET, 'Name': fileName}},
#                                   ExternalImageId=name,
#                                   MaxFaces=2,
#                                   QualityFilter="AUTO",
#                                   DetectionAttributes=['DEFAULT'])
#     print(response)
#


def button_1_pressed():
    print("pressed")

    led_red.blink()
    sleep(10)
    led_red.off()
    led_green.on()


def button_2_pressed():
    print("MOTOR ON")
    motor.on()
    sleep(5)
    motor.off()
    print("motor off")


def main():
    print('starting program')
    button_1_press_triggered = False
    button_2_press_triggered = False

    while True:  # comment th
        if button1.value == 1:
            if not button_1_press_triggered:
                print('triggering button 1')
                button_1_pressed()
                button_1_press_triggered = True
        else:
            button_1_press_triggered = False

        if button2.value == 1:
            if not button_2_press_triggered:
                print('triggering button 2')
                button_2_pressed()
                button_2_press_triggered = True
        else:
            button_2_press_triggered = False




            # button.wait_for_press()  # comment this out if you ar enot using a button
            #
            # button.wait_for_release()  # comment this out if you ar enot using a button
            # print("released")
        # button2.wait_for_press()
        # print("tear up")
        # motor.on()
        # sleep(10)
        # motor.off()
        # button2.wait_for_release()


if __name__ == "__main__":
    # execute only if run as a script
    main()