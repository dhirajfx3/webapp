from flask import *
import sys
import os
import flask_sijax

from Home import *
from Admin import *
from Letters import *
from library import *
from Student import *
from timetable import *

from Table import attempt_creating_tables
from cryptography.fernet import Fernet
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from email.MIMEBase import MIMEBase
import re
from MySQLdb import connect
from email.utils import parseaddr
from threading import Thread
from DatabaseOperation import *

path = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')
app= Flask(__name__)
app.config['SIJAX_STATIC_PATH'] = path
app.config['SIJAX_JSON_URI'] = '/static/js/sijax/json2.js'
flask_sijax.Sijax(app)
app.register_blueprint(hp)
app.register_blueprint(apg)
app.register_blueprint(library)
app.register_blueprint(student)
app.register_blueprint(timetable)
app.register_blueprint(letters)
app.secret_key="sdljksd21e-ds;lf"
connector=connect("localhost","root","dhirajfx3","facarts");
curs=connector.cursor()
@app.route('/add_user/',methods=['Get','Post'])
def add_user():
	email=request.args.get('a')
	fname=request.args.get('b')
	lname=request.args.get('c')
	id=request.args.get('d')
	e=request.args.get('e')
	f=alphaNum(20)
	try:
		if parseaddr(email)[0]=="" and parseaddr(email)[1]==email and len(email)!=0:
			if add_to_database(id,email,f,e,fname,lname)==False:
				return jsonify("Some error occurred in inserting into database.\nPlease try again later.")
			object=SMTP('smtp.gmail.com:587')
			object.starttls()
			un='dhirajfx2@gmail.com'
			pwd='NCR356$#!'
			object.login(un,pwd)
			Rf=""
			if e=='1':
				Rf="Admin"
			elif e=='2':
				Rf="Office personnel"
			elif e=='3':
				Rf="Faculty"
			elif e=='4':
				Rf="Student"
			msg={'From':"dhirajfx2@gmail",'To':email,'Subject':'Do not Reply'}
			mine_mime=MIMEMultipart()
			text=MIMEText('Hello {0} !!!\n Your {2} account has been created on Faculty of Arts portal and your user id is :{3} and temporary password is {1}'.format(email,f,Rf,id),'plain')
			mine_mime.attach(text)
			for z in msg.keys():
				mine_mime[z]=msg[z]
			msg=mine_mime.as_string()
			def fn(obj):
				obj.sendmail(un,email,msg);
				obj.quit()
			
			Thread(target=fn,args=(object,)).start()
			
			return jsonify(msg="{3} account for {0} with id {1} is created\nFurther instructions are sent to {2}".format(fname,id,email,Rf))
	except:
		return jsonify(msg="Some error occurred\nPlease try again later.")
	return jsonify(msg="INVALID EMAIL")
	pass
	#authentication pending

@app.route('/letters/addletter/',methods=['Get','Post'])
def add_letter():
	if check_login() and session['alevel']<=2:
		f=request.files['imge']
		add_letter_to_database(request.form['mail'],request.form['lno'],request.form['subject'],f.read())
		return redirect('/letters/');
	else:
		return("<h1 >Access Denied ERROR 401</h1>")
		
	pass
	#authentication pending
def login_attempt(us,pwd):
	data=curs.execute("select * from user where uniq_id=%s" %(us))
	
	if data==1:
		data=curs.fetchone()
		suite=Fernet(b"%s" %str(data[3]))
		ep=suite.decrypt(b"%s" %str(data[2]))
		if ep == pwd :
			session['uid']=us
			session['alevel']=data[4]
			va,ty="",""
			d=curs.execute("select fname from student where eno =%s " ,(us,))
			if d==0:
				d=curs.execute("select fname from professor where profid =%s " ,(us,))
				if d==0:
					d=curs.execute("select fname from office_personnels where id =%s " ,(us,))
					if d==0:
						va="admin"+us.split("@")[0]
						ty="admin"
					else:
						va=curs.fetchone()[0]
						ty="office_personnels"
				else:
					va=curs.fetchone()[0]
					ty="professor"
			else:
				va=curs.fetchone()[0]
				ty="student"
			session['name']=va
			session['type']=ty
			session['addr']=request.remote_addr
			print ("Lgging in")
			return True
	return False
@app.route('/logout/',methods=["Get","Post"])
def logout():
	session.pop('name',None)
	session.pop('type',None)
	session.pop('addr',None)
	session.pop('alevel',None)
	session.pop('uid',None)
	flash("You have been successfully logged out.")
	return redirect('/')
def check_login():
	if ("uid" in session) and (session['addr']==request.remote_addr):
		return True
	return False
@app.route("/logint/",methods=["Get","Post"])
def loginnow():
	login_attempt(request.form['usid'],request.form['pwd'])
	return redirect("/")
if __name__=="__main__":
	attempt_creating_tables()
	app.run(debug=True)
