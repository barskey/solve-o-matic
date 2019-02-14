from flask import render_template, request
from flask import jsonify
from app import app
import json

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Main Menu')
	
@app.route('/scan')
def scan():
	return render_template('scan.html', title='Scan')

@app.route('/settings')
def settings():
	settings = json.load(open('app/calibrate.json'))
	return render_template('settings.html', title='Settings', settings=settings)

@app.route('/get_calibrate', methods=['POST'])
def get_config():
	config = json.load(open('app/calibrate.json'))
	return jsonify({'config': config})

@app.route('/set_calibrate', methods=['POST'])
def set_calibrate():
	calibrate = json.load(open('app/calibrate.json'))
	setting = request.form['setting']
	cmd = request.form['cmd']
	value = request.form['value']

	new_value = calibrate[setting][value] + 

	calibrate[setting][value] = 1
	return jsonify({'data': 'Test message'})
	
def scan_cube():
	pass
