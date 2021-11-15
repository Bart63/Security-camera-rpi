from flask import Flask, render_template, request, redirect

DEBUG = True
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'GET':
        return render_template('form.html')
    else:
        print(request.form)
        return redirect(request.url)


if __name__ == '__main__':
    app.run(host="0.0.0.0")
