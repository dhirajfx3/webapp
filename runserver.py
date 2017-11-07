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

@app.route('/letters/addletter/',methods=['Get','Post'])
def add_letter():
	if check_login() and session['alevel']<=2:
		f=request.files['imge']
		add_letter_to_database(request.form['mail'],request.form['lno'],request.form['subject'],f.read())
		return redirect('/letters/');
	else:
		return("<h1 >Access Denied ERROR 401</h1>")
		
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

@app.route("/fwd/",methods=["Get","Post"])
def fwd():
	if check_login():
		
		R=request.form['usid']
		Lid=request.form['lid']
		S=session['uid']
		print(R,S,Lid)
		if fwd_attempt(S,R,Lid):
			return "<a href='localhost:5000/letters/'>Click to go back</a><br><h1>Letter forwarded</h1>"
	return "Some error occurred please try again later..."

def fwd_attempt(src,NEXT,id):
	print("A1")
	if curs.execute("select holder from letter where lno=%s;",(id,)) :
		print("A2")
		if src==str(curs.fetchone()[0]):
			print("A3")
			if curs.execute("select id from office_personnels where id=%s;",(NEXT,)):
				curs.execute("update letter set holder =%s where lno=%s;",(NEXT,id,))
				idx=curs.execute("select count(idx) from recieverlist where letno=%s;",(id,))
				idx=curs.fetchone()[0]+1
				print("A4")
				curs.execute("insert into recieverlist values(%s,%s,%s,%s,curdate(),'forwarded');",(id,NEXT,idx,src,))
				connector.commit()
				return True
	return False

@app.route("/complete/",methods=["Get","Post"])
def comp():
	if check_login():
		Lid=request.form['act']
		S=session['uid']
		if comp_attempt(S,Lid):
			return jsonify(msg="Letter completed")
		return jsonify(msg="Completion Success!!!")
	return jsonify(msg="INVALID REQUEST")

def comp_attempt(src,id):
	print(src,id)
	if curs.execute("select holder from letter where lno=%s",(id,)) :
		print("B1")
		if src==str(curs.fetchone()[0]):
			print("B2")
			curs.execute("update letter set holder =null,status='completed' where lno=%s",(id,))
			idx=curs.execute("select count(idx) from recieverlist where letno=%s",(id,))
			idx=curs.fetchone()[0]+1
			curs.execute("insert into recieverlist (letno,idx,recieverno,recdate,action) values(%s,%s,%s,curdate(),'completed');",(id,idx,src,))
			connector.commit()
			return True
	return False

@app.route("/reject/",methods=["Get","Post"])
def rej():
	if check_login():
		Lid=request.form['act']
		S=session['uid']
		if comp_attempt(S,Lid):
			return "<a href='localhost:5000/letters/'>Click to go back</a><br><h1>LetterRjected</h1>"
		return "Rejection Failed!!!"
def rej_attempt(src,id):
	if curs.execute("select holder from letter where lno=%s",(id,)) :
		print("Alpha1")
		if src==str(curs.fetchone()[0]):
			print("Alpha2")
			curs.execute("update letter set holder =null,status='rejected' where lno=%s;",(id,))
			idx=curs.execute("select count(idx) from recieverlist where letno=%s",(id,))
			idx=curs.fetchone()[0]+1
			curs.execute("insert into recieverlist (letno,idx,recieverno,recdate,action) values(%s,%s,%s,curdate(),'rejected');",(id,idx,src,))
			connector.commit()
			return True
	return False

@app.route("/profile/",methods=["get","post"])
def profile():
	if check_login():
		print(str(request.form['id']),str(session['uid']))
		if str(request.form['id'])==str(session['uid']):
			return get_profile_data(str(request.form['id']))
		if curs.execute('select access from user where uniq_id=%s;',(request.form['id'],)):
			if curs.fetchone()[0]<int(session['alevel']):
				return get_profile_data(str(request.form['id']))
		else:
			return "<h1> Record not found</h1>"
	return "<h1>Unauthorized access</h1>"

def get_profile_data(id):
	data=dict()
	data['name']=session['name']
	data['uid']=session['uid']
	data['Data']=[id]
	if curs.execute("select eno from student where eno=%s",(id,)):
		curs.fetchall()
		curs.execute("select eno,fname,lname,mothername,fathername,house,sector,state,city,zip,category,religion,dob,contactno,email from student where eno=%s;",(id,))
		tup=curs.fetchone()
		Degree=[]
		Enroll=[]
		Details=[\
				('Name',str(tup[1])+" "+str(tup[2])),\
				('Mother"s name',tup[3]),\
				('Father"s name',tup[4]),\
				('Address',str(tup[5])+', Sector-'+str(tup[6])+'<br>'+str(tup[7])+' '+str(tup[8])+'<br>'+str(tup[9])),\
				('Category',tup[10]),\
				('Religion',tup[11]),\
				('Date of birth',tup[12]),\
				('Contact number',tup[13]),\
				('E-mail id',tup[14])\
			   ]
		if curs.execute("select name,cgpa,institute,year from degree where stuid=%s",(id,)):
			dup=curs.fetchall()
			for x in dup:
				Details.append(("Degree(s)",str(x[0])+" CGPA : "+str(x[1])+", from "+str(x[2])+" in "+str(x[3])))
		if curs.execute("select courseid from enrolledin where stuid=%s",(id,)):
			dup=curs.fetchall()
			res=""
			for x in dup:
				curs.execute("select name from course where cid=%s",(x[0],))
				t=curs.fetchone()
				res=res+str(t[0])+", "
			res=res.strip(", ")
			Details.append(("Enrolled courses",res))
		data['Details']=Details
		
	elif curs.execute("select profid from professor where profid=%s",(id,)):
		curs.fetchall()
		curs.execute('select profid,fname,lname,email,phone from professor where profid=%s',(id,))
		tup=curs.fetchone()
		Details=[\
					('Name',str(tup[1])+' '+tup[2]),\
					('E-mail id',tup[3]),\
					('Contact number',tup[4]),\
				]
		if curs.execute("select name from course where cprof=%s",(id,)):
			tup=curs.fetchall()
			da=""
			for x in tup:
				da=da+str(x[0])
			Details.append(("Courses",da))
		data['Details']=Details
	elif curs.execute('select fname,lname,email,contactno from office_personnels where id=%s',(id,)):
		tup=curs.fetchone()
		Details=[\
				('Name',str(tup[0])+' '+str(tup[1])),\
				('E-mail id',tup[2]),\
				('Contact number',tup[3]),\
				]
		
		data['Details']=Details
	else:
		data['Details']=[('No information found for this record',"")]
	return  render_template("profile/profile.html",**data)

@app.route("/edit/<id>")
def update(id):
	if check_login() and session['alevel']==1:
		data=dict()
		var=0

		if curs.execute("select eno from student where eno=%s;",(id,)):
			#name type display name value
			data=get_sd(id,data)
			var=1
		elif curs.execute("select profid from professor where profid=%s",(id,)):
			data=get_prof(id,data)
			var=1
		elif curs.execute("select id from office_personnels where id=%s",(id,)):
			data=get_office(id,data)
			var=1
		data['name']=session['name']
		data['uid']=session['uid']
		data['id']=id
		if var:
			return render_template("student/edit.html",**data)
	return "<h1>Invalid access request</h1>"
def get_sd(id,data):
	curs.execute("select * from student where eno=%s",(id,))
	R=[]
	tup=curs.fetchone()
	curs.fetchall()
	R.append(("eno","number","Enrollment number",tup[0],"disabled"))
	R.append(("fname","text","First Name",tup[1],''))
	R.append(("lname","text","Last Name",tup[2],''))
	R.append(("mothername","text","Mother's name",tup[4],''))
	R.append(("fathername","text","Father's name",tup[5],''))
	R.append(("house","number","House number",tup[6],''))
	R.append(("sector","number","Sector",tup[7],''))
	R.append(("state","text","State",tup[8],''))
	R.append(("city","text","City",tup[9],''))
	R.append(("zip","number","Postal code",tup[10],''))
	R.append(("category","text","Category",tup[11],''))
	R.append(("religion","text","Religion",tup[12],''))
	R.append(("dob","date","Date of birth",tup[13],''))
	R.append(("contactno","number","Contact number",tup[14],''))
	R.append(("email","text","E-mail address",tup[15],''))
	data['Requirements']=R;

	data['type']='student'
	if curs.execute("select name,cgpa,institute,year from degree where stuid=%s",(id,)):
		dup=curs.fetchall()
		i=1
		Degree=[]
		for x in dup:
			y=x
			y.insert(0,i)
			i+=1
			Degree.append(y)
		data['Degree']=Degree;
	if curs.execute("select courseid from enrolledin where stuid=%s",(id,)):
		dup=curs.fetchall()
		res=[]
		for x in dup:
			curs.execute("select * from course where cid=%s",(x[0],))
			t=curs.fetchone()
			curs.execute("select fname,lname from professor where profid=%s",(x[4],))
			gt=" ".join(list(curs.fetchone()))
			res.append(list(t).append(gt))
		data['Courses']=res

	return data;
	
def get_prof(id,data):
	curs.execute("select * from professor where profid=%s",(id,));
	R=[]
	tup=curs.fetchone()
	curs.fetchall()
	R.append(("id","number","ID card number",tup[0],"disabled"))
	R.append(("fname","text","First Name",tup[1],''))
	R.append(("lname","text","Last Name",tup[2],''))
	R.append(("email","text","E-mail address",tup[3],''))
	R.append(("contactno","number","Contact number",tup[4],''))
	R.append(("class_p","text","Currently Teaching",tup[5],''))
	data['Requirements']=R;
	data['type']='professor'
	if curs.execute("select * from course where cprof=%s",(id,)):
		dup=curs.fetchall()
		res=[]
		curs.execute("select fname,lname from professor where profid=%s",(id,))
		gt=" ".join(list(curs.fetchone()))
		for x in dup:
			res.append(list(x).append(gt))
		data['Courses']=res;
	return data;

@app.route("/edit/update/",methods=["get","post"])
def set_Val():
	if check_login() and session['alevel']==1:
		
		if 'selectprofid' in request.form:
			profify(request.form)
		elif 'selectid' in request.form:
			officfy(request.form)
		elif 'selecteno' in request.form:
			studify(request.form)
	return "<h1>You have successfully edited details</h1>"
@app.route("/print/",methods=["get","post"])
def un():
	print(request.form.keys())
	return "ok"
def get_office(id,data):
	curs.execute("select * from office_personnels where id=%s",(id,));
	R=[]
	tup=curs.fetchone()
	curs.fetchall()
	R.append(("id","number","ID card number",tup[0],"disabled"))
	R.append(("fname","text","First Name",tup[1],''))
	R.append(("lname","text","Last Name",tup[2],''))
	R.append(("email","text","E-mail address",tup[3],''))
	R.append(("contactno","number","Contact number",tup[4],''))
	data['Requirements']=R;
	data['type']='Office Member'
	return data;
if __name__=="__main__":
	attempt_creating_tables()
	app.run(debug=True)
