import boto3
import json
from pprint import pprint

if __name__ == "__main__":
    # Change bucket to your S3 bucket that contains the image file.
    # Change photo to your image file.
    bucket='itpface'
    collectionId='itpFaces'
    photo='Ellen.jpeg'
    imageFile='test.jpeg'
    client=boto3.client('rekognition')

    with open(imageFile, 'rb') as image:
        response = client.detect_faces(Image={'Bytes': image.read()}, Attributes=['ALL'])

    pprint (response)
    # response = client.detect_faces(Image={'S3Object':{'Bucket':bucket,'Name':photo}},Attributes=['ALL'])
    # print('Detected faces for ' + photo)
    # for faceDetail in response['FaceDetails']:
    #     for emotion in faceDetail['Emotions']:
    #         if emotion['Confidence'] > 60:
    #             print(str(emotion['Type']) + ', ' + str(emotion['Confidence']))

        # print('The detected face is  ' + str(faceDetail['AgeRange']['Low'])
        #       + ' and ' + str(faceDetail['AgeRange']['High']) + ' years old')
    # print('Here are the other attributes:')
    # print(json.dumps(faceDetail, indent=4, sort_keys=True))
