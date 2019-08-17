import time
from app import rscube
from adafruit_servokit import ServoKit
import base64
import io
from PIL import Image, ImageStat
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

# for convenience in referening array index
tp = {'ccw': 0, 'center': 1, 'cw': 2}
tpk = ['ccw', 'center', 'cw']

THRESHOLD = 10

# with cube starting in UFD, these sides can be rotated to scan each side in proper rotation (0)
# perform moves, then scan -- hence no moves before scanning U
MOVES_FOR_SCAN = [
    [''],                                                # UFD-scan U
    ['Bo','A+','Bc','Ao','A-','B+','Ac','Bo','B-','Bc'], # LDR-scan L
    ['Bo','A-','Bc','Ao','A+','Ac'],                     # FDB-scan F
    ['Bo','A-','Bc','Ao','A+','Ac'],                     # RDL-scan R
    ['Bo','A-','Bc','Ao','A+','Ac'],                     # BDF-scan B
    ['Ao','B-','Ac','Bo','B-','A+','Bc',
        'Ao','A-','B-','Ac','Bo','B-','Bc']              # DBU-scan D
]

class Bot(object):
    CUBE = None
    colors = []

    kit = None
    SLEEP_TIME = 0.5 # time to sleep after sending servo cmd
    # channels on servo pwm board
    grip_channel = {'A': 1, 'B': 3}
    twist_channel = {'A': 0, 'B': 2}
    
    GRIP_STATE = {'A': 'o', 'B': 'o'}
    TWIST_STATE = {'A': tp['center'], 'B': tp['center']}
    GRIP_POS = {
        'A': {'o': 0, 'c': 0, 'l': 0},
        'B': {'o': 0, 'c': 0, 'l': 0}
    }
    TWIST_POS = {
        'A': [0, 0, 0],
        'B': [0, 0, 0]
    }

    def __init__(self, cal_data):
        self.CUBE = rscube.MyCube()
        self.update_cal(cal_data) # get/update calibration data for in this instance
        #self.kit = ServoKit(channels=8) # initialize the servo kit
		# initialize both grippers to open/center position
        # set positions directly to ensure exact position at start
        #for grip in ['A', 'B']:
        #    self.kit.servo[self.grip_channel[grip]].angle = self.GRIP_POS[grip]['o']
        #    self.kit.servo[self.twist_channel[grip]].angle = self.TWIST_POS[grip][1]

    def update_cal(self, cal_data):
        self.GRIP_POS['A'] = {
            'o': cal_data.GRIPA['open'],
            'c': cal_data.GRIPA['close'],
            'l': cal_data.GRIPA['load']
        }
        self.GRIP_POS['B'] = {
            'o': cal_data.GRIPB['open'],
            'c': cal_data.GRIPB['close'],
            'l': cal_data.GRIPB['load']
        }
        self.TWIST_POS['A'] = [
            cal_data.GRIPA['ccw'],
            cal_data.GRIPA['center'],
            cal_data.GRIPA['cw']
        ]
        self.TWIST_POS['B'] = [
            cal_data.GRIPB['ccw'],
            cal_data.GRIPB['center'],
            cal_data.GRIPB['cw']
        ]
        # move/rotate grippers to current/new positions
        for g in ['A', 'B']:
            self.grip(g, self.GRIP_STATE[g])
            self.twist(g, tpk[self.TWIST_STATE[g]])

    def grip(self, gripper, cmd):
        """
        Function to open or close gripper
        gripper = 'A' or 'B'
        cmd = 'o' 'c' or 'l' for load
        """
        #self.kit.servo[self.grip_channel[gripper]].angle = self.GRIP_POS[gripper][cmd]
        time.sleep(self.SLEEP_TIME)
        self.GRIP_STATE[gripper] = cmd
        return [0, cmd]

    def twist(self, gripper, dir):
        """
        Function to twist gripper, either twisting face or rotating cube
        gripper = 'A' or 'B'
        dir = '+' 90-deg CW, '-' 90-deg CCW
        dir = 'ccw', 'center', 'cw' sets to that position
        returns
            ERROR [-1, 'error msg'] no move or twist
            SUCCESS [0, 'dir'] twisted cube
            SUCCESS [1, 'dir'] twisted face
        """
        other_gripper = 'B' if gripper == 'A' else 'A'

        new_state = None
        if dir == '-':
            if self.TWIST_STATE[gripper] == 0:
                return [-1, 'Already at min ccw position.']
            else:
                new_state = self.TWIST_STATE[gripper] - 1
        elif dir == '+':
            if self.TWIST_STATE[gripper] == len(self.TWIST_STATE[gripper]) - 1:
                return [-1, 'Already at max cw position.']
            else:
                new_state = self.TWIST_STATE[gripper] + 1
        elif dir in ['ccw', 'center', 'cw']:
            new_state  = tp[dir]
        
        if new_state is None:
            return [-1, 'Could not twist. Unknown error.']

        if self.GRIP_STATE[gripper] == 'l': # don't twist if gripper is in load position
            return [-1, 'Can\'t twist {}. Gripper {} currently in {} position.'.format(gripper, other_gripper, self.GRIP_STATE[gripper])]
        if self.GRIP_STATE[other_gripper] == 'l': # don't twist if other gripper is in load position
            return [-1, 'Can\'t twist {}. Gripper {} currently in load position.'.format(gripper, other_gripper)]

        #self.kit.servo[self.twist_channel[gripper]].angle = self.TWIST_POS[gripper][new_state]
        time.sleep(self.SLEEP_TIME)
        self.TWIST_STATE[gripper] = new_state
        return [0 if self.GRIP_STATE[other_gripper] == 'o' else 1, dir] # return 0 if this twist moves cube and changes orientation, else return 1

    def scan_cube(self):
        self._scan_index = 0
        self.CUBE.orientation = 'UFD'
        self.grip('B','c')
        self.grip('A','c')
        return [0, 'Ready']

    def scan_move(self):
        if self._scan_index >= len(MOVES_FOR_SCAN):
            return 'Done!'

        for move in MOVES_FOR_SCAN[self._scan_index]:
            if len(move) > 0:
                gripper = move[0]
                cmd = move[1]
                if cmd in ['+', '-']:
                    result = self.twist(gripper, cmd)
                    if result[0] == 0:
                        self.CUBE.set_orientation(gripper, cmd)
                elif cmd in ['o', 'c', 'l']:
                    result = self.grip(gripper, cmd)
                self._scan_index = self._scan_index + 1

        return self.CUBE.get_up_face()

    def process_face(self, face, img, sites):
        """
        Gets image from camera, crops and gets average (mean) colors
        in each region, and stores in _raw_colors.
        Returns list of colors on this face for uix
        """
        img_decoded = base64.b64decode(img)
        face_img = Image.open(io.BytesIO(img_decoded))

        # loop through each site and store its raw color
        sitenum = 0
        face_colors = [None for i in range(9)]
        unsure_sites = []
        for row in range(0, 3):
            for col in range(0, 3):
                left = sites['tlx'] + (col * sites['pitch'])
                upper = sites['tly'] + (row * sites['pitch'])
                site = face_img.crop((left, upper, left + sites['size'], upper + sites['size'])) # crop the img so only the site is left
                #site.show() # debug
                mean_color = ImageStat.Stat(site).mean
                match_color, delta_e = find_closest_color(mean_color, self.colors)
                #print (match_color, delta_e) # debug
                if delta_e > THRESHOLD:
                    if len(self.colors) < 6: # store this color since list is not populated yet
                        self.colors.append(mean_color)
                        self.CUBE.set_raw_color(face, sitenum, mean_color)
                    else:
                        unsure_sites.append(sitenum)
                else:
                    self.CUBE.set_raw_color(face, sitenum, match_color)
                
                hex_color = '#' + format(int(mean_color[0]), 'x') + format(int(mean_color[1]), 'x') + format(int(mean_color[2]), 'x')
                face_colors[sitenum] = hex_color # return the hex color
                sitenum = sitenum + 1
        print(self.colors)
        return {'face_colors': face_colors, 'unsure_sites': unsure_sites}


def find_closest_color(color, colors_to_check):
	# create Color object from site color and convert to lab color for comparison
	r, g, b, a = (x / 255.0 for x in color)
	site_color_lab = convert_color(sRGBColor(r, g, b), LabColor)
	last_delta_e = 999
	match_color = None
	for c in colors_to_check:
		r, g, b, a = (x / 255.0 for x in c)
		check_color_lab = convert_color(sRGBColor(r, g, b), LabColor) # convert to lab color for comparison
		delta_e = delta_e_cie2000(site_color_lab, check_color_lab)
		if delta_e < last_delta_e: # use this check to find the closest match
			match_color = c
			last_delta_e = delta_e
	return match_color, last_delta_e
