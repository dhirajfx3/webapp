from flask import *
hp = Blueprint('hp', __name__, template_folder='templates')
@hp.route('/')
def home():
	if "uid" in session:
		if session["addr"]==request.remote_addr:
			print(session['name'])
			return render_template("home/loggedIN.html",name=session['name'])
	return render_template("home/index.html")