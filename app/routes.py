from flask import render_template, request
from flask import jsonify
from app import app
from app import calibration, rscube
import json

cal = calibration.Calibration()
cube = rscube.MyCube()

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

@app.route('/set_calibrate', methods=['POST'])
def set_calibrate():
	gripper = request.form['gripper']
	setting = request.form['setting']
	mod = request.form['mod']

	delta = 1 if mod == 'more' else -1
	new_value = cal.get_property(gripper, setting) + delta

	cal.set_property(gripper, setting, new_value)
	#print (gripper, setting, new_value)
	return jsonify({'gripper': gripper, 'setting': setting, 'value': new_value})

@app.route('/move_gripper', methods=['POST'])
def move_gripper():
	gripper = request.form['gripper'][-1].upper()
	cmd = request.form['cmd']
	if cmd in ['open', 'load', 'close']:
		mycube.grip(gripper, cmd[0])
	elif cmd in ['ccw', 'center', 'cw']:
		mycube.twist_absolute(gripper, cmd)
	return jsonify({'msg': True})
	
def scan_cube():
	pass
