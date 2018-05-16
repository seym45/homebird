import requests
import json
import cv2

# addr = 'http://18.220.219.13:5001'
addr = 'http://localhost:9001'

test_url = addr + '/api/test'

# prepare headers for http request
content_type = 'image/jpeg'
headers = {'content-type': content_type}

img = cv2.imread('test.jpg')

_, img_encoded = cv2.imencode('.jpg', img)
try:
    response = requests.post(test_url, data=img_encoded.tostring(), headers=headers)
    print(json.loads(response.text))
except:
    print('data sending failed or resoponse error')
