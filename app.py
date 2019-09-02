from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort


import json
import os

app = Flask(__name__)

global g_credentials
g_credentials = {}

def load_credentials(file_path):
	try:
		with open(file_path, "r") as f:
			credentials = json.load(f)
			return credentials
	except Exception as e:
		raise e

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

def reset_session():
	session['cat_art'] = generate_cat_art("meow!")
	session['credentials'] = load_credentials("default.json")

@app.route('/')
def home():
	if 'cat_art' not in session:
		session['cat_art'] = generate_cat_art("meow!")

	return render_template('cat.html', cat_art=session['cat_art'])

@app.route('/login', methods=['GET', 'POST'])
def do_login():
	if 'credentials' not in session:
		global g_credentials
		session['credentials'] = g_credentials

	if request.method == 'POST':

		if request.form['username'] in session['credentials'] and session['credentials'][request.form['username']] == request.form['password']:
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
			reset_session()

	return home()

@app.route("/logout")
def logout():
	session['logged_in'] = False
	session.pop("username", None)
	return home()

if __name__ == "__main__":
	app.secret_key = os.urandom(12)
	global g_credentials
	g_credentials = load_credentials("default.json")
	app.run(debug=True,host='0.0.0.0', port=4000)