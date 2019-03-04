import pprint

import boto3

# Set this to whatever percentage of 'similarity'
# you'd want
SIMILARITY_THRESHOLD = 75.0

if __name__ == '__main__':

    #create collection
    maxResults=2
    collectionId='itpFaces'

    client=boto3.client('rekognition')

    #Create a collection
    print('Creating collection:' + collectionId)
    response=client.create_collection(CollectionId=collectionId)
    print('Collection ARN: ' + response['CollectionArn'])
    print('Status code: ' + str(response['StatusCode']))
    print('Done...')


    # fileName = 'Elizabeth.jpeg'
    # bucket = 'itpface'
    #
    #
    # # with open('source.jpg', 'rb') as source_image:
    # #     source_bytes = source_image.read()
    #
    # with open('target.jpg', 'rb') as target_image:
    #     target_bytes = target_image.read()
    #
    # response = client.compare_faces(
    #                SourceImage={ 'S3Object':{'Bucket':bucket,'Name':fileName}},
    #                TargetImage={ 'Bytes': target_bytes },
    #                SimilarityThreshold=SIMILARITY_THRESHOLD
    # )

    pprint.pprint(response)
