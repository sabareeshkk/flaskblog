from flask import Flask,render_template,redirect,url_for,request,session,flash,g,send_from_directory
from functools import wraps
import sqlite3
import os

app = Flask(__name__)

app.secret_key ='sabareeshk'
#app.database ="sample.db"
@app.before_request
def before_request():
    g.db = sqlite3.connect("sample.db")

def login_required(f):
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'logged_in' in session:
			return f(*args,**kwargs)
		else:
			flash('you need to login first.')
			return redirect(url_for('login'))
	return wrap


@app.route('/',methods=['GET','POST'])
@login_required
def home():
	#g.db = connect_db()
	cur = g.db.execute('select *from posts')
	posts = [dict(title=row[0],description=row[1]) for row in cur.fetchall()]
	print posts
	#if request.method == 'POST':
		#g.db.execute('INSERT INTO comments VALUES(?)',[request.form['']])
		#g.db.commit()
	#g.db.close()
	return render_template('index.html',posts=posts)


@app.route('/favicon.ico')
def favicon():
	 return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/blog',methods=['GET','POST'])
@login_required
def blog():
	if request.method == 'POST':
		#head=request.form['head']
		#text=request.form['text']
		g.db.execute('INSERT INTO posts VALUES(?,?)',[request.form['head'],request.form['text']])
		g.db.commit()
		return redirect(url_for('home'))
	return render_template('layout.html')

@app.route('/welcome')
@login_required
def welcome():
	return render_template("welcome.html")

@app.route('/login',methods=['GET','POST'])
def login():
	error=None
	if request.method =='POST':
		if request.form['username'] != 'admin' or request.form['password'] != 'admin':
			error ='invalid password or user name please try again'
		else:
			session['logged_in'] = True
			flash('your just logged in!')
			return redirect(url_for('blog'))
	return render_template('login.html',error=error)

@app.route('/logout')
@login_required
def logout():
		session.pop('logged_in',None)
		flash('your just logged out!')
		return redirect(url_for('welcome'))

#def connect_db():
	#return sqlite3.connect(app.database)

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

if __name__ == '__main__':
	app.run(debug=True)
