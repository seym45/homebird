import os

from flask import Flask, request, render_template, send_from_directory

__author__ = 'ibininja'

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


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

    app.run(port=5001, debug=False)
