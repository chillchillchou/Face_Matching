import numpy as np
import cv2
import boto3
import io
from PIL import Image
from pprint import pprint
import os
import re
import pyttsx3
import time
import picamera
from gpiozero import Button

#connect to aws server
rekognition = boto3.client('rekognition', region_name='us-east-1')
#dynamodb = boto3.client('dynamodb', region_name='us-east-1')

#define button pin
button = Button(17)

def take_picture():
    with picamera.PiCamera()as camera:
        camera.resolution = (1024,768)
        camera.start_preview()
        #camera warm up
        time.sleep(1)
        t = str(datetime.datetime.now())
        fileName=re.sub(r'\D',"",t)[4:12]
        file = "img_cap/img_"+fileName+".jpeg"
        print("Taking image...")
        # Take the actual image we want to keep

        camera.capture(file)

    os.system("say Hello 'I am processing picture'")
    return(file)

def findName (file):
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
        pprint (response)
        matchedFile = response["FaceMatches"][0]["Face"]["ExternalImageId"]
        # b = matchedFile.index(".")
        # returnName = matchedFile[:b]
        return matchedFile
        engine.pyttsx.init()
        engine.say('Good morning.')

def detectEmotion ():

    response = client.detect_faces(Image={'S3Object':{'Bucket':bucket,'Name':photo}},Attributes=['ALL'])

    print('Detected faces for ' + photo)
    for faceDetail in response['FaceDetails']:
        for emotion in faceDetail['Emotions']:
            if emotion['Confidence'] > 60:
                print(str(emotion['Type']) + ', ' + str(emotion['Confidence']))

# Now trigger the event after button is pressed
button.wait_for_press()
# take a picture and return the name of the filename
fileName=take_picture()
#submitting the picture to aws Rekognition and serch for matching name
name=findName(fileName)
print('Detected faces for ' + name)
engine = pyttsx3.init();
engine.say("hello, "+name);

#detect emtotion
with open(fileName, 'rb') as image:
        response = rekognition.detect_faces(Image={'Bytes': image.read()}, Attributes=['ALL'])
#pprint (response)

#flag for emotion detection
no_emotion=True
for faceDetail in response['FaceDetails']:
    for emotion in faceDetail['Emotions']:
#print the emotion if one of the emotion types have confidence score larger than 50 
        if emotion['Confidence'] > 50:
            engine.say("Looks like you are "+str(emotion['Type']));
            no_emotion=False
if no_emotion:
    engine.say("Looks like you are not displaying any emotion")

engine.runAndWait();
