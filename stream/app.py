from flask import Flask, request, render_template, Response, jsonify
import cv2
import numpy as np
import threading
import time
import datetime
import os
from camera_opencv import Camera
from control import Car

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')
img_err = cv2.imread(os.path.join(static_file_dir, 'img', 'err-img.png'))
img_err = cv2.imencode(".jpg", img_err)[1]

car = Car().init()


@app.route("/")
def home():
    return render_template("stream.html", message="Hello, World!")


@app.route("/stream")
def streamer():
    # t = threading.Thread(name='stream-thread', target=stream_worker)
    # t.start()
    return Response(gen(Camera()), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/socket.io/control", methods=["POST"])
def handle_control():
    data = request.form
    action = data.get("action")
    timestamp = data.get("time")
    try:
        car.__getattribute__(action)()
    except AttributeError as err:
        return jsonify(status="error", message=str(err)), 500

    return jsonify(status="ok", message="Request sent in thread.")


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def stream_worker():
    while True:
        ret, outputFrame = cap.read()
        if outputFrame is None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + img_err.tobytes() + b'\r\n')
            continue

        (flag, encoded_image) = cv2.imencode(".jpg", outputFrame)

        if not flag:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + img_err.tobytes() + b'\r\n')
            continue

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + encoded_image.tobytes() + b'\r\n')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
