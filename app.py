from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort


import os

app = Flask(__name__)

credentials = {'admin': 'password'}


def generate_cat_art(words):
	return """
      ,_     _,
      |\\\\___//|
      |=6   6=|		-({}) 
      \=._Y_.=/
       )  `  (    ,
      /       \  ((
      |       |   ))
     /| |   | |\_//
jgs  \| |._.| |/-`
      :.:   :.:
""".format(words)

@app.route('/')
def home():
	if 'cat_art' not in session:
		session['cat_art'] = generate_cat_art("meow!")
	return render_template('cat.html', cat_art=session['cat_art'])

@app.route('/login', methods=['GET', 'POST'])
def do_admin_login():
	if request.method == 'POST':

		if request.form['username'] in credentials and credentials[request.form['username']] == request.form['password']:
			session['logged_in'] = True
			session['username'] = request.form['username']
		else:
			flash('wrong password!')
		return home()
	else:
		return render_template('login.html')

@app.route('/cat', methods=['GET', 'POST'])
def cat():
	if request.method == 'POST':
		try:
			session['cat_art'] = generate_cat_art(request.form['input'].lower())
		except:
			session['cat_art'] = generate_cat_art("Uh Oh!")

	return home()

@app.route("/logout")
def logout():
	session['logged_in'] = False
	return home()

if __name__ == "__main__":
	app.secret_key = os.urandom(12)
	app.run(debug=True,host='0.0.0.0', port=4000)