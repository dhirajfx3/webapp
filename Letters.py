from flask import *
from MySQLdb import connect
c=connect("localhost","root","dhirajfx3","facarts")
d=c.cursor()
letters = Blueprint('letters', __name__, template_folder='templates')
@letters.route('/letters/')
def letterf():
	if ("uid" in session) and session['addr']==request.remote_addr: 
		disc=dict()
		d.execute("select * from recieverlist;")
		x=d.fetchall()
		for i in x:
			print(i)
		return render_template("letters/index.html",**disc)
	else:
		return redirect("/")