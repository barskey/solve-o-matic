from flask import render_template, request
from flask import jsonify
from app import app
from app import calibration, bot
import json
from picamera import PiCamera
from io import BytesIO
from PIL import Image
import time

cal = calibration.Calibration()
bot = bot.Bot(cal)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Main Menu')
	
@app.route('/scan')
def scan():
	return render_template('scan.html', title='Scan')

@app.route('/calibration')
def settings():
	#stream = BytesIO()
	#camera = PiCamera()
	#camera.resolution = (80, 80)
	#camera.start_preview()
	#time.sleep(2) #  carmera warm-up?
	#camera.capture(stream, format='jpeg')
	#stream.seek(0) #  "Rewind" the stream to the beginning so we can read its content
	#image = Image.open(stream)
	cal_data = json.load(open('app/calibrate.json'))
	return render_template('calibration.html', title='Calibration', cal_data=cal_data)

@app.route('/set_cal_data', methods=['POST'])
def set_calibrate():
	prop = request.form['prop']
	setting = request.form['setting']
	mod = request.form['mod']

	delta = 1 if mod == 'more' else -1
		
	new_value = cal.get_property(prop, setting) + delta

	cal.set_property(prop, setting, new_value)
	bot.update_cal(cal)
	
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
		result = bot.grip(gripper, cmd[0]) # cmd[0] is first character, hence 'c' 'o' or 'l'
	elif cmd in ['ccw', 'center', 'cw']:
		result = bot.twist(gripper, cmd)
	
	return jsonify({'code': result[0], 'msg': result[1]})

@app.route('/scan_next', methods=['POST'])
def scan_next():
	if request.form['start'] == 'true':
		result = bot.scan_cube()
		return jsonify({'msg': result[1]})
	else:
		result = bot.scan_move()
		return jsonify({'upface': result})

@app.route('/process_img', methods=['POST'])
def process_img():
	face = request.form['face']
	header,img = request.form['imgdata'].split(',') # get image from post data
	result = bot.process_face(face, img, cal.SITES)

	return jsonify({'colors': result['face_colors'], 'face': face, 'unsure': result['unsure_sites']})
