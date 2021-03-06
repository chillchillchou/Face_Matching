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
from gpiozero import Button

#connect to aws rekognition
bucket='itpface'
collectionId='itpFaces'
s3 = boto3.resource('s3')
client=boto3.client('rekognition')
rekognition = boto3.client('rekognition', region_name='us-east-1')

#define button pin
button = Button(2)

#take a picture and save as a local file
def take_picture():
    with picamera.PiCamera()as camera:
        camera.resolution = (1024, 768)
        camera.start_preview()
        # camera warm up
        time.sleep(1)
        t = str(datetime.datetime.now())
        fileName = re.sub(r'\D', "", t)[4:12]
        file = "img_cap/img_" + fileName + ".jpeg"
        print("Taking image...")
        # Take the actual image we want to keep

        camera.capture(file)

    os.system("espeak \"Hello Hello, I am processing your pictures\"  --stdout | aplay -D bluealsa:HCI=hci0,DEV=70:99:1C:07:86:EE,PROFILE=a2dp");
    return(file)

#upload the captured picture to aws and search for matching face
def findName(file):
    image = Image.open(file)
    stream = io.BytesIO()
    image.save(stream,format="JPEG")
    image_binary = stream.getvalue()

    response = rekognition.detect_faces(
        Image={'Bytes':image_binary}
            )

    all_faces=response['FaceDetails']

    # Initialize list object
    boxes = []

    # Get image diameters
    image_width = image.size[0]
    image_height = image.size[1]

    # Crop face from image
    for face in all_faces:
        box=face['BoundingBox']
        x1 = int(box['Left'] * image_width) * 0.9
        y1 = int(box['Top'] * image_height) * 0.9
        x2 = int(box['Left'] * image_width + box['Width'] * image_width) * 1.10
        y2 = int(box['Top'] * image_height + box['Height']  * image_height) * 1.10
        image_crop = image.crop((x1,y1,x2,y2))

        stream = io.BytesIO()
        image_crop.save(stream,format="JPEG")
        image_crop_binary = stream.getvalue()

        # Submit individually cropped image to Amazon Rekognition
        response = rekognition.search_faces_by_image(
                CollectionId='itpFaces',
                Image={'Bytes':image_crop_binary}
                )
        face_found= len((response["FaceMatches"]))
        if face_found:
            print('found '+str(face_found) + 'face')
            matchedFile = response["FaceMatches"][0]["Face"]["ExternalImageId"]
            # b = matchedFile.index(".")
            # returnName = matchedFile[:b]
            return matchedFile
        if not face_found:
            return


def detectEmotion():

    response = client.detect_faces(
        Image={'S3Object': {'Bucket': bucket, 'Name': photo}}, Attributes=['ALL'])

    print('Detected faces for ' + photo)
    for faceDetail in response['FaceDetails']:
        for emotion in faceDetail['Emotions']:
            if emotion['Confidence'] > 60:
                print(str(emotion['Type']) + ', ' + str(emotion['Confidence']))

def uploadSingleImg(filename,name):
    file = open(fileName,'rb')
    object = s3.Object('itpface', fileName)
    ret = object.put(Body=file,
                    Metadata={'FullName':name}
                    )
    response = client.index_faces(CollectionId=collectionId,
                                    Image={'S3Object':{'Bucket':bucket,'Name':fileName}},
                                    ExternalImageId=name,
                                    MaxFaces=2,
                                    QualityFilter="AUTO",
                                    DetectionAttributes=['DEFAULT'])
    print (response)


while True: #comment this out if you ar enot using a button
    button.wait_for_press() #comment this out if you ar enot using a button
    print ("pressed")
    fileName = take_picture()
    name = findName(fileName)
    if name:
        with open(fileName, 'rb') as image:
            response = rekognition.detect_faces(
                	  Image={'Bytes': image.read()}, Attributes=['ALL'])
        	# pprint (response)
        print('Detected faces for ' + str(name))
        os.system("espeak \"Hello" + str(name) + "\" --stdout | aplay -D bluealsa:HCI=hci0,DEV=70:99:1C:07:86:EE,PROFILE=a2dp")
        no_emotion = True
        for faceDetail in response['FaceDetails']:
            for emotion in faceDetail['Emotions']:
                if emotion['Confidence'] > 50:
                    emotion_str = str(emotion['Type'])
                    print("looks like you are," + emotion_str)
                    os.system("espeak \"Looks like you are" + emotion_str+"\" --stdout | aplay -D bluealsa:HCI=hci0,DEV=70:99:1C:07:86:EE,PROFILE=a2dp");
                    no_emotion=False
        if no_emotion:
            os.system("espeak \"Hello\"  --stdout | aplay -D bluealsa:HCI=hci0,DEV=70:99:1C:07:86:EE,PROFILE=a2dp");
    else:
        os.system("espeak \"Seems like I don't know you, Can you tell me your name\"  --stdout | aplay -D bluealsa:HCI=hci0,DEV=70:99:1C:07:86:EE,PROFILE=a2dp");
        name_input = input('What is your name? ')
        uploadSingleImg(fileName, name_input)
        print (fileName)
        print(name_input)
        os.system("espeak \"Hello" + str(name_input)+"\" --stdout | aplay -D bluealsa:HCI=hci0,DEV=70:99:1C:07:86:EE,PROFILE=a2dp");


    button.wait_for_release() #comment this out if you ar enot using a button
    print ("released")
