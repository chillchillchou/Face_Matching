from __future__ import print_function
import numpy as np
import cv2
import boto3
import io
from PIL import Image
from pprint import pprint

rekognition = boto3.client('rekognition', region_name='us-east-1')
dynamodb = boto3.client('dynamodb', region_name='us-east-1')

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
        # matchedFile = response["FaceMatches"][0]["Face"]["ExternalImageId"]
        # b = matchedFile.index(".")
        # returnName = matchedFile[:b]

        pprint(response)


findName("img_03161633.jpeg")
