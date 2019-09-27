import time
import threading
from app import rscube
from adafruit_servokit import ServoKit
from picamera import PiCamera, Color
import base64
from io import BytesIO
from PIL import Image, ImageStat

# for convenience in referening array index
tp = {'ccw': 0, 'center': 1, 'cw': 2}
tpk = ['ccw', 'center', 'cw']

THRESHOLD = 10

# channels on servo pwm board
GRIP_CHANNEL = {'A': 1, 'B': 3}
TWIST_CHANNEL = {'A': 0, 'B': 2}
SLEEP_TIME = 0.5 # time to sleep after sending servo cmd

kit = ServoKit(channels=8)

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
    _grip_state = {'A': 'o', 'B': 'o'}
    _twist_state = {'A': tp['center'], 'B': tp['center']}
    _grip_pos = {
        'A': {'o': 0, 'c': 0, 'l': 0},
        'B': {'o': 0, 'c': 0, 'l': 0}
    }
    _twist_pos = {
        'A': [0, 0, 0],
        'B': [0, 0, 0]
    }
    servo_range = {
        'gA': [520, 2450],
        'gB': [750, 2250],
        'tA': [750, 2250],
        'tB': [680, 2410]
    }

    def __init__(self, cal_data):
        self.cube = rscube.MyCube()
        self.update_cal(cal_data) # get/update calibration data for in this instance
        self.init_servos() # initialize servos to their default ranges/positions
        self.camera = PiCamera()
        self.camera.resolution = (160, 160)
        self.camera.iso = 400
    
    def init_servos(self):
        """ initialize servo pulse ranges """
        for g,channel in GRIP_CHANNEL.items():
            kit.servo[channel].set_pulse_width_range(*self.servo_range['g' + g])
            #print('{} grip{}: {}'.format(channel, g, self.servo_range['g' + g]))
        for g,channel in TWIST_CHANNEL.items():
            kit.servo[channel].set_pulse_width_range(*self.servo_range['t' + g])
            #print('{} twist{}: {}'.format(channel, g, self.servo_range['t' + g]))

    def update_cal(self, cal_data):
        self._grip_pos['A'] = {
            'o': cal_data.gripa['open'],
            'c': cal_data.gripa['close'],
            'l': cal_data.gripa['load']
        }
        self._grip_pos['B'] = {
            'o': cal_data.gripb['open'],
            'c': cal_data.gripb['close'],
            'l': cal_data.gripb['load']
        }
        self._twist_pos['A'] = [
            cal_data.gripa['ccw'],
            cal_data.gripa['center'],
            cal_data.gripa['cw']
        ]
        self._twist_pos['B'] = [
            cal_data.gripb['ccw'],
            cal_data.gripb['center'],
            cal_data.gripb['cw']
        ]
        self.servo_range['gA'] = [cal_data.gripa['min'], cal_data.gripa['max']]
        self.servo_range['gB'] = [cal_data.gripb['min'], cal_data.gripb['max']]
        self.servo_range['tA'] = [cal_data.TWISTA['min'], cal_data.TWISTA['max']]
        self.servo_range['tB'] = [cal_data.TWISTB['min'], cal_data.TWISTB['max']]
        # move/rotate grippers to current/new positions
        #for g in ['A', 'B']:
        #    self.grip(g, self._grip_state[g])
        #    self.twist(g, tpk[self._twist_state[g]])
        self.color_limits = cal_data.color_limits
        self.sites = cal_data.sites

    def grip(self, gripper, cmd):
        """
        Function to open or close gripper
        gripper = 'A' or 'B'
        cmd = 'o' 'c' or 'l' for load
        """
        set_servo_angle(GRIP_CHANNEL[gripper], self._grip_pos[gripper][cmd])
        time.sleep(SLEEP_TIME)
        self._grip_state[gripper] = cmd
        return [0, cmd]

    def twist(self, gripper, dir):
        """
        Function to twist gripper, either twisting face or rotating cube
        gripper = 'A' or 'B'
        dir = 'min' or 'max'
        dir = '+' 90-deg CW, '-' 90-deg CCW
        dir = 'ccw', 'center', 'cw' sets to that position
        returns
            ERROR [-1, 'error msg'] no move or twist
            SUCCESS [0, dir] turned cube
            SUCCESS [1, dir] twisted face
        """
        other_gripper = 'B' if gripper == 'A' else 'A'
        new_state = None

        if dir == 'min':
            set_servo_angle(TWIST_CHANNEL[gripper], 0)
            return [2, 'min']
        if dir == 'max':
            set_servo_angle(TWIST_CHANNEL[gripper], 180)
            return [2, 'max']
        if dir == '-':
            if self._twist_state[gripper] == 0:
                return [-1, 'Already at min ccw position.']
            else:
                new_state = self._twist_state[gripper] - 1
        elif dir == '+':
            if self._twist_state[gripper] == len(self._twist_state[gripper]) - 1:
                return [-1, 'Already at max cw position.']
            else:
                new_state = self._twist_state[gripper] + 1
        elif dir in ['ccw', 'center', 'cw']:
            new_state  = tp[dir]
        
        if new_state is None:
            return [-1, 'Could not twist. Unknown error.']

        if self._grip_state[gripper] == 'l': # don't twist if gripper is in load position
            return [-1, 'Can\'t twist {}. Gripper {} currently in {} position.'.format(gripper, other_gripper, self._grip_state[gripper])]
        if self._grip_state[other_gripper] == 'l': # don't twist if other gripper is in load position
            return [-1, 'Can\'t twist {}. Gripper {} currently in load position.'.format(gripper, other_gripper)]

        set_servo_angle(TWIST_CHANNEL[gripper], self._twist_pos[gripper][new_state])
        time.sleep(SLEEP_TIME)
        
        self._twist_state[gripper] = new_state
        return [0 if self._grip_state[other_gripper] == 'o' else 1, dir] # return 0 if this twist moves cube and changes orientation, else return 1
    
    def ready_load(self):
        """ moves grippers to load positions """
        # open first so they don't collide as they twist
        self.grip('A', 'o')
        self.grip('B', 'o')
        # move both to center
        self.twist('A', 'center')
        self.twist('B', 'center')
        # move both to load
        self.grip('A', 'l')
        self.grip('B', 'l')
        return 0

    def start_scan(self):
        self._scan_index = 0
        self.cube.reset_cube()
        self.grip('B','c')
        self.grip('A','c')
        return [0, 'Ready']

    def scan_move(self):
        if self._scan_index >= len(MOVES_FOR_SCAN):
            return [1, 'Done!']

        for move in MOVES_FOR_SCAN[self._scan_index]:
            if len(move) > 0:
                gripper = move[0]
                cmd = move[1]
                if cmd in ['+', '-']:
                    result = self.twist(gripper, cmd)
                    if result[0] == 0:
                        self.cube.set_orientation(gripper, cmd)
                elif cmd in ['o', 'c', 'l']:
                    result = self.grip(gripper, cmd)
        self._scan_index += 1
        return [0, 'Move done.']
    
    def save_snapshot(self):
        #camera.start_preview(fullscreen=False, window=(255,98,160,160))
        self.camera.capture('app/static/images/snapshot.jpg')
        #camera.stop_preview()

    def get_imagestream(self):
        """ Captures to BytesIO (python in-memory stream class) """
        stream = BytesIO() # create the in-memory stream
        #camera.start_preview(fullscreen=False, window=(255,98,160,160))
        self.camera.capture(stream, 'jpeg')
        #camera.stop_preview()
        # "Rewind" the stream to the beginning so we can read its content
        stream.seek(0)
        return stream

    def process_face(self):
        """
        Gets image from camera, crops and gets average (mean) colors in each site.
        Saves colors on cube and returns color list and face name for uix.
        """
        face_img = Image.open(self.get_imagestream()) # open in-memory stream as PIL image

        # loop through each site and determine color
        face_colors = []
        for row in range(3):
            for col in range(3):
                print('r{}c{}'.format(row, col)) # debug
                left = self.sites['tlx'] + (col * self.sites['pitch'])
                upper = self.sites['tly'] + (row * self.sites['pitch'])
                box = (left, upper, left + self.sites['size'], upper + self.sites['size'])
                site = face_img.crop(box) # crop the img so only the site is left

                mean_color = ImageStat.Stat(site).mean
                c = Color.from_rgb_bytes(mean_color[0], mean_color[1], mean_color[2])
                site_color = self.get_color(c)
                print('Color identified:{}'.format(str(site_color)))
                face_colors.append(str(site_color)) # save the hex color
        # TODO check if range of colors is high on site 4-center, and guess that it is a logo

        colors_r = self.cube.set_face_colors(face_colors) # set cube face colors, and get back rotated list
        return {'colors': colors_r, 'upface': self.cube.get_up_face()}
    
    def get_color(self, c):
        """ Decide the color by its h value (non-white) or by s and v (white) """
        h,s,v = c.hsv
        print('H:{} S:{} V:{}'.format(h, s, v))
        if s <= self.color_limits['sat_W'] and v >= self.color_limits['val_W']:
            return Color('white')
        elif self.color_limits['orange_L'] <= h < self.color_limits['orange_H']:
            return Color('orange')
        elif self.color_limits['orange_H'] <= h < self.color_limits['yellow_H']:
            return Color('yellow')
        elif self.color_limits['yellow_H'] <= h <= self.color_limits['green_H']:
            if s < 0.5:
                return Color('white') # green saturation is always higher
            else:
                return Color('green')
        elif self.color_limits['green_H'] <= h < self.color_limits['blue_H']:
            if s < 0.5:
                return Color('white') # blue saturation is always higher
            else:
                return Color('blue')
        else:
            return Color('red')
    
    def go_solve(self):
        move_string = self.cube.get_solve_string()
        if move_string != 0:
            moves = move_string.split()
            for move in moves:
                # parse move into command
                    # first char is face to twist as string
                    # no second char means single cw twist
                    # second char as 2 means double cw twist
                    #second char as ' means single ccw twist
                # tell self to move or twust
                # update cube orientation as necessary
                print(move) # debug


def set_servo_angle(s, a):
    print(s,a)
    kit.servo[s].angle = a
