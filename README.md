# Face_Matching
Raspberry Pi Face recognition and emotion detection with AWS Rekognition

### Description
This program is used with AWS Rekognition and pi camera to recognize a person's name and emotion. In its current state, it is triggered by pressing a button. In the future, the button might be replaced by other sensors or openCV face detection.

### build requirements
raspberry pi
pi camera
AWS Rekognition Acess

Alternatively, if you don't have a raspberry pi, you can use master_cv_webcam.py to run it on a computer with a webcam.

### Configure aws access
You will need to ask a AWS credentials from me. After you have the credentials, create a new directory called .aws under your home directory and created a file named credentials under "~.aws/" <br/><br/>


Put the following lines in the credentials file:<br/>

[default]<br/>
aws_access_key_id = [your access key id]<br/>
aws_secret_access_key = [your secret acess key]<br/>
region = us-east-1<br/>

Set up AWS SDK: https://docs.aws.amazon.com/rekognition/latest/dg/setup-awscli-sdk.html<br/><br/>

### Install
#### If you are using a picamera:
```
$ pip install boto3
$ pip install PiCamera
$ pip install pil
```
#### if you are using webcam
```
$ pip install numpy
$ pip install cv2
```

### Use
With a picamera:<br/>
run $master_picam.py<br/>

With a webcam:<br/>
run $master_cv_webcam.py<br/>

To see all the faces in the collection:<br/>
run $listFace.py<br/>

To upload a image to the collection and index a face in the image:<br/>
run $uploadImage.py <filename><person's name><br/>

### Future steps </br>
1. Now faces are all saved locally after captured and being uploaded to aws. this step can be skipped so that pictures are captured and saved directly to stream<br/>
2. Use opencv face detection so that the functions are only triggered after a face is detected. But running that on pi is making it slow so maybe not 
