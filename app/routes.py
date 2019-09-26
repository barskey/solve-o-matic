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

@app.route('/ready_load')
def ready_load():
	return mybot.ready_load()

@app.route('/calibration')
def settings():
	#mybot.save_snapshot()
	image = mybot.get_imagestream()
	img = base64.b64encode(image.getvalue()).decode('utf-8')
	return render_template('calibration.html', title='Calibration', cal=cal, img=img) # TODO should I get servo_range from mybot?

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

@app.route('/set_color_slider', methods=['POST'])
def set_color_slider():
	setting = request.form['setting']
	value = request.form['val']
	print('color_slider', setting, value)

	cal.set_property('color_limits', setting, float(value))
	mybot.update_cal(cal)
	
	return jsonify(mybot.process_face())

@app.route('/get_sites', methods=['POST'])
def get_sites():
	return jsonify({'sites': cal.sites})

@app.route('/get_face_colors', methods=['POST'])
def get_face_colors():
	return jsonify(mybot.process_face())

@app.route('/move_gripper', methods=['POST'])
def move_gripper():
	gripper = request.form['gripper'][-1].upper() # last character to upper case e.g. 'A' from 'gripa'
	cmd = request.form['cmd']

	result = None
	if cmd in ['open', 'load', 'close']:
		result = mybot.grip(gripper, cmd[0]) # cmd[0] is first character, hence 'o' 'l' or 'c'
	elif cmd in ['ccw', 'center', 'cw']:
		result = mybot.twist(gripper, cmd)
	elif cmd in ['min', 'max']:
		result = mybot.twist(gripper, cmd)
	
	return jsonify({'code': result[0], 'msg': result[1]})

@app.route('/scan_next', methods=['POST'])
def scan_next():
	if request.form['start'] == 'true':
		result = mybot.start_scan()
		return jsonify({'msg': result[1], 'result': result[0]})
	else:
		result = 0
		while result != 1:
			r = mybot.scan_move()
			return jsonify(mybot.process_face())
