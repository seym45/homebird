 # Homebird 
### 
A camera mounted on door attached with Raspberry PI, sends images to AWS EC2 backend whenever a face is detected. 
Then the face is analyzed by AWS Rekognition, the result is stored in AWS S3 storage. Developed the backend to handle 
reqeusts with python flask and wrote python scripts on Raspberry Pi to support the whole system. Through an android
app user would be notified if there were any events like `Unknown face Detected` or `Mr. X is in front of your door`.
