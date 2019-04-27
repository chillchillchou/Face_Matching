#import numpy as np
#import cv2
import boto3
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
led_red = LED(23)
led_green = LED(24)

# connect to aws rekognition
BUCKET = 'itpface'
COLLECTION_ID = 'itpFaces'
s3 = boto3.resource('s3')
client = boto3.client('rekognition')
rekognition = boto3.client('rekognition', region_name='us-east-1')


def do_something_when_pressed():
    print("button pressed")

# define button pin
button1 = Button(25)
button2 = Button(4)

# take a picture and save as a local file


def take_picture(camera, stream):

    print("Taking image...")
    # Take the actual image we want to keep
    stream.seek(0)
    stream.truncate()
    camera.capture(stream, format="jpeg")
    os.system("espeak \"Hello Hello, I am processing your pictures\"  --stdout | aplay -D bluealsa:HCI=hci0,DEV=30:C0:1B:8D:BF:7F,PROFILE=a2dp")
    return Image.open(stream)
    #return(file)

# upload the captured picture to aws and search for matching face
def findName(stream):
    # stream = io.BytesIO()
    # image.save(stream, format="JPEG")
    #image_binary = stream.getvalue()
    response = rekognition.detect_faces(
        Image={'Bytes':  stream.getvalue()}
    )

    all_faces = response['FaceDetails']

    # Initialize list object
    boxes = []

    image = Image.open(stream)
    # Get image diameters
    image_width = image.size[0]
    image_height = image.size[1]

    # Crop face from image
    for face in all_faces:
        box = face['BoundingBox']
        x1 = int(box['Left'] * image_width) * 0.9
        y1 = int(box['Top'] * image_height) * 0.9
        x2 = int(box['Left'] * image_width + box['Width'] * image_width) * 1.10
        y2 = int(box['Top'] * image_height
                 + box['Height'] * image_height) * 1.10
        image_crop = image.crop((x1, y1, x2, y2))

        stream = io.BytesIO()
        image_crop.save(stream, format="JPEG")
        image_crop_binary = stream.getvalue()

        # Submit individually cropped image to Amazon Rekognition
        response = rekognition.search_faces_by_image(
            CollectionId='itpFaces',
            Image={'Bytes': image_crop_binary}
        )
        face_found = len((response["FaceMatches"]))
        if face_found:
            print('found ' + str(face_found) + 'face')
            matchedFile = response["FaceMatches"][0]["Face"]["ExternalImageId"]
            # b = matchedFile.index(".")
            # returnName = matchedFile[:b]
            return matchedFile
        if not face_found:
            return


def detectEmotion():

    response = client.detect_faces(
        Image={'S3Object': {'Bucket': BUCKET, 'Name': photo}}, Attributes=['ALL'])

    print('Detected faces for ' + photo)
    for faceDetail in response['FaceDetails']:
        for emotion in faceDetail['Emotions']:
            if emotion['Confidence'] > 60:
                print(str(emotion['Type']) + ', ' + str(emotion['Confidence']))


def uploadSingleImg(stream, name):
    # file = open(fileName, 'rb')
    t = str(datetime.datetime.now())
    fileName = re.sub(r'\D', "", t)[4:12] + ".jpeg"

    object = s3.Object('itpface', fileName)
    ret = object.put(Body=stream.getvalue(),
                     Metadata={'FullName': name}
                     )
    response = client.index_faces(CollectionId=COLLECTION_ID,
                                  Image={'S3Object': {
                                      'Bucket': BUCKET, 'Name': fileName}},
                                  ExternalImageId=name,
                                  MaxFaces=2,
                                  QualityFilter="AUTO",
                                  DetectionAttributes=['DEFAULT'])
    print(response)



def button_1_pressed(camera, stream):
    print("pressed")
    led_green.off()
    led_red.blink()

    take_picture(camera, stream)
    name = findName(stream)

    if name:
        response = rekognition.detect_faces(
            Image={'Bytes': stream.getvalue()}, Attributes=['ALL'])
            # pprint (response)
        led_red.off()
        led_green.on()
        print('Detected faces for ' + str(name))
        os.system("espeak \"Hello" + str(name) +
                  "\" --stdout | aplay -D bluealsa:HCI=hci0,DEV=30:C0:1B:8D:BF:7F,PROFILE=a2dp")
        pprint(response['FaceDetails'][0]['Emotions'])
        no_emotion = True
        for faceDetail in response['FaceDetails']:
            for emotion in faceDetail['Emotions']:
                if emotion['Confidence'] > 50:
                    emotion_str = str(emotion['Type'])
                    print("looks like you are," + emotion_str)
                    os.system("espeak \"Looks like you are" + emotion_str
                              + "\" --stdout | aplay -D bluealsa:HCI=hci0,DEV=30:C0:1B:8D:BF:7F,PROFILE=a2dp")
                    no_emotion = False
                if emotion['Type'] == "SAD":
                    if emotion['Confidence'] > 5:
                        print("looks like you are sad")
                        motor.on()
                        print("turn on motor")
                        led_green.on()
                        sleep(10)
                        led_green.off()
                        motor.off()
                        print("turn off motor")

        if no_emotion:
            os.system(
                "espeak \"Hello\"  --stdout | aplay -D bluealsa:HCI=hci0,DEV=30:C0:1B:8D:BF:7F,PROFILE=a2dp")
    else:
        os.system("espeak \"Seems like I don't know you, Can you tell me your name\"  --stdout | aplay -D bluealsa:HCI=hci0,DEV=30:C0:1B:8D:BF:7F,PROFILE=a2dp")
        name_input = input('What is your name? ')
        uploadSingleImg(stream, name_input)
        #print(fileName)
        print(name_input)
        os.system("espeak \"Hello" + str(name_input)
                  + "\" --stdout | aplay -D bluealsa:HCI=hci0,DEV=30:C0:1B:8D:BF:7F,PROFILE=a2dp")


def button2_pressed():
    print("button 2 pressed")

button_1_press_triggered = False

def main():
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        camera.rotation = 90
        camera.start_preview()

        stream = io.BytesIO()

        time.sleep(1)



        while True:  # comment this out if you
            if button1.is_held:
                print("buton 1 held.")
                if not button_1_press_triggered:
                    print('triggering button 1')
                    button_1_pressed(camera, stream)
                    button_1_press_triggered = True
            else:
                button_1_press_triggered = False



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
