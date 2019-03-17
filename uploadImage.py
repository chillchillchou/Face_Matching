import boto3
import sys
from pprint import pprint

fileName = sys.argv[1]
name = sys.argv[2]


bucket='itpface'
collectionId='itpFaces'
s3 = boto3.resource('s3')
client=boto3.client('rekognition')

# Get list of objects for indexing
images=[('Aiden.jpeg','Aiden'),
      ('Caleb.jpeg','Caleb'),
      ('Effy.jpeg','Effy'),
      ('Elizabeth.jpeg','Elizabeth'),
      ('Ellen.jpeg','Ellen'),
      ('Hweiyi.jpeg','Huiyi'),
      ('Jenna.jpeg','Jenna'),
      ('Jiyao.jpeg','Jiyao'),
      ('Kimberly.jpeg','Kimberly'),
      ('Yen.jpeg','Yen')
      ]


def uploadSingleImg():
    file = open("./itpStudents/"+fileName,'rb')
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
    pprint (response)

# Iterate through list to upload objects to S3
def uploadImages():
    for image in images:
        file = open("./itpStudents/"+image[0],'rb')
        object = s3.Object('itpface', image[0])
        ret = object.put(Body=file,
                        Metadata={'FullName':image[1]}
                        )
        client.index_faces(CollectionId=collectionId,
                                        Image={'S3Object':{'Bucket':bucket,'Name':image[0]}},
                                        ExternalImageId=image[1],
                                        MaxFaces=2,
                                        QualityFilter="AUTO",
                                        DetectionAttributes=['DEFAULT'])

uploadSingleImg()
