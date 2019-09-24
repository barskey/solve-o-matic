from flask import render_template, request
from flask import jsonify
from app import app
from app import calibration, bot
import json
import time
import base64

cal = calibration.Calibration()
mybot = bot.Bot(cal)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Main Menu')
	
@app.route('/scan')
def scan():
	image = mybot.get_imagestream()
	img = base64.b64encode(image.getvalue()).decode('utf-8')
	return render_template('scan.html', title='Scan', img=img)

@app.route('/calibration')
def settings():
	#mybot.save_snapshot()
	image = mybot.get_imagestream()
	img = base64.b64encode(image.getvalue()).decode('utf-8')
	return render_template('calibration.html', title='Calibration', servo_range=mybot.servo_range, color_limit=mybot.color_limit, img=img)

@app.route('/set_cal_data', methods=['POST'])
def set_calibrate():
	prop = request.form['prop']
	setting = request.form['setting']
	value = request.form['val']
	print(prop, setting, value)
	new_value = cal.get_property(prop, setting) + int(value)

	cal.set_property(prop, setting, new_value)
	mybot.update_cal(cal)
	if setting in ['min', 'max']:
		mybot.init_servos()
	
	return jsonify({'prop': prop, 'setting': setting, 'value': new_value})

@app.route('/get_sites', methods=['POST'])
def get_sites():
	return jsonify({'sites': cal.SITES})

@app.route('/move_gripper', methods=['POST'])
def move_gripper():
	gripper = request.form['gripper'][-1].upper() # last character to upper case e.g. 'A' from 'gripa'
	cmd = request.form['cmd']

	result = None
	if cmd in ['open', 'load', 'close']:
		result = mybot.grip(gripper, cmd[0]) # cmd[0] is first character, hence 'c' 'o' or 'l'
	elif cmd in ['ccw', 'center', 'cw']:
		result = mybot.twist(gripper, cmd)
	elif cmd in ['min', 'max']:
		result = mybot.twist(gripper, cmd)
	
	return jsonify({'code': result[0], 'msg': result[1]})

@app.route('/scan_next', methods=['POST'])
def scan_next():
	if request.form['start'] == 'true':
		result = mybot.scan_cube()
		return jsonify({'msg': result[1], 'result': result[0]})
	else:
		result = mybot.scan_move()
		if result[0] == 0:
			r = mybot.process_face(cal.SITES)
			return jsonify(r)
