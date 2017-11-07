from flask import *
import sys
import os
import flask_sijax

from Home import *
from Admin import *
from Letters import *
from library import *
from Student import *

from Table import attempt_creating_tables
from cryptography.fernet import Fernet
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re
from MySQLdb import connect
from email.utils import parseaddr
from threading import Thread
from DatabaseOperation import *
from datetime import timedelta
import datetime
path = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')
app= Flask(__name__)
app.config['SIJAX_STATIC_PATH'] = path
app.config['SIJAX_JSON_URI'] = '/static/js/sijax/json2.js'
flask_sijax.Sijax(app)
app.register_blueprint(hp)
app.register_blueprint(apg)
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
			if add_to_database(id,email,f,e,fname,lname)==False:
				return jsonify("Some error occurred in inserting into database.\nPlease try again later.")
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
		
def login_attempt(us,pwd):
	data=curs.execute("select * from user where uniq_id={0}".format(us))
	
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
			print("va","ty",ty,va)
			session['name']=va
			session['type']=ty
			session['addr']=request.remote_addr
			
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
		
		if fwd_attempt(S,R,Lid):
			return "<a href='localhost:5000/letters/'>Click to go back</a><br><h1>Letter forwarded</h1>"
	return "Some error occurred please try again later..."

def fwd_attempt(src,NEXT,id):
	
	if curs.execute("select holder from letter where lno=%s;",(id,)) :
		if src==str(curs.fetchone()[0]):
			if curs.execute("select id from office_personnels where id=%s;",(NEXT,)):
				curs.execute("update letter set holder =%s where lno=%s;",(NEXT,id,))
				idx=curs.execute("select count(idx) from recieverlist where letno=%s;",(id,))
				idx=curs.fetchone()[0]+1
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
	if curs.execute("select holder from letter where lno=%s",(id,)) :
		if src==str(curs.fetchone()[0]):
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
		if src==str(curs.fetchone()[0]):
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
		return get_profile_data(str(session['uid']))
	return "<h1>Unauthorized access</h1>"
@app.route("/settings/")
def settin():
	if check_login():
		return render_template("/settings/settings.html",name=session['name'])
	return "<h1>Unauthorized access</h1>"


def get_profile_data(id):
	data=dict()
	data['name']=session['name']
	data['uid']=session['uid']
	data['Data']=[id]
	if curs.execute("select eno from student where eno=%s",(id,)):
		curs.fetchall()
		curs.execute("select eno,fname,lname,mothername,fathername,house,\
		sector,state,city,zip,category,religion,dob,contactno,email,programme,\
		admdate,class from student where eno=%s;",(id,))
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
				('E-mail id',tup[14]),\
				('Programme ',tup[15]),\
				('Admission date ',tup[16])\
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
	elif curs.execute('select fname,lname,email,contactno\
		 from office_personnels where id=%s',(id,)):
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
	R.append(("programme","text","Programme",tup[16],''))
	R.append(("admdate","date","Admission date",tup[17],''))
	R.append(("class","text","Class",tup[18],''))
	data['Requirements']=R;

	data['type']='student'
	if curs.execute("select name,cgpa,institute,year from degree where stuid=%s",(id,)):
		dup=curs.fetchall()
		i=1;print("your def",dup);
		Degree=[]
		for x in dup:
			y=list(x)
			y.insert(0,i)
			i+=1
			Degree.append(y)
		data['Degree']=Degree;
	if curs.execute("select courseid from enrolledin where stuid=%s",(id,)):
		dup=curs.fetchall()
		res=[]
		for x in dup:
			if curs.execute("select * from course where cid=%s",(x[0],)):
				t=curs.fetchone()
				curs.execute("select fname,lname from professor where profid=%s",(t[4],))
				gt=" ".join([str(X) for X in list(curs.fetchone())]);t=list(t);t.append(gt)
				res.append(t);
		data['Course']=res
		print("res :",res)

	return data;
	
def get_prof(id,data):
	curs.execute("select * from professor where profid=%s",(id,));
	R=[]
	tup=curs.fetchone()
	curs.fetchall()
	R.append(("profid","number","ID card number",tup[0],"disabled"))
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
		gt=" ".join([str(x) for x in list(curs.fetchone())])
		for x in dup:
			t=list(x);t.append(gt);res.append(t);
		data['Course']=res;
	return data;

@app.route("/edit/update/",methods=["get","post"])
def set_Val():
	if check_login() and session['alevel']==1:
		
		if 'selectprofid' in request.form:
			profify(request.form)
		elif 'selectid' in request.form:
			officify(request.form)
		elif 'selecteno' in request.form:
			studify(request.form)
	return "<h1>You have successfully edited details</h1>"

@app.route("/student/")
def studpg():
	print('Access level :',session['alevel'])
	if check_login() and session['alevel']<=3:
		return render_template("/student/index.html",name=session['name'],uid=session['uid'],Rec=[])
	return "<h1>You are not authorized to view this page</h1>"
@app.route("/pwdchange/",methods=["get","post"])
def pchange():
	if check_login():
		try:
			a=str(request.form['cp'])
			b=str(request.form['p2'])
			c=str(request.form['p1'])
			if b!=c or len(b)<8:
				return "<h1>Do not interfere with developer's work!!!";
			id=session['uid']
			curs.execute("select encpwd,seckey from user where uniq_id=%s",(id,))
			D=curs.fetchone();F=Fernet(b"{0}".format(D[1]));p=F.decrypt(b"{0}".format(D[0]));
			if str(p)==a:
				F2=F.encrypt(b"{0}".format(b));Q=str("update user set encpwd ='{0}' where uniq_id={1};".format(F2,id))
				print(Q);curs.execute(Q);connector.commit()
				return "<h1>Your password changed</h1>"
			return "<h1> Please enter you correct password to change to new one</h1>"
		except:
			return "<h1>Some error occured try again later</h1>"

@app.route('/student/search/',methods=["get","post"])
def search():
	if check_login() and session['alevel']<=3:
		filter=str(request.form['filterby'])
		filter_value=str(request.form['filtervalue']);print("FIL:",filter,filter_value)
		rc=0;
		if filter=='cid':
			rc=curs.execute("select stuid from enrolledin where courseid={0};".format(filter_value))
		elif filter =='fname' or filter=='programme':
			rc=curs.execute("select eno from student where {0}='{1}';".format(filter,filter_value))
		else:
			Qry="select eno from student where %s=%s;"%(filter,filter_value);
			rc=curs.execute(Qry)
		Data=dict()
		L=[];print("RC :",rc)
		if rc:
			data=curs.fetchall();print("Your data",data,"Not data :",filter,filter_value);
			for i in data:
				if curs.execute("select eno,fname,lname,programme,admdate from student where eno=%s",(i[0],)):
					Z=list(curs.fetchone());L.append([Z[0],Z[1]+" "+Z[2],Z[3],Z[4]])
		Data['Rec']=L;
		Data['name']=session['name']
		Data['uid']=session['uid']
		return render_template("/student/index.html",**Data)
	return "<h1>Invalid access request</h1>"
@app.route("/request/",methods=["get","post"])
def load():
	id=request.form['eno']
	if check_login():
		if session['alevel']==1:
			return redirect("/edit/"+str(id))
		elif session['alevel']<=3:
			data=dict()
			var=0

			if curs.execute("select eno from student where eno=%s;",(id,)):
				#name type display name value
				data=get_sd(id,data)
				var=1
			data['name']=session['name']
			data['uid']=session['uid']
			data['id']=id
			if var:
				return render_template("/student/readonly.html",**data)
	return "<h1>Invalid access request</h1>"

@app.route("/book/search/",methods=["get","post"])
def srch_book2():
	if check_login() and session['alevel']<=4:
		data=dict();print("signed in")
		data['uid']=session['uid']
		data['name']=session['name']
		data['search']="1"
		type=request.form['filterby']
		fv=request.form['filtervalue']
		type=str(type)
		Direct1=("ano")
		D={"cno":"Card number "+fv,"due":"due date expired","ano":"Accession number"+fv,\
		"name":"Book name "+fv,"author":"author name "+fv,"avail":"available","borrowed":"borrowed books"}
		v=0
		data['typo']=D[type]
		if type in Direct1:
			v=curs.execute("select ano,name,author,publisher,libcard\
			from book where {0}={1};".format(type,fv))
		elif type=="cno":
			v=curs.execute("select b.ano,b.name,b.author,b.publisher,b.libcard from book b,borrowed r where b.ano=r.acno and r.cno={0}".format(fv))
		elif type in ["name","author"]:
			v=curs.execute("select ano,name,author,publisher,libcard\
			from book where {0}='{1}';".format(type,fv))
		elif type=="due":
			v=curs.execute("select b.ano,b.name,b.author,b.publisher,b.libcard\
			from book as b,borrowed as r where b.ano=r.acno and r.due > curdate();")
			v=curs.fetchall()
		elif type=='avail':
			v=curs.execute("select ano,name,author,publisher,libcard\
			from book where libcard is  NULL;")
		elif type=="borrowed":
			v=curs.execute("select ano,name,author,publisher,libcard\
			from book where libcard is NOT NULL;")
		da=list(curs.fetchall())
		
		for i in range(len(da)):
			print(da[i])
			x=list(da[i])
			if da[i][4]==None:
				x.insert(0,"Not Borrowed")
			else:
				x.insert(0,"Borrowed")
			da[i]=x
		data['res']=da
		buttons=[]
		if session['alevel']<=2:
			buttons=[("Issue a book","libraryissue"),\
					("Return a book","libraryreturn"),\
					("Add a book","libraryedit/a"),\
					("Issue a library card","librarycard")]
		data['buttons']=buttons
		return render_template("/library/index.html",**data)
	
	return "<h1>You are not signed in</h1>"
@app.route("/timetable/search/",methods=["get","post"])
def srch_book():
	if check_login() and session['alevel']<=4:
		data=dict();print("signed in")
		data['uid']=session['uid']
		data['name']=session['name']
		data['search']="1"
		type=request.form['filterby']
		fv=request.form['filtervalue2']
		fv2=request.form['filtervalue1']
		type=str(type)
		D={"stu":"student with id "+fv + " for date " + fv2,"fac":"professor with id "+fv + " for date " + fv2,"cls":"Class  "+fv + " for date " + fv2}
		v=0
		Q=""
		data['typo']=D[type]
		if type =="stu":
			Q="select slot,courseid from ofclass c,timetable t where \
c.clslot=t.slot and c.cldate=t.date_ and c.class_=t.class_id \
and c.stuid={0} and t.date_='{1}'" 
		elif type=="fac":
			Q="select slot,courseid from professor p ,timetable t where \
class_p=class_id and date_='{1}' profid={0}"
		elif type=="cls":
			Q="select slot,courseid from timetable t where\
 t.class_id = '{0}' \
 and t.date_='{1}'"
		print(Q)
		d1=datetime.datetime.strptime(fv2, "%Y-%m-%d")
		data['buttons']=[]
		res=[["-" for j in range(8)] for i in range(10)]
		res[0][0]="Time Slot"
		for i in range(7):
			res[0][i+1]=str(d1.date())
			d1=d1+timedelta(days=1)
		d1=datetime.datetime.strptime("08:00", "%H:%M")
	
		for i in range(9):
			res[i+1][0]=str(d1.time())
			d1=d1+timedelta(hours=1)
			res[i+1][0]+=" to "+str(d1.time())
		d1=datetime.datetime.strptime(fv2,"%Y-%m-%d")
	
		for j in range(7):
			print("Q:",Q.format(fv,str(d1.date())))
			curs.execute(Q.format(fv,str(d1.date())))
			Z=[0 for i in range(9)]
			d=list(curs.fetchall())
			print(d)
			for i in d:
				curs.execute("select name,cid,fname from course c,professor p\
			    where c.cprof=p.profid and\
			    cid={0}".format(i[1]))
				res[i[0]+1][j+1]=" - ".join([str(x) for x in list(curs.fetchone())])
			d1=d1+timedelta(days=1)

		data['res']=res
		buttons=[("See attendance","showattendance")]
		if session['alevel']<=3:
			buttons.append(("Edit time table","timetabledit"))
		if session['alevel']==3:
			buttons.append(("Mark attendance","markattendance"))
		data['buttons']=buttons
		data['search']="1"
		return render_template("/timetable/index.html",**data)
	return "<h1>You are not signed in</h1>"
@app.route("/timetabledit/")
def ttedit():
	if check_login() and session['alevel']<=3:
		data=dict()
		data['search']="0"
		data['name']=session['name']
		buttons=[("See attendance","showattendance")]
		if session['alevel']==3:
			buttons.append(("Mark attendance","markattendance"))
		data['buttons']=buttons
		id=session['uid']
		if session['alevel']==3:
			curs.execute("select class_p from professor where profid={0}".format(id));
		data['classname']=curs.fetchone()[0]
		curs.execute("select name from course where cprof={0}".format(id))
		data['coursename']=curs.fetchone()[0]
		return render_template("/timetable/edit.html",**data)
	return "<h1>Unauthorized access</h1>"
@app.route("/timetableupdate/",methods=["get","post"])
def ttupdate():
	if check_login() and session['alevel']<=3:
		data=request.form
		pid=session['uid']
		dte=data['date_']
		slot=data['slot']
		if curs.execute("select class_p from professor where profid={0}".format(pid)):
			X=curs.fetchone()[0]
			Y=curs.execute("select cid from course where cprof={0}".format(pid))
			Y=curs.fetchone()[0]
			curs.execute("insert into timetable values ('{0}',{1},'{2}',{3})".\
				format(dte,slot,X,Y));
			print("insert into ofclass select eno,'{0}',{1},\
			1,'{2}'from student where class='{2}';".format(dte,slot,X))
			curs.execute("insert into ofclass select eno,'{0}',{1},\
			1,'{2}' from student where class='{2}';".format(dte,slot,X));connector.commit();
		return "<h1>Update successful</h1>"
	return "<h1>Unauthorized Access</h1>"
@app.route("/markattendanc/",methods=["get","post"])
def mark_attendance():
	if check_login() and session['alevel']==3:
		data=request.form;
		slot=data['slot']
		date_=data['date_']
		curs.execute("select class_p from professor where profid={0}".format(session['uid']))
		class_=curs.fetchone()[0]
		y=lambda a:0 if a==-1 else 1;
		for i in data.keys():
			if i[0:5]=="stuid":
				curs.execute("insert into attendance values('{0}','{1}',1,{2},{3})".\
					format(date_,slot,i[5::],y(int(data[i]))))
		connector.commit();
		return "<h1>Attendance marked successfully</h1>"
	return "<h1> Unauthorized access</h1>"
@app.route("/showattendance/")
def check_attendance():
	if check_login() and session['alevel']<=4:
		class_p=""
		data=dict()
		id=session['uid']
		if session['alevel']==3:
			curs.execute("select class_p from professor where profid={0}".format(id));
		elif session['alevel']==4:
			curs.execute("select class from student where eno={0}".format(id))
		class_p=curs.fetchone()[0]
		curs.execute("select eno from student where class='{0}'".format(class_p))
		tsy=curs.fetchall()
		st=set()
		for i in tsy:
			st.add(i[0])
		L=[]
		print(str(st))
		for i in st:
			L.append(i)
		st=", ".join([str(x) for x  in L])
		curs.execute("select stuid,count(stuid),croll,fname from attendance, student\
		 where  stuid=eno and classattended=0 and stuid in ({0}) group by stuid".format(st)); 
		Absents=curs.fetchall()
		curs.execute("select stuid,count(stuid),croll,fname from attendance, student\
		 where  stuid=eno and classattended=1 and stuid in ({0}) group by stuid".format(st)); 
		Presents=curs.fetchall()
		initial=dict()
		final=dict()
		s=set()
		res=[]
		print("Presents:",Presents)
		print("Absents:",Absents)
		for a in Absents:
			initial[a[0]]=(a[1],a[2],a[3])#count id fname
			s.add(a[0])
		for b in Presents:
			final[b[0]]=(b[1],b[2],b[3])
			s.add(b[0])
		for x in s:
			a,p=0,0
			y=0
			z=""
			if x in initial:
				a=initial[x][0]
				y=initial[x][1]
				z=str(initial[x][2])
			if x in final:
				p=final[x][0]
				y=final[x][1]
				z=final[x][2]
			z2=lambda x,y:(x*100)/(x+y) if x+y >0 else 0
			res.append((y,x,z,a,p,z2(int(p),int(a))))
		res.sort()
		print(res)
		data['res']=res
		data['action']='show'
		data['name']=session['name']
		buttons=[("See attendance","showattendance")]
		if session['alevel']<=3:
			buttons.append(("Edit time table","timetabledit"))
		if session['alevel']==3:
			buttons.append(("Mark attendance","markattendance"))
		data['buttons']=buttons
		return render_template('/timetable/markattendance.html',**data)
	return "<h1>Unauthorized access</h1>"
@app.route("/markattendance/")
def matt():
	if check_login() and session['alevel']==3:
		data=dict()
		data['name']=session['name']
		data['res']=[]
		id=session['uid']
		curs.execute("select class_p from professor where profid={0}".\
			format(id))
		class_p=curs.fetchone()[0]
		stud=[]
		curs.execute("select name from course where cprof={0}".format(id))
		data['coursename']=curs.fetchone()[0]
		data['classname']=class_p
		print(class_p)
		curs.execute("select croll,eno,fname from student s\
		where class='{0}' order by croll;".format(class_p))
		y=curs.fetchall()
		for i in y:
			stud.append(list(i))
		print(stud)
		data['res']=stud;
		data['action']='markattendance'

		buttons=[("See attendance","showattendance")]
		if session['alevel']<=3:
			buttons.append(("Edit time table","timetabledit"))
		if session['alevel']==3:
			buttons.append(("Mark attendance","markattendance"))
		data['buttons']=buttons
		return render_template("/timetable/markattendance.html/",**data)
@app.route("/timetable/")
def timt():
	if check_login() and session['alevel']<=4:
		data=dict();
		data['name']=session['name']
		data['search']='0'
		data['res']=[]
		buttons=[("See attendance","showattendance")]
		if session['alevel']<=3:
			buttons.append(("Edit time table","timetabledit"))
		if session['alevel']==3:
			buttons.append(("Mark attendance","markattendance"))
		data['buttons']=buttons
		return render_template("/timetable/index.html",**data)
	return "<h1>Unauthorized access </h1>"
@app.route("/library/")
def libr_home():
	if check_login():
		data=dict()
		data['uid']=session['uid']
		data['name']=session['name']
		data['search']=0
		data['res']=[]
		buttons=[]
		if session['alevel']<=2:
			buttons=[("Issue a book","libraryissue"),\
					("Return a book","libraryreturn"),\
					("Add a book","libraryedit/a"),\
					("Issue a library card","librarycard")]
		data['buttons']=buttons
		return render_template("/library/index.html",**data)
	
	return "<h1>You are not signed in</h1>"
@app.route("/libraryedit/<book>/")
def libform(book=None):
	if check_login() and session['alevel']<=2:
		R=[];data=dict()
		tup=["" for i in range(11)]
		if str(book):
			if curs.execute("select * from book where ano=%s",(book,)):
				tup=curs.fetchone()
		R.append(("ano","number","Acession number",tup[0],"required"))
		R.append(("dateofpurchase","date","Date of purchase",tup[1],'required'))
		R.append(("name","text","Book name",tup[2],'required'))
		R.append(("author","text","Author's name",tup[3],'required'))
		R.append(("price","number","Price",tup[4],'required step=0.01'))
		R.append(("booktype","text","Book type",tup[5],'required'))
		R.append(("supplier","text","Supplier",tup[6],'required'))
		R.append(("publisher","text","Publisher",tup[7],'required'))
		R.append(("papertype","text","Paper Type",tup[8],'required'))
		R.append(("pagescount","number","Number of pages",tup[9],'required'))
		R.append(("libcard","number","Borrower's card number (if any)",tup[10],'disabled'))
		data['Requirements']=R;
		data['name']=session['name']
		data['uid']=session['uid']
		data['target']="bookinfo"
		data['type']="Office member"
		return render_template("/library/operation.html",**data)
	return "<h1>Unauthorized user</h1>"
@app.route("/return/",methods=["get","post"])
def retbook():
	if check_login() and session['alevel']<=2:
		Data=request.form
		cn=str(Data['selectcardno'])
		bn=str(Data['selectano'])
		if curs.execute("select acno,cno from borrowed where acno=%s and cno=%s",(bn,cn,)):
			curs.execute("delete from borrowed where acno=%s and cno=%s",(bn,cn,))
			curs.execute("update library set booksleft=booksleft+1 where cardno=%s",(cn,))
			curs.execute("update book set libcard=NULL where ano=%s",(bn,))
			connector.commit()
			return "<h1>Book successfully returned</h1>"
		return "<h1>Inconsistent data provided</h1>"
	return "<h1>Unauthorized access</h1>"
@app.route("/card/",methods=["get","post"])
def librcard():
	if check_login() and session['alevel']<=2:
		try:
			Data=request.form
			D=[Data['selectcardno'],Data['selectexpiry'],"curdate()",Data["selectbooksleft"]\
			,Data["selectstuid"]]
			for i in range(len(D)):
				if not str(D[i]):
					D[i]='NULL'
				else:
					D[i]=str(D[i])
			print("IT IS D",D)
			curs.execute("insert into library values({0},'{1}',{2},{3},{4})".format(D[0],D[1],D[2],D[3],D[4]))
			connector.commit()
			return "<h1>Card Successfully issued</h1>"
		except:
			return "<h1>Inconsistent data provided</h1>"
	return "<h1>Unauthorized access</h1>"
@app.route("/issue/",methods=["get","post"])
def libisue():
	if check_login() and session['alevel']<=2:
		try:
			Data=request.form
			D=[Data['selectano'],Data['selectcardno'],"curdate()",Data["selectdue"]]
			for i in range(len(D)):
				if not str(D[i]):
					D[i]='NULL'
				else:
					D[i]=str(D[i]);print("I am here")
			if (not curs.execute("select booksleft from library where cardno=%s",(D[1],))) or curs.fetchone()[0]==0:
				return "<h1>No more books can be issued for this student</h1>"
			curs.execute("insert into borrowed values({0},{1},{2},'{3}')".format(D[0],D[1],D[2],D[3]))
			curs.execute("update library set booksleft=booksleft-1 where cardno=%s",(D[1],))
			curs.execute("update book set libcard=%s where ano=%s",(D[1],D[0],))
			connector.commit()
			return "<h1>Book Successfully issued</h1>"
		except:
			return "<h1>Inconsistent data provided</h1>"
	return "<h1>Unauthorized access</h1>"
@app.route("/bookinfo/",methods=["get","post"])
def bookinfo():
	if check_login() and session['alevel']<=2:
		
		Data=request.form;
		D=[\
			Data['selectano'],\
			Data['selectdateofpurchase'],\
			Data['selectname'],\
			Data['selectauthor'],\
			Data['selectprice'],\
			Data['selectbooktype'],\
			Data['selectsupplier'],\
			Data['selectpublisher'],\
			Data['selectpapertype'],\
			Data['selectpagescount']];print("Here")
		for i in range(len(D)):
			D[i]=str(D[i])
		if curs.execute("select ano from book where ano=%s",(D[0],)):
			D=list(D);D.append(D[0]);curs.execute("update book set\
			ano=%s,\
			dateofpurchase=%s,\
			name=%s,\
			author=%s,\
			price=%s,\
			booktype=%s,\
			supplier=%s,\
			publisher=%s,\
			papertype=%s,\
			pagescount=%s where ano=%s)",D);connector.commit()
			return "<h1>Successfully updated book details</h1>"
		else:
			D2=D
			curs.execute("insert into book values \
			(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NULL)",D2);connector.commit()
			return "<h1>Successfully add a new book</h1>"
			return "<h1> Incosistent Data Provided</h1>"
		
			return "<h1> Some error occured kindly try after a few moments<h1>"
	return "<h1>Unauthorized access </h1>"
@app.route("/libraryissue/")
def libissue():
	if check_login() and session['alevel']<=2:
		R=[];data=dict()
		R.append(("ano","number","Acession number","","required"))
		R.append(("cardno","number","Card number","","required"))
		R.append(("due","date","Due date","","required"))
		data['Requirements']=R;
		data['name']=session['name']
		data['uid']=session['uid']
		data['target']="issue"
		data['type']="Office member"
		return render_template("/library/operation.html",**data)
	return "<h1>Unauthorized access</h1>"

@app.route("/libraryreturn/")
def libret():
	if check_login() and session['alevel']<=2:
		R=[];R.append(("ano","number","Acession number","","required"))
		R.append(("cardno","number","Card number","","required"))
		data=dict();data['Requirements']=R;
		data['name']=session['name']
		data['uid']=session['uid']
		data['target']="return"
		data['type']="Office member"
		return render_template("/library/operation.html/",**data)
	return "<h1>Unauthorized access</h1>"

@app.route("/librarycard/")
def libcard():
	if check_login() and session['alevel']<=2:
		R=[]
		R.append(("cardno","number","Card number","","required"))
		R.append(("expiry","date","Expiry date","",'required'))
		R.append(("booksleft","number","Books allowed on this card","",'required'))
		R.append(("stuid","number","Student Roll number","",'required'))
		data=dict();data['Requirements']=R;
		data['name']=session['name']
		data['uid']=session['uid']
		data['target']="card"
		data['type']="Office Member"
		return render_template("/library/operation.html/",**data)
	return "<h1>Unauthorized access</h1>"
@app.route("/viewletter/",methods=["get","post"])
def let_view():
	if check_login() and session['alevel']<=2:
		if curs.execute("select lno from letter where lno={0}".format(request.form['letterView'])):
			curs.execute("select image from letter where lno={0}".format(request.form['letterView']))
			imag3=curs.fetchone()[0]
			response = make_response(imag3)
			response.headers['Content-Type'] = 'image/jpeg'
			response.headers['Content-Disposition'] = 'attachment; filename={0}.jpg'.format(request.form['letterView'])
			return response
		return "<h1>Letter not found</h1>"
	return "<h1> Unauthorized access</h1>"
	pass
@app.route("/print/",methods=["get","post"])
def un():
	print(request.form.keys())
	return "ok"
def get_office(id,data):
	curs.execute("select * from office_personnels where id=%s",(id,));
	R=[];
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
