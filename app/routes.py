from flask import render_template, request
from flask import jsonify
from app import app
from app import calibration, rscube, bot
import json
import base64
import io
from PIL import Image, ImageStat

cal = calibration.Calibration()
bot = bot.Bot(cal)
cube = rscube.MyCube()

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Main Menu')
	
@app.route('/scan')
def scan():
	return render_template('scan.html', title='Scan')

@app.route('/calibration')
def settings():
	cal_data = json.load(open('app/calibrate.json'))
	return render_template('calibration.html', title='Calibration', cal_data=cal_data)

@app.route('/set_cal_data', methods=['POST'])
def set_calibrate():
	gripper = request.form['gripper']
	setting = request.form['setting']
	mod = request.form['mod']

	delta = 1 if mod == 'more' else -1
	new_value = cal.get_property(gripper, setting) + delta

	cal.set_property(gripper, setting, new_value)
	bot.update_cal(cal)
	
	return jsonify({'gripper': gripper, 'setting': setting, 'value': new_value})

@app.route('/move_gripper', methods=['POST'])
def move_gripper():
	gripper = request.form['gripper'][-1].upper() # last character to upper case e.g. 'A' from 'gripa'
	cmd = request.form['cmd']
	result = None
	if cmd in ['open', 'load', 'close']:
		result = bot.grip(gripper, cmd[0]) # cmd[0] is first character, hence 'c' 'o' or 'l'
	elif cmd in ['ccw', 'center', 'cw']:
		result = bot.twist(gripper, cmd)
	
	return jsonify({'code': result[0], 'msg': result[1]})

@app.route('/scan', methods=['POST'])
def scan_cube():
	header,img = request.form['imgdata'].split(',')
	img_decoded = base64.b64decode(img)
	face = Image.open(io.BytesIO(img_decoded))
	#face.show() # debug

	return 'ok'
