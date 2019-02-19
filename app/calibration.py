import json

class Calibration(object):
    def __init__(self):
        calibrate = json.load(open('app/calibrate.json'))
        self.CROP = {
            'tl': calibrate['crop']['tl'],
            'size': calibrate['crop']['size']
        }
        self.SITES = {
            'tlx': calibrate['sites']['tlx'],
            'tly': calibrate['sites']['tly'],
            'size': calibrate['sites']['size'],
            'pitch': calibrate['sites']['pitch']
        }
        self.GRIPA = {
            'open': calibrate['gripa']['open'],
            'close': calibrate['gripa']['close'],
            'load': calibrate['gripa']['load'],
            'ccw': calibrate['gripa']['ccw'],
            'cw': calibrate['gripa']['cw'],
            'center': calibrate['gripa']['center']
        }
        self.GRIPB = {
            'open': calibrate['gripb']['open'],
            'close': calibrate['gripb']['close'],
            'load': calibrate['gripb']['load'],
            'ccw': calibrate['gripb']['ccw'],
            'cw': calibrate['gripb']['cw'],
            'center': calibrate['gripb']['center']
        }
        self.COLORS = {
            'red': calibrate['colors']['red'],
            'orange': calibrate['colors']['orange'],
            'yellow': calibrate['colors']['yellow'],
            'green': calibrate['colors']['green'],
            'blue': calibrate['colors']['blue'],
            'white': calibrate['colors']['white'],
        }

    def get_property(self, prop, param):
        value = None
        if prop == "crop":
            value = self.CROP[param]
        elif prop == "sites":
            value = self.SITES[param]
        elif prop == "gripa":
            value = self.GRIPA[param]
        elif prop == "gripb":
            value = self.GRIPB[param]
        elif prop == "colors":
            value = self.COLORS[param]
        return value

    def set_property(self, prop, param, value):
        if prop == "crop":
            self.CROP[param] = value
        elif prop == "sites":
            self.SITES[param] = value
        elif prop == "gripa":
            self.GRIPA[param] = value
        elif prop == "gripb":
            self.GRIPB[param] = value
        elif prop == "colors":
            self.COLORS[param] = value
        self.write_to_file()

    def write_to_file(self):
        data = {
            'crop': self.CROP,
            'sites': self.SITES,
            'gripa': self.GRIPA,
            'gripb': self.GRIPB,
            'colors': self.COLORS
        }
        with open('app/calibrate.json', 'w') as outfile:
            json.dump(data, outfile)
