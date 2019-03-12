import boto3

s3 = boto3.resource('s3')

# Get list of objects for indexing
images=[('Aiden.jpeg','Aiden'),
      ('Caleb.jpeg','Caleb'),
      ('Effy.jpeg','Effy'),
      ('Elizabeth.jpeg','Niels Bohr'),
      ('Ellen.jpeg','Ellen'),
      ('Hweiyi.jpeg','Huiyi'),
      ('Jenna.jpeg','Jenna'),
      ('Jiyao.jpeg','Jiyao'),
      ('Kimberly.jpeg','Kimberly'),
      ('Yen.jpeg','Yen'),
      ('Effy2.jpeg','Effy'),
      ('Jiyao2.jpg','Jiyao')
      ]

# Iterate through list to upload objects to S3
for image in images:
    file = open("./itpStudents/"+image[0],'rb')
    object = s3.Object('itpface','index/'+ image[0])
    ret = object.put(Body=file,
                    Metadata={'FullName':image[1]}
                    )
