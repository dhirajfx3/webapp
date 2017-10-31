from flask import *
student = Blueprint('student', __name__, template_folder='templates')
@student.route('/student/')
def home():
	#authentication pending
	return render_template("student/index.html")