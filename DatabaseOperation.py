from MySQLdb import connect
from random import randint
from flask import session
from cryptography.fernet import Fernet
c=connect("localhost","root","dhirajfx3","facarts")
d=c.cursor()
def add_to_database(id,email,pwd,al,fname,lname):
	try:
		
		key=Fernet.generate_key()
		suite=Fernet(key)
		s1=suite.encrypt(b"{0}".format(pwd))
		al=int(al)
		d.execute("insert into user values({0},'{1}','{2}','{3}',{4})".format(id,email,s1,key,al))
		
		if al==1:
			#admin level 2
			pass;
		elif al==2:
			#office
			d.execute("insert into office_personnels (id,fname,lname,email) values({0},'{1}','{2}','{3}')".format(id,fname,lname,email));
			pass
		elif al==3:
			#faculty
			d.execute("insert into professor (profid,fname,lname,email) values({0},'{1}','{2}','{3}')".format(id,fname,lname,email));
			pass
		elif al==4:
			#student
			d.execute("insert into student (eno,fname,lname,email) values({0},'{1}','{2}','{3}')".format(id,fname,lname,email));
			pass
		c.commit()
		
		return True
	except:
		return False
	
def add_letter_to_database(src,num,sub,content):
	
	qry="insert into letter values('%s',%s,curdate(),'%s','pending'" %(src,num,sub) + ",%s)"
	c.commit()
	d.execute(qry,(content,))
	qry="insert into recieverlist values(%s,1,%s,%s,curdate(),'pending')" %(num,session['uid'],session['uid'])
	d.execute(qry)
	c.commit()
	
def getImage(pid):
	g=d.execute("select image from letter where lno = %s",(pid,)).fetchone()[0]
	response = make_response(g)
	response.headers['Content-Type'] = 'image/jpeg'
	response.headers['Content-Disposition'] = 'attachment; filename=%s.jpg' %pid
	return response
def alphaNum(L,fixed=True):
	sz=randint(1,L)
	if fixed==True:
		sz=L
	Result=""
	for i in range(sz):
		R=randint(0,125)
		if R<100:
			Result+=str(R//10)
		else:
			Result+=chr(ord('A')+R-100)
	return Result