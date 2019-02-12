from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Main Menu')
	
@app.route('/scan')
def scan():
	return render_template('scan.html', title='Scan')

@app.route('/settings')
def settings():
	return render_template('settings.html', title='Settings')