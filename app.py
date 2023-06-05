import io
import json
import os

from flask import Flask, render_template, request

from run import printHtml

app = Flask(__name__)

common = {
    'first_name': 'Junyao Chen',
    'last_name': '',
}


@app.route('/')
def index():
    return render_template('home.html', common=common)

@app.route('/maxcut')
def maxcut():
    return render_template('maxcut.html', common=common, slides=printHtml())




@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', common=common), 404


def get_static_file(path):
    site_root = os.path.realpath(os.path.dirname(__file__))
    return os.path.join(site_root, path)


def get_static_json(path):
    return json.load(open(get_static_file(path)))


if __name__ == "__main__":
    print("running py app")
    app.run(host="127.0.0.1", port=5000, debug=True)
