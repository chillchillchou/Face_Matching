import numpy as np
import cv2
import boto3
import io
from PIL import Image
from pprint import pprint
import os
import datetime
import re
import pyttsx3



# Camera 0 is the integrated web cam on my netbook
camera_port = 0

#Number of frames to throw away while the camera adjusts to light levels
ramp_frames = 30

rekognition = boto3.client('rekognition', region_name='us-east-1')
dynamodb = boto3.client('dynamodb', region_name='us-east-1')



# Captures a single image from the camera and returns it in PIL format
def get_image(camera):
 retval, im = camera.read()
 return im

# Ramp the camera - these frames will be discarded and are only used to allow v4l2
# to adjust light levels, if necessary

def take_picture():
    # initialize the camera capture object with the cv2.VideoCapture class.
    camera = cv2.VideoCapture(camera_port)
    for i in range(ramp_frames):
     temp = get_image(camera)
    print("Taking image...")
    # Take the actual image we want to keep
    camera_capture = get_image(camera)
    t = str(datetime.datetime.now())
    fileName=re.sub(r'\D',"",t)[4:12]
    print(fileName)
    file = "img_cap/img_"+fileName+".jpeg"

    # imwrite method will automatically choose the
    # correct format based on the file extension you provide. Convenient!
    cv2.imwrite(file, camera_capture)
    os.system("say Hello 'I am processing picture'")


    # release the camera
    del(camera)
    return file

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

fileName=take_picture()
name=findName(fileName)
with open(fileName, 'rb') as image:
        response = rekognition.detect_faces(Image={'Bytes': image.read()}, Attributes=['ALL'])
pprint (response)
print('Detected faces for ' + name)
engine = pyttsx3.init();
engine.say("hello, "+name);

no_emotion=True
for faceDetail in response['FaceDetails']:
    for emotion in faceDetail['Emotions']:
        if emotion['Confidence'] > 50:
            # print(str(emotion['Type']) + ', ' + str(emotion['Confidence']))
            engine.say("Looks like you are "+str(emotion['Type']));
            no_emotion=False
if no_emotion:
    engine.say("Looks like you are not displaying any emotion")

engine.runAndWait();
