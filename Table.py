from MySQLdb import connect

def attempt_creating_tables():

	c=connect("localhost","root","dhirajfx3","facarts")
	d=c.cursor()
	#d.execute("drop database facarts;")
	student(d)
	attendance(d)
	degree(d)
	
	library_card(d)
	book(d)
	borrowed(d)
	
	
	

	professor(d)
	course(d)

	timeTable(d)
	ofClass(d)	
	enrolledin(d)
	
	
	office_personnels(d)
	letter(d)
	reciever_list(d)
	
	system_users(d)
	c.commit()
	c.close()
	return True
	
def book(curr):
	curr.execute(r'''
				create table if not exists book
					(
						ano int primary key,
						dateofpurchase date,
						name varchar(100),
						author varchar(100),
						price float(7,2),
						booktype varchar(100),
						supplier varchar(100),
						publisher varchar(100),
						papertype varchar(30),
						pagescount int,
						libcard int,
						foreign key (libcard)
							references library(cardno)
							ON DELETE SET NULL
					);
	''')
	pass

def borrowed(curr):
	curr.execute(r'''
				create table if not exists borrowed
					(
						acno int,
						cno int,
						issue date,
						due date,
						foreign key (acno)
							references book(ano)
							ON DELETE CASCADE,
						foreign key (cno)
							references library(cardno)
							ON DELETE CASCADE,
						primary key(acno,cno)
						
					);
	''')
	pass

def library_card(curr):
	curr.execute(r'''
				create table if not exists library
					(
						cardno int primary key,
						expiry date,
						issue date,
						booksleft int,
						stuid int,
						foreign key (stuid)
							references student(eno)
							ON DELETE CASCADE
					);
	''')
	pass
	
def student(curr):
	curr.execute(r'''
				create table if not exists student
					(
						eno int primary key,
						fname varchar(100),
						lname varchar (100),
						croll int,
						mothername varchar(100),
						fathername varchar(100),
						house int,
						sector int,
						state varchar(100),
						city varchar(100),
						zip int,
						category varchar(30),
						religion varchar(30),
						dob date,
						contactno bigint,
						email varchar(100),
                        programme varchar(100),
                        admdate date,
						class varchar(100)
					);
	''')
	pass
	
def attendance(curr):
	curr.execute(r'''
				create table if not exists attendance
					(
						classdate date,classslot int,
						duration int,
						stuid int,
						classattended bit(1),
						foreign key (stuid)
							references student(eno)
							ON DELETE CASCADE,
						primary key (classdate,classslot,stuid)
					);
	''')
	pass
		
def degree(curr):
	curr.execute(r'''
				create table if not exists degree
					(
						name varchar(100),
						stuid int,
						cgpa float(3,2),
						institute varchar(100),
						year int,
						foreign key (stuid)
							references student(eno)
							ON DELETE CASCADE,
						primary key (name,stuid)
					);
	''')
	pass
	
def course(curr):
	curr.execute(r'''
				create table if not exists course
					(
						cid int primary key,
						name varchar(100),
						type varchar(100),
						duration int,
						cprof int, 
						foreign key (cprof)
							references professor(profid)
							ON DELETE SET NULL
					);
	''')
	pass
	
def enrolledin(curr):
	curr.execute(r'''
				create table if not exists enrolledin
					(
						stuid int,
						courseid int,
						foreign key (stuid)
							references student(eno),
						foreign key (courseid)
							references course(cid)
							ON DELETE CASCADE,
						primary key(stuid,courseid)
					);
	''')
	pass

def ofClass(curr):
	curr.execute(r'''
				create table if not exists ofclass
					(
						stuid int,
						cldate date,clslot int,
						duration int,
						class_ varchar(100),
						foreign key (stuid)
							references student(eno)
							ON DELETE CASCADE,
						foreign key (cldate,clslot,class_)
							references timetable(date_,slot,class_id)
							ON DELETE CASCADE,
						primary key(stuid,cldate,clslot)
					);
	''')
	pass
	
def timeTable(curr):
	curr.execute(r'''
				create table if not exists timetable
					(
						date_ date,slot int,
						class_id varchar(100),
						courseid int,
						foreign key(courseid)
							references course(cid)
							ON DELETE CASCADE,
						primary key(date_,slot,class_id)
					);
	''')
	pass
	
def professor(curr):
	curr.execute(r'''
				create table if not exists professor
					(
						profid int primary key,
						fname varchar(100),
						lname varchar(100),
						email varchar(100),
						phone bigint,
						class_p varchar(100)
					);
	''')
	pass
	
def letter(curr):
	curr.execute(r'''
				create table if not exists letter
					(
						src varchar(100),
						lno int primary key,
						date_in date,
						subject varchar(300),
						status varchar(30),
						holder int,
						image longblob,
						foreign key(holder)
							references office_personnels(id)
							ON DELETE SET NULL
					);
	''')
	pass
	
def reciever_list(curr):
	curr.execute(r'''
				create table if not exists recieverlist
					(
						letno int,
						idx int ,
						recieverno int,
						senderno int,
						recdate date,
						action varchar(100),
						foreign key(letno)
							references letter(lno)
							ON DELETE CASCADE,
						foreign key(recieverno)
							references office_personnels(id)
							ON DELETE SET NULL,
						foreign key (senderno)
							references office_personnels(id)
							ON DELETE SET NULL
					);
	''')
	pass

def office_personnels(curr):
	curr.execute(r'''
				create table if not exists office_personnels
					(
						id int primary key,
						fname varchar(100),
						lname varchar(100),
						email varchar(100),
						contactno bigint
					);
	''')
	pass
	
def system_users(curr):
	curr.execute(r'''
				create table if not exists user
					(
						uniq_id int primary key,
						username varchar(100),
						encpwd varchar(200),
						seckey varchar(200),
						access int
					);
	''')
	pass

