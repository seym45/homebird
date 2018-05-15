import os
from flask import Flask, request, render_template, send_from_directory
__author__ = 'seym45'
app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

from flask import Flask, request, Response, render_template, jsonify
import jsonpickle
import numpy as np
import cv2
import datetime
import base64
from io import BytesIO
from PIL import Image
def convert_and_save(file):
    starter = file.find(',')
    image_data = file[starter + 1:]
    image_data = bytes(image_data, encoding="ascii")
    im = Image.open(BytesIO(base64.b64decode(image_data)))
    im = im.convert('RGB')
    im.save('images/image.jpg')


@app.route('/up', methods=['POST','GET'])
def upload_base64_file(): 
     img_data = request.form['img']
     name_rel = request.form['name']
     # this method convert and save the base64 string to image
     convert_and_save(img_data)
     return jsonify({'name_rel':name_rel})


import boto3
import datetime
import json
@app.route('/status')
def status():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('hbdb')
    timestamp = str(datetime.datetime.now())
    response = table.scan()
    res = (jsonify(response['Items']))
    return res



# route http posts to this method
@app.route('/api/test', methods=['POST'])
def test():
    r = request
    # convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    name = str(datetime.datetime.now()).replace(':', '').replace(' ','').replace('.','').replace('-','')
    name  = '1_unknown_'+name+ '.jpg'
    img_dir = 'images/'
    img_name = img_dir + name
    # do some fancy processing here....
    cv2.imwrite(img_name,img)
    s3 = boto3.client('s3')
    bucket_name = 'homebird'
    s3.upload_file(img_name, bucket_name, img_name)

    # build a response dict to send back to client
    response = {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0])
                }
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route("/")
def index():
    return render_template("index.html")



@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)


@app.route('/gallery')
def get_gallery():
    image_names = os.listdir('./images')
    print(image_names)
    return render_template("gallery.html", image_names=image_names)

if __name__ == "__main__":
    app.run(port=5001, debug=True, host='0.0.0.0')
