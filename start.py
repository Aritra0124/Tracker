from flask import Flask, render_template, redirect, url_for, request, send_from_directory, make_response, session
import pymysql, io, os, time, json

app = Flask(__name__)


@app.route('/')
def hello_world():
    return index()


@app.route('/index')
def index():
    return render_template('starter.html')


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        print(request.get_data(as_text=True))
        return {"status": "OK"}


if __name__ == '__main__':
    app.run(debug=True)
