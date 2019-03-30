#Face_Matching
Raspberry Pi Face recognition and emotion detection with AWS Rekognition

###Description
This program is used with AWS Rekognition and pi camera to recognize a person's name and emotion. In its current state, it is triggered by pressing a button. In the future, the button might be replaced by other sensors or openCV face detection.

###build requirements
raspberry pi
pi camera
AWS Rekognition Acess

Alternatively, if you don't have a raspberry pi, you can use master_cv_webcam.py to run it on a computer with a webcam.

###Configure aws access
You will need to ask a AWS credentials from me. After you have the credentials, create a new directory called .aws under your home directory and created a file named credentials under "~.aws/" <br/>"


Put the following lines in the credentials file:

[default]
aws_access_key_id = [your access key id]
aws_secret_access_key = [your secret acess key]
region = us-east-1

Set up AWS SDK: https://docs.aws.amazon.com/rekognition/latest/dg/setup-awscli-sdk.html

###install
#### If you are using a pi:
$pip install boto3
$pip install PiCamera
