from flask import *
library = Blueprint('library', __name__, template_folder='templates')
@library.route('/library/')
def home():
	#authentication pending
	return render_template("library/index.html")