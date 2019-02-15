import time
#from adafruit_servokit import ServoKit

# for convenience in referening array index
tp = {'ccw': 0, 'center': 1, 'cw': 2}

class Bot(object):
    SLEEP_TIME = 0.5 # time to sleep after sending servo cmd
    # channels on servo pwm board
    grip_channel = {'A': 0, 'B': 2}
    twist_channel = {'A': 1, 'B': 3}
    
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
        self.update_cal(cal_data) # get/update calibration data for in this instance
        #self.kit = ServoKit(channels=8) # initialize the servo kit
		# initialize both grippers to open/center position
        # set positions directly to ensure exact position at start
        #for grip in ['A', 'B']:
        #    self.kit.servo[grip_channel[grip]].angle = self.GRIP_POS[grip]['o']
        #    self.kit.servo[twist_channel[grip]].angle = self.TWIST_POS[grip][1]

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

    def grip(self, gripper, cmd):
        """
        Function to open or close gripper
        gripper = 'A' or 'B'
        cmd = 'o' 'c' or 'l' for load
        """
        #self.kit.servo[grip_channel[gripper]].angle = self.GRIP_POS[gripper][cmd]
        time.sleep(self.SLEEP_TIME)
        self.GRIP_STATE[gripper] = cmd
        return [0, cmd]

    def twist(self, gripper, dir):
        """
        Function to twist face without moving cube
        gripper = 'A' or 'B'
        dir = '+' 90-deg CW, '-' 90-deg CCW
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

        #self.kit.servo[twist_channel[gripper]].angle = self.TWIST_POS[gripper][new_state]
        time.sleep(self.SLEEP_TIME)
        self.TWIST_STATE[gripper] = new_state
        return [0 if self.GRIP_STATE[other_gripper] == 'o' else 1, dir] # return 0 if this twist moves cube and changes orientation, else return 1

