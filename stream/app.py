from flask import Flask, request, render_template, Response, send_from_directory
import cv2
import numpy as np
import threading
import time
import datetime
import os
from camera_opencv import Camera

app = Flask(__name__)

static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')
img_err = cv2.imread(os.path.join(static_file_dir, 'img', 'err-img.png'))
img_err = cv2.imencode(".jpg", img_err)[1]


@app.route("/")
def home():
    return render_template("stream.html", message="Hello, World!")


@app.route("/stream")
def streamer():
    # t = threading.Thread(name='stream-thread', target=stream_worker)
    # t.start()
    return Response(gen(Camera()), mimetype="multipart/x-mixed-replace; boundary=frame")


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
