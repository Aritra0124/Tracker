from flask import Flask, render_template, redirect, url_for, request, send_from_directory, make_response, session, \
    jsonify
import pymysql, io, os, time, json

app = Flask(__name__)
app.secret_key = "tracking system"


def login_validation(username, password):
    db = pymysql.connect("localhost", "pmauser", "aritraroot", "labtest")
    cursor = db.cursor()
    sql = "select id from Details where email = %s and password = %s"
    cursor.execute(sql, (username, password))
    db.close()
    id = cursor.fetchone()
    return id


@app.route('/')
def hello_world():
    return index()


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = json.loads(request.get_data(as_text=True))
        id = login_validation(data['username'], data['password'])
        if id != None:
            print(id[0])
            session['id'] = id[0]
            return {"status": "Valid user"}
        else:
            return {"status": "Invalid"}


@app.route('/logout')
def logout():
    session.pop('id', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
