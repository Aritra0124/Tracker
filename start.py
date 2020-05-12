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
            session['id'] = id[0]
            return {"status": "Valid user"}
        else:
            return {"status": "Invalid"}


@app.route('/logout')
def logout():
    session.pop('id', None)
    return redirect(url_for('index'))


@app.route('/add_activity', methods=['POST'])
def add_activity():
    if request.method == 'POST':
        data = json.loads(request.get_data(as_text=True))
        print(data)
        if id != None:
            return {"status code": 200, "status": "added"}
        else:
            return {"status code": 404, "status": "Not added"}


@app.route('/activities', methods=['GET'])
def activities():
    if request.method == 'GET':
        #        data = json.loads(request.get_data(as_text=True))
        #        print(data["username"])
        pass
    return jsonify({"activities": ["A", "B", "C"]})


@app.route('/activity_details', methods=['POST'])
def activity_details():
    if request.method == 'POST':
        data = json.loads(request.get_data(as_text=True))
        print(data["activity_name"])
    return jsonify({"activities_details": {"activity_name": "A", "activity_type": "activity_type",
                                           "target_type": "target_type"}})


@app.route('/update_activity', methods=['POST'])
def update_activity():
    if request.method == 'POST':
        data = json.loads(request.get_data(as_text=True))
        print(data)
    return {"status code": 200, "status": "Updated"}


if __name__ == '__main__':
    app.run(debug=True)
