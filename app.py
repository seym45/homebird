import os
from flask import Flask, request, render_template, send_from_directory, Response, render_template, jsonify
import jsonpickle
import numpy as np
import cv2
import datetime, time
import base64
from io import BytesIO
from PIL import Image
from AWS import AWS
from threading import Thread

__author__ = 'seym45'
app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
PORT = 9001
PUBLIC_IP = '18.220.219.13'

def convert_and_save(file,people_name, relation):
    starter = file.find(',')
    image_data = file[starter + 1:]
    image_data = bytes(image_data, encoding="ascii")
    im = Image.open(BytesIO(base64.b64decode(image_data)))
    im = im.convert('RGB')
    img_name = str(time.time()).replace('.','')+'.jpg'
    dir_name = os.path.join(APP_ROOT,'images', img_name)
    im.save(dir_name)

    data = {
        'name':people_name,
        'relation':relation,
        'image_bucket_key':img_name
    }
    thread = Thread(target=AWS.put_item_db(tablename='people',data=data))
    thread.start()
    thread2 = Thread(target=AWS.put_item_bucket(sourcename=dir_name, targetname=img_name))
    thread2.start()


@app.route('/up', methods=['POST', 'GET'])
def upload_base64_file():
    img_data = request.form['img']
    name = request.form['name']
    relation = request.form['relation']
    thread = Thread(target=convert_and_save(img_data,name,relation))
    thread.start()
    return jsonify({'name': name,'realtion':relation,})


@app.route('/status')
def status():
    return jsonify(AWS.get_item__db('status'))


def pi2aws_process_image(img):
    t = time.time()
    print(str(pi2aws_process_image.__name__))
    name = str(time.time()).replace('.', '') + '.jpg'
    dir_name = os.path.join(APP_ROOT, 'images', name)
    cv2.imwrite(dir_name, img)

    AWS.put_item_bucket(sourcename=dir_name,targetname=name)

    people = AWS.get_item__db('people')
    keys = [item['image_bucket_key'] for item in people]
    print(keys)

    matched_key = AWS.compare_faces_among_all(unknown_key=name, known_keys=keys)
    print('match: ' + str(matched_key))

    if matched_key is None:
        person_name = 'unknown'
    else:
        # for person in people:
        #     if person['image_bucket_key'] == matched_key:
        #         person_name = person['name']
        #         break

        person_name = next((item['name'] for item in people if item['image_bucket_key'] == matched_key),False)

    local_url = r'http://' + PUBLIC_IP + ':' + str(PORT) + r'/upload/' + name
    data = {
        'name':person_name,
        'url':local_url,
        'timestamp':str(datetime.datetime.now()),
    }
    print(data)
    AWS.put_item_db(tablename='status', data=data)
    print('time elapsed: ' + str(time.time()-t) )

# rcv iamge from pi
@app.route('/api/test', methods=['POST'])
def test():
    r = request
    nparr = np.fromstring(r.data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    thread = Thread(target=pi2aws_process_image(img))
    thread.start()
    response = {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0])}
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
    app.run(port=PORT, debug=True)
