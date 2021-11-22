from flask import Flask, render_template, request, redirect
from typing import Dict
import json

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
    with open('config.json', 'r') as file:
        data = file.read()
    obj = json.loads(data)
    return obj


def set_vars(obj):
    data = json.dumps(obj)
    with open('config.json', 'w') as file:
        file.write(data)


def fill_vars(values:Dict):
    USER_SETTINGS = get_vars()
    bools = ["DETECT_FACES", "DETECT_BODIES", "DETECT_CONTOURS"]
    integers = ["SECONDS_RECORDING_AFTER_DETECTION", "CONTOUR_MIN_AREA"]

    USER_SETTINGS['DETECT_FACES'] = bool(bools[0] in values.keys())
    USER_SETTINGS['DETECT_BODIES'] = bool(bools[1] in values.keys())
    USER_SETTINGS['DETECT_CONTOURS'] = bool(bools[2] in values.keys())

    if integers[0] in values.keys():
        USER_SETTINGS['SECONDS_RECORDING_AFTER_DETECTION'] = int(values.get(integers[0]))
    if integers[1] in values.keys():
        USER_SETTINGS['CONTOUR_MIN_AREA'] = int(values.get(integers[1]))

    set_vars(USER_SETTINGS)


def print_vars():
    print(get_vars())


def run_app(host="0.0.0.0"):
    app.run(host)

if __name__=='__main__':
    run_app()
    main.main()