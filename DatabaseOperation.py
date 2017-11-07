from MySQLdb import connect
from random import randint
from flask import session
from re import search
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
	
	qry="insert into letter values('%s',%s,curdate(),'%s','pending',%s" %(src,num,sub,session['uid']) + ",%s)"
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
def studify(Data):
	Data2=dict()
	for i in Data.keys():
		Data2[i]=str(Data[i]).strip("'")
	Data=Data2
	Keys=[]
	Pk=str(Data['selecteno'])
	print(Data['fname'])
	if Data['fname']=="-1":
		Keys.append("fname='"+str(Data['selectfname'])+"'")
	if Data['lname']=="-1":
		Keys.append("lname='"+str(Data['selectlname'])+"'")
	if Data['mothername']=="-1":
		Keys.append("mothername='"+str(Data['selectmothername'])+"'")
	if Data['fathername']=="-1":
		Keys.append("fathername='"+str(Data['selectfathername'])+"'")
	if Data['house']=="-1":
		Keys.append("house="+str(Data['selecthouse']))
	if Data['sector']=="-1":
		Keys.append("sector="+str(Data['selectsector']))
	if Data['state']=="-1":
		Keys.append("state='"+str(Data['selectstate'])+"'")
	if Data['city']=="-1":
		Keys.append("city='"+str(Data['selectcity'])+"'")
	if Data['zip']=="-1":
		Keys.append("zip="+str(Data['selectzip']))
	if Data['category']=="-1":
		Keys.append("category ='"+ str(Data['selectcategory'])+"'")
	if Data['religion']=="-1":
		Keys.append("religion='"+str(Data['selectreligion'])+"'")
	if Data['dob']=="-1":
		Keys.append("dob='"+str(Data['selectdob'])+"'")
	if Data['contactno']=="-1":
		Keys.append("contactno="+str(Data['selectcontactno']))
	if Data['email']=="-1":
		Keys.append("email='"+str(Data['selectemail'])+"'")
	if Data['programme']=="-1":
		Keys.append("programme='"+str(Data['selectprogramme'])+"'")
	if Data['admdate']=="-1":
		Keys.append("admdate='"+str(Data['selectadmdate'])+"'")
	if Data['class']=="-1":
		Keys.append("class='"+str(Data['selectclass'])+"'")
	s=",".join(Keys)
	Qry=[]
	if s.strip(''):
		print("update student set {0} where eno={1};".format(str(s),Pk))
		Qry.append(str("update student set {0} where eno={1};".format(str(s),Pk)))
		
	Courses=[]
	for i in Data.keys():
		if search("^cid.*",str(i)):
			#print(i)
			y=str(i)[3::]
			if y and Data[y]=="-1":
				Courses.append(str(i))
	for i in Courses:
		y=i[3::]
		if y and Data['butc'+y]=="1":
			Qry.append("delete from enrolledin where courseid={0} and stuid={1};".format(Data[i],Pk))
	for i in Courses:
		y=i[3::]
		if Data[i] and Data['butc'+y]=='0':
			if d.execute("select cid from course where cid={0};".format(Data[i])): 
				Qry.append("update course set name='{0}',type='{1}',duration={2},cprof={3} where cid={4};".format(Data['cname'+y],\
				Data['ctype'+y],Data['cduration'+y],Data['cmentorid'+y],Data[i]))
			else:
				Qry.append("insert into course values({0},'{1}','{2}',{3},{4})".format(Data[i],Data['cname'+y],\
				Data['ctype'+y],Data['cduration'+y],Data['cmentorid'+y]))
	for i in Courses:
		y=i[3::]
		if Data[i] and Data['butc'+y]=='0':
			if d.execute("select stuid from enrolledin where courseid={0} and stuid={1};".format(Data[i],Pk))==0:
				Qry.append("insert into enrolledin values({0},{1})".format(Pk,Data[i]))
	Degree=[]
	for i in Data.keys():
		if search("^name.*",str(i)):
			y=str(i)[4::]
			if y and Data[y]=="-1":
				Degree.append(str(i))
	for i in Degree:
		y=i[4::]
		if y and Data['butd'+y]=="1":
			Qry.append("delete from degree where stuid={0} and name='{1}';".format(Pk,Data[i]))
	for i in Degree:
		y=i[4::]
		if Data[i] and Data['butd'+y]=='0':
			TR=("select name from degree	where stuid={0} and name ='{1}';".format(Pk,Data[i]))
			if d.execute(TR): 
				Qry.append("update degree set cgpa={0},institute='{1}' year={2}\
				where stuid={3} and name='{4}';".format (\
				Data['cgpa'+y],Data['ins'+y],Data['yr'+y],str(Pk),str(Data['name'])))	
			else:
				Qry.append("insert into degree values('{0}',{1},{2},'{3}',{4});".format(Data['name'+y],\
				Pk,Data['cgpa'+y],Data['ins'+y],Data['yr'+y]))
	for Q in Qry:
		d.execute(Q)
	c.commit()
	pass
def profify(Data):
	Data2=dict()
	for i in Data.keys():
		Data2[i]=str(Data[i]).strip("'")
	Data=Data2
	Keys=[]
	Pk=str(Data['selectprofid'])
	print(Data['fname'])
	if Data['fname']=="-1":
		Keys.append("fname='"+str(Data['selectfname'])+"'")
	if Data['lname']=="-1":
		Keys.append("lname='"+str(Data['selectlname'])+"'")
	if Data['contactno']=="-1":
		Keys.append("contactno="+str(Data['selectcontactno']))
	if Data['email']=="-1":
		Keys.append("email='"+str(Data['selectemail'])+"'")
	if Data['class_p']=="-1":
		Keys.append("class_p='"+str(Data['selectclass_p'])+"'")

	s=",".join(Keys)
	Qry=[]
	if s.strip(''):
		Qry.append(str("update professor set {0} where profid={1};".format(s,Pk)))
	Courses=[]
	for i in Data.keys():
		if search("^cid.*",str(i)):
			#print(i)
			y=str(i)[3::]
			if y and Data[y]=="-1":
				Courses.append(str(i))
	for i in Courses:
		y=i[3::]
		if y and Data['butc'+y]=="1":
			Qry.append("delete from enrolledin where courseid={0}".format(Data[i]))
			Qry.append("delete from course where cid={0}".format(Data[i]))
	for i in Courses:
		y=i[3::]
		if Data[i] and Data['butc'+y]=='0':
			if d.execute("select cid from course where cid={0};".format(Data[i])): 
				Qry.append("update course set name='{0}',type='{1}',duration={2},cprof={3} where cid={4};".format(Data['cname'+y],\
				Data['ctype'+y],Data['cduration'+y],Data['cmentorid'+y],Data[i]))
			else:
				Qry.append("insert into course values({0},'{1}','{2}',{3},{4})".format(Data[i],Data['cname'+y],\
				Data['ctype'+y],Data['cduration'+y],Pk))

	for Q in Qry:
		print("Q:",Q),d.execute(Q);c.commit();
	c.commit()
def officify(Data):
	Data2=dict()
	for i in Data.keys():
		Data2[i]=str(Data[i]).strip("'")
	Data=Data2
	Keys=[]
	Pk=str(Data['selectid'])
	print(Data['fname'])
	if Data['fname']=="-1":
		Keys.append("fname='"+str(Data['selectfname'])+"'")
	if Data['lname']=="-1":
		Keys.append("lname='"+str(Data['selectlname'])+"'")
	if Data['contactno']=="-1":
		Keys.append("contactno="+str(Data['selectcontactno']))
	if Data['email']=="-1":
		Keys.append("email='"+str(Data['selectemail'])+"'")
	s=",".join(Keys)
	Qry=[]
	if s.strip(''):
		Qry.append(str("update office_personnels set {0} where id={1};".format(s,Pk)))
	for Q in Qry:
		print("Q:",Q),d.execute(Q);c.commit()
	pass