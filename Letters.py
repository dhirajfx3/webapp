from flask import *
from MySQLdb import connect
c=connect("localhost","root","dhirajfx3","facarts")
d=c.cursor()
letters = Blueprint('letters', __name__, template_folder='templates')
@letters.route('/letters/',methods=['get','post'])
def letterf():
	if ("uid" in session) and session['addr']==request.remote_addr: 
		disc=dict()
		d.execute("select * from recieverlist order by idx;")
		x=d.fetchall()
		S=set()
		for i in x:
			S.add(i[0])
		Letter=[[], [], []] #pending on curr,pending on other ,completed or rej
		i,j,l=0,0,0
		
		for k in S:
			d.execute("select src,date_in,subject,status,holder from letter where lno = %s",(k,))
			gf=d.fetchone()
			if gf[3]=='pending':
				if str(gf[4])==str(session['uid']):
					Letter[0].append([])
					Letter[0][i].append(k)
					Letter[0][i].append(gf[0]) 
					Letter[0][i].append(gf[1]) 
					Letter[0][i].append(gf[2])
					Letter[0][i].append(gf[3])
					Letter[0][i].append([])
					Letter[0][i].append(True)
					disc[k]=(0,i)
					i+=1
				else:
					Letter[1].append([])
					Letter[1][j].append(k)
					Letter[1][j].append(gf[0]) 
					Letter[1][j].append(gf[1]) 
					Letter[1][j].append(gf[2])
					Letter[1][j].append(gf[3])
					Letter[1][j].append([])
					Letter[1][j].append(False)
					disc[k]=(1,j)
					j+=1
			else:
				Letter[2].append([])
				Letter[2][l].append(k)
				Letter[2][l].append(gf[0]) 
				Letter[2][l].append(gf[1]) 
				Letter[2][l].append(gf[2])
				Letter[2][l].append(gf[3])
				Letter[2][l].append([])
				Letter[2][l].append(False)
				disc[k]=(2,l)
				l+=1
		for jm in x:
			fnameR="NONE"
			fnameS="NONE"
			if jm[2]!=None:
				d.execute("select fname from office_personnels where id=%s",(jm[2],))
				fnameR=d.fetchone()[0]
			if jm[3]!=None:
				d.execute("select fname from office_personnels where id=%s",(jm[3],))
				fnameS=d.fetchone()[0]
			Letter[disc[jm[0]][0]][disc[jm[0]][1]][5].append([fnameS,jm[4],fnameR])
			
		data_pack = {'new':Letter[0],'pending':Letter[1],"other":Letter[2],'name':session['name'],'uid':session['uid']}
		return render_template("letters/index.html",**data_pack)
	else:
		return redirect("/")