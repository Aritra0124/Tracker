from flask import Flask, render_template, redirect, url_for, request, send_from_directory, make_response
import pymysql, io,os, time, json
from base64 import b64encode
from werkzeug.utils import secure_filename
import num2word, pdfkit

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "../p-v-e/temp_image"


session = {}



def preprosessing():
	disability_name = []
	affected_bodypart = []
	diagnosis =[]
	disability_percent = []
	disability = {'1':'Locomotor Disability','2':'Muscular Dystrophy','3':'Leprosy Cured','4':'Dwarfism','5':'Cerebral Palsy','6':'Acid name Attack Victim','7':'Low Vision','8':'Blindness','9':'Deaf','10':'Hard of Hearing',
					'11':'Speech and Language Disability','12':'Intellectual Disability','13':'Specific Learning Disability','14':'Autism Spectrum Disorder','15':'Mental Illness','16':'Chronic Neurological Condition','17':'Multiple Sclerosis','18':"Parkinson's Disease",'19':'Haemophilia','20':'Thalassemia',
					'21':'Sickle Cell Disease'}
	for i in range(1,len(disability)+1):
		try:
			if session['disability'][disability[str(i)]] == 'on':
				temp = disability[str(i)]
				if temp == 'Locomotor Disability':
					body_part = session['disability'][disability[str(i)] + " affect"] +" "+ session['disability'][disability[str(i)] + " bodypart"]
					affected_bodypart.append(body_part)
				else:
					affected_bodypart.append(session['disability'][disability[str(i)]+" affect"])
				disability_name.append(temp)
				diagnosis.append(session['disability'][disability[str(i)]+" diagnosis"])
				disability_percent.append(session['disability'][disability[str(i)]+" percent"])
		except:
			pass

	db = pymysql.connect("localhost","pmauser","aritraroot","disability_managment_system" )
	cursor = db.cursor()
	print(len(disability_name))
	print(disability_name)
	for i in range(0,len(disability_name)):
		sql = ("""insert into disability_details values(0,"%s","%s","%s","%s","%s","%s","%s")""")
		cursor.execute(sql,(session['personal']['regno'],disability_name[i],affected_bodypart[i],diagnosis[i],int(disability_percent[i]),session['condition']['condition'],session['condition']['reassessment']))
	cursor.execute("""insert into disability_status values(0,"%s",0,"Not Issue",NOW())""",(session['personal']['regno']))
	db.commit()
	db.close()


@app.route('/')
def hello_world():
	return 'Hello World from python server'


@app.route('/index')
def index():
	session.clear()
	return render_template('starter.html')


@app.route('/end')
def end():
	session.clear()
	return render_template('end.html')


@app.route('/test')
def test():
	db = pymysql.connect("localhost","pmauser","aritraroot","labtest" )
	cursor = db.cursor()
	with open("../p-v-e/temp_image/photo_01.jpg", "rb") as f:
		photo = f.read()
	sql = ("""insert into Details values(0, "test_name", "test", "test@test.com","test12345", "10-10-2019", "%s")""")
	cursor.execute(sql,photo)
	db.commit()
	sql = "select dp from Details where id = 10"
	cursor.execute(sql)
	detail = cursor.fetchall()
	db.close()

	image = detail[0][0]
	with open("photo_01.jpg", "wb") as f:
		f.write(image)
	return render_template('image_test.html', image = image)


@app.route('/submit', methods = ['POST','GET'])
def submit():
	if request.method == 'POST':
		form3 = request.form
		session["condition"] = form3
		photo_name = "photo_"+session['regno']+".jpg"
		doc_name = "residence_"+session['regno']+".jpg"
		os.system("cp " +"../p-v-e/temp_image/photo_"+session['regno']+".jpg " + " ../p-v-e/static/image/photo_"+session['regno']+".jpg")
		os.system("cp " +"../p-v-e/temp_image/residence_"+session['regno']+".jpg " + " ../p-v-e/static/image/residence_"+session['regno']+".jpg")
		with open("../p-v-e/temp_image/photo_"+session['regno']+".jpg", 'rb') as f:
			photo = f.read()
		with open("../p-v-e/temp_image/residence_"+session['regno']+".jpg", 'rb') as f:
			doc = f.read()
		db = pymysql.connect("localhost","pmauser","aritraroot","disability_managment_system" )
		cursor = db.cursor()
		sql = ("""insert into personal_details values(0,"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s",NOW())""")
		cursor.execute(sql,(session['personal']['regno'],session['personal']['salutation'],session['personal']['name'],session['personal']['swd'],session['personal']['swdof'],session['personal']['dob'],int(session['personal']['age']),session['personal']['gender'],session['personal']['prohn'],session['personal']['wavilst'],session['personal']['po'],session['personal']['district'],session['personal']['state'],session['personal']['id'],int(session['personal']['card_no']),session['personal']['doi'],session['personal']['daic'],photo,doc,photo_name, doc_name))
		db.commit()
		db.close()
		preprosessing()
	return redirect(url_for('end'))

@app.route('/view',  methods = ['POST', 'GET'])
def view():
	temp={}
	if request.method == 'POST':
		form2 = request.form
		for key in form2:
			if form2[key] == '' or form2[key] == 'none':
				pass
			else:
				temp[key] = form2[key]
		session["disability"] = temp
		photo = "../p-v-e/temp_image/photo_"+session['regno']+".jpg"
		doc = "../p-v-e/temp_image/residence_"+session['regno']+".jpg"
	return render_template('view.html', form = session, photo =photo, doc = doc)

@app.route('/dis',  methods = ['POST', 'GET'])
def disability():
	if len(session) <= 0:
		return redirect(url_for('index'))
	else:
		if request.method == 'POST':

			form1 = request.form
			session["personal"] = form1
			photos = request.files['photo']
			docs = request.files['residence']
			photo = secure_filename(photos.filename)
			doc = secure_filename(docs.filename)
			photos.save(os.path.join(app.config['UPLOAD_FOLDER'], photo))
			os.rename("../p-v-e/temp_image/"+photo, "../p-v-e/temp_image/photo_"+session['regno']+".jpg")
			docs.save(os.path.join(app.config['UPLOAD_FOLDER'], doc))
			os.rename("../p-v-e/temp_image/"+doc, "../p-v-e/temp_image/residence_"+session['regno']+".jpg")


			#im_to_blob(filename)
			return render_template('disability_details.html', regno = session["regno"])


@app.route('/form')
def form():
	if len(session)<=0:
			return redirect(url_for('index'))
	return render_template('form.html', regno = session["regno"])


@app.route('/check', methods = ['POST', 'GET'])
def check():
	if request.method == 'POST' and request.form['regno'] !='' :
		regno = request.form['regno']
		session["regno"] = regno
	else:
		flash("No registration no")
		return redirect(url_for('index'))

	return redirect(url_for('form'))




@app.route('/details/<regno>')
def details(regno):
	personal = []
	disability = []
	db = pymysql.connect("localhost","pmauser","aritraroot","disability_managment_system" )
	cursor = db.cursor()
	sql = """select registration_no,salutation,Name,swd,swdof,dob,age,gender,prohn,wavilst,po,district,state,id,card_no,doi,daic,photo_name from personal_details where registration_no = %s"""
	cursor.execute(sql, regno)
	detail =list( cursor.fetchall())
	for i in range(0,len(detail)):
		personal.append(list(detail[i]))
	for i in range(0,len(personal)):
		image = personal[i][17]

	sql = "select * from disability_details where reg_no = %s"
	cursor.execute(sql,regno)
	disable =list( cursor.fetchall())
	for i in range(0,len(disable)):
		disability.append(list(disable[i]))


	sql = "select sl_no from disability_status where reg_no = %s"
	cursor.execute(sql,regno)
	sl_no =list(cursor.fetchone())
	db.close()
	print(image)
	certificate_no = str("temp/" + regno[1:-1] + "/" + str(sl_no[0]))
	return render_template("certificate.html", image =image, certificate_no = certificate_no, date = time.asctime() ,personal = personal ,disability = disability, word_percent = num2word.word(disability[0][5]), valid = time.localtime()[0] + 5)


@app.route('/doc/<regno>')
def doc(regno):
	personal = []
	disability = []
	db = pymysql.connect("localhost","pmauser","aritraroot","disability_managment_system" )
	cursor = db.cursor()
	sql = """select registration_no,salutation,Name,swd,swdof,dob,age,gender,prohn,wavilst,po,district,state,id,card_no,doi,daic,photo_name from personal_details where registration_no = %s"""
	cursor.execute(sql, regno)
	detail =list( cursor.fetchall())
	for i in range(0,len(detail)):
		personal.append(list(detail[i]))
	for i in range(0,len(personal)):
		image = personal[i][17]

	sql = "select * from disability_details where reg_no = %s"
	cursor.execute(sql,regno)
	disable =list( cursor.fetchall())
	for i in range(0,len(disable)):
		disability.append(list(disable[i]))


	sql = "select sl_no from disability_status where reg_no = %s"
	cursor.execute(sql,regno)
	sl_no =list(cursor.fetchone())

	certificate_no = str( str(sl_no[0]) + "/" + str(time.localtime()[0]))

	sql = "update disability_status set certificate_no = %s, issue_status = %s  where reg_no = %s"
	cursor.execute(sql, (certificate_no, "Issued", regno))
	db.commit()
	db.close()

	options = {
    'page-size': 'A4',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
    'encoding': "UTF-8",
    }
	rendered = render_template("certificate.html",image = image, certificate_no = certificate_no, date = time.asctime() ,personal = personal ,disability = disability, word_percent = num2word.word(disability[0][5]), valid = time.localtime()[0] + 5)
	pdf = pdfkit.from_string(rendered, False, options = options )
	response = make_response(pdf)
	response.headers['Content-Type'] = 'application/pdf'
	response.headers['Content-Disposition'] = 'inline; filename=certificate.pdf'
	return response


@app.route('/search', methods = ['POST'])
def search():
	details = []
	print(request.get_data(as_text=True))
	tag, data = str(request.get_data())[2:-1].split("&")
	tag = tag.split('=')[1].replace("+", " ")
	data = data.split('=')[1]
	print(tag)
	print(data)
	if tag != "Name" or tag != "po":
		data = int(data)
		sql = "select sl_no,reg_no,certificate_no,issue_status from disability_status where reg_no in(select registration_no from personal_details where card_no = %s)limit 0, 50"
	elif tag == "Name":
		sql = "select sl_no,reg_no,certificate_no,issue_status from disability_status where reg_no in(select registration_no from personal_details where Name = %s)limit 0, 50"
	elif tag == "po":
		sql = "select sl_no,reg_no,certificate_no,issue_status from disability_status where reg_no in(select registration_no from personal_details where po = %s)limit 0, 50"

	print(tag)
	print(data)
	db = pymysql.connect("localhost","pmauser","aritraroot","disability_managment_system" )
	cursor = db.cursor()
#	sql = "select sl_no,reg_no,certificate_no,issue_status from disability_status where reg_no in(select registration_no from personal_details where card_no = %s)limit 0, 50"
	cursor.execute(sql,data)
	db.close()
	detail =list( cursor.fetchall())
	print(sql,(tag,data))
	for i in range(0,len(detail)):
		details.append(list(detail[i]))
	return {"status":"ok", "data":details}

@app.route('/approve')
def approve():
	details = []
	db = pymysql.connect("localhost","pmauser","aritraroot","disability_managment_system" )
	cursor = db.cursor()
	sql = "select sl_no,reg_no,certificate_no,issue_status from disability_status"
	cursor.execute(sql)
	db.close()
	detail =list( cursor.fetchall())
	for i in range(0,len(detail)):
		details.append(list(detail[i]))
	return render_template("approve.html", form = details, result = [] )

@app.route('/login', methods = ['POST', 'GET'])
def login():
	error = None
	if request.method == 'POST':
		if request.form["email"] == 'aritra@aritra.com' and request.form["psw"] == "123456789":
			return redirect(url_for('approve'))
		else:
			error = "Invalid!!!"
	return render_template('login.html', error=error)



if __name__ == '__main__':
	app.run(debug = True)