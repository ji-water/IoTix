from flask import Flask, render_template, redirect, request, url_for
from pymongo import MongoClient

app = Flask(__name__)


@app.route('/')
def mongoTest():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
