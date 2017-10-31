from flask import *
timetable = Blueprint('timetable', __name__, template_folder='templates')
@timetable.route('/timetable/')
def home():
	#authentication pending
	return render_template("timetable/index.html")