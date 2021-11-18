from flask import Flask, render_template, request, redirect
from typing import Dict
import glob_vars as gv

DEBUG = True
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'GET':
        print_vars()
        return render_template('form.html', vars=get_vars())
    else:
        fill_vars(request.form)
        print(request.form)
        return redirect(request.url)


def get_vars():
    return {
        "DETECT_FACES": gv.DETECT_FACES,
        "DETECT_BODIES": gv.DETECT_BODIES,
        "DETECT_CONTOURS": gv.DETECT_CONTOURS,
        "SECONDS_RECORDING_AFTER_DETECTION": gv.SECONDS_RECORDING_AFTER_DETECTION,
        "CONTOUR_MIN_AREA": gv.CONTOUR_MIN_AREA
    }


def fill_vars(values:Dict):
    bools = ["DETECT_FACES", "DETECT_BODIES", "DETECT_CONTOURS"]
    integers = ["SECONDS_RECORDING_AFTER_DETECTION", "CONTOUR_MIN_AREA"]

    gv.DETECT_FACES = bool(bools[0] in values.keys())
    gv.DETECT_BODIES = bool(bools[1] in values.keys())
    gv.DETECT_CONTOURS = bool(bools[2] in values.keys())

    if integers[0] in values.keys():
        gv.SECONDS_RECORDING_AFTER_DETECTION = int(values.get(integers[0]))
    if integers[1] in values.keys():
        gv.CONTOUR_MIN_AREA = int(values.get(integers[1]))


def print_vars():
    print(gv.DETECT_FACES, gv.DETECT_BODIES, gv.DETECT_CONTOURS,
          gv.SECONDS_RECORDING_AFTER_DETECTION, gv.CONTOUR_MIN_AREA)


if __name__ == '__main__':
    app.run(host="0.0.0.0")
