from flask import Flask
from .utils import add_numbers

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/add/<int:a>/<int:b>')
def add(a, b):
    return str(add_numbers(a, b))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
