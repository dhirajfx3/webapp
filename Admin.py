from flask import *
apg = Blueprint('apg', __name__, template_folder='templates')
@apg.route('/admin/')
def admin_site():
	if ("uid" in session.keys()) and session['addr']==request.remote_addr and session['alevel']==1:
		return render_template("admin/index.html",name=session['name'])
	return redirect("/")
#sans-serif