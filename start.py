from flask import Flask, render_template, redirect, url_for, request, send_from_directory, make_response, session, \
    jsonify
import pymysql, io, os, time, json

app = Flask(__name__)
app.secret_key = "tracking system"


def graph_data():
    db = pymysql.connect("localhost", "pmauser", "aritraroot", "tracker")
    cursor = db.cursor()
    sql = '''select DATE(entry_time), TIME_FORMAT(SEC_TO_TIME(total_time),'%%Hh %%im') from activity_update where user_id = %s and activity_id = %s'''
    cursor.execute(sql, (session["id"], session["activity_id"]))
    db.close()
    date_time = cursor.fetchall()
    label = []
    time = []
    for data in date_time:
        date, total_time = data
        label.append(date)
        time.append(total_time)
    return label, time


def get_details(activity_name):
    db = pymysql.connect("localhost", "pmauser", "aritraroot", "tracker")
    cursor = db.cursor()
    sql = "select activity_id, activity_name, activity_type, target_type from activity_entry where user_id = %s and activity_name = %s"
    cursor.execute(sql, (session["id"], activity_name))
    db.close()
    data = cursor.fetchone()
    return data


def get_activities():
    db = pymysql.connect("localhost", "pmauser", "aritraroot", "tracker")
    cursor = db.cursor()
    sql = "select activity_name from activity_entry where user_id = %s"
    cursor.execute(sql, (session["id"]))
    db.close()
    data = list(cursor.fetchall())
    return data


def activity_update(data):
    db = pymysql.connect("localhost", "pmauser", "aritraroot", "tracker")
    cursor = db.cursor()
    sql = "select TIMEDIFF(%s, %s)"
    cursor.execute(sql, (data["to_time"], data["from_time"]))
    total_time = cursor.fetchone()
    sql = "insert into activity_update values(0,%s, %s, NOW(), %s, %s, %s)"
    id = cursor.execute(sql, (
        session["activity_id"], session['id'], data["from_time"], data["to_time"],
        total_time))
    db.commit()
    db.close()
    # id = cursor.fetchone()
    return id


def activity_entry(data):
    db = pymysql.connect("localhost", "pmauser", "aritraroot", "tracker")
    cursor = db.cursor()
    sql = "insert into activity_entry values(0,%s, 0,%s, %s, %s, %s)"
    id = cursor.execute(sql, (
        session['id'], data["activity_name"], data["activity_type"], str(data["target_type"]), data["activity_note"]))
    db.commit()
    db.close()
    # id = cursor.fetchone()
    return id


def create_user(name, email, password):
    db = pymysql.connect("localhost", "pmauser", "aritraroot", "tracker")
    cursor = db.cursor()
    sql = "insert into user_data values(0, %s, %s, %s)"
    id = cursor.execute(sql, (name, email, password))
    db.commit()
    db.close()
    # id = cursor.fetchone()
    return id


def login_validation(username, password):
    db = pymysql.connect("localhost", "pmauser", "aritraroot", "tracker")
    cursor = db.cursor()
    sql = "select id, name from user_data where email_id = %s and password = %s"
    cursor.execute(sql, (username, password))
    db.close()
    id = list(cursor.fetchone())
    return id


@app.route('/index')
def hello_world():
    return index()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = json.loads(request.get_data(as_text=True))
        id = login_validation(data['username'], data['password'])
        if id[0] != None:
            session['id'] = id[0]
            return {"status": "Valid user", "name": id[1]}
        else:
            return {"status": "Invalid"}


@app.route('/create_login', methods=['POST'])
def create_login():
    if request.method == 'POST':
        data = json.loads(request.get_data(as_text=True))
        id = create_user(data['username'], data["email_id"], data['password'])
        if id != None:
            return {"status": "Valid user"}
        else:
            return {"status": "Invalid"}


@app.route('/logout')
def logout():
    session.pop('id', None)
    session.pop('activity_id', None)
    return redirect(url_for('index'))


@app.route('/add_activity', methods=['POST'])
def add_activity():
    if request.method == 'POST':
        data = json.loads(request.get_data(as_text=True))
        activity_entry(data)
        if id != None:
            return {"status code": 200, "status": "added"}
        else:
            return {"status code": 404, "status": "Not added"}


@app.route('/activities', methods=['GET'])
def activities():
    if request.method == 'GET':
        activities = get_activities()
    return jsonify({"activities": activities})


@app.route('/activity_details', methods=['POST'])
def activity_details():
    if request.method == 'POST':
        data = json.loads(request.get_data(as_text=True))
        activity_details = get_details(data["activity_name"])
        session['activity_id'] = activity_details[0]
        labels, total_time = graph_data()
        target_time = []
        print(activity_details)
        for i in range(len(labels)):
            target_time.append(activity_details[3])
    return jsonify({"activities_details": {"activity_name": activity_details[1], "activity_type": activity_details[2],
                                           "target_type": activity_details[3]},
                    "dataset": {"labels": labels, "data": total_time, "target_time": target_time}})


@app.route('/update_activity', methods=['POST'])
def update_activity():
    if request.method == 'POST':
        data = json.loads(request.get_data(as_text=True))
        id = activity_update(data)
        if id != None:
            return {"status code": 200, "status": "Updated"}
        else:
            return {"status code": 404, "status": "Not Updated"}


@app.route('/graph')
def graph():
    return render_template("graph_test.html")


if __name__ == '__main__':
    app.run(debug=True)
