import json

class Calibration(object):
    def __init__(self):
        caldata = json.load(open('app/calibrate.json'))
        self.CROP = {
            'tl': caldata['crop']['tl'],
            'size': caldata['crop']['size']
        }
        self.SITES = {
            'tlx': caldata['sites']['tlx'],
            'tly': caldata['sites']['tly'],
            'size': caldata['sites']['size'],
            'pitch': caldata['sites']['pitch']
        }
        self.GRIPA = {
            'open': caldata['gripa']['open'],
            'close': caldata['gripa']['close'],
            'load': caldata['gripa']['load'],
            'ccw': caldata['gripa']['ccw'],
            'cw': caldata['gripa']['cw'],
            'center': caldata['gripa']['center'],
            'min': caldata['gripa']['min'],
            'max': caldata['gripa']['max']
        }
        self.GRIPB = {
            'open': caldata['gripb']['open'],
            'close': caldata['gripb']['close'],
            'load': caldata['gripb']['load'],
            'ccw': caldata['gripb']['ccw'],
            'cw': caldata['gripb']['cw'],
            'center': caldata['gripb']['center'],
            'min': caldata['gripb']['min'],
            'max': caldata['gripb']['max']
        }
        self.TWISTA = {
            'min': caldata['twista']['min'],
            'max': caldata['twista']['max']
        }
        self.TWISTB = {
            'min': caldata['twistb']['min'],
            'max': caldata['twistb']['max']
        }
        self.COLORS = {
            'red': caldata['colors']['red'],
            'orange': caldata['colors']['orange'],
            'yellow': caldata['colors']['yellow'],
            'green': caldata['colors']['green'],
            'blue': caldata['colors']['blue'],
            'white': caldata['colors']['white'],
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
        elif prop == "twista":
            value = self.TWISTA[param]
        elif prop == "twistb":
            value = self.TWISTB[param]
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
        elif prop == "twista":
            self.TWISTA[param] = value
        elif prop == "twistb":
            self.TWISTB[param] = value
        elif prop == "colors":
            self.COLORS[param] = value
        self.write_to_file()

    def write_to_file(self):
        data = {
            'crop': self.CROP,
            'sites': self.SITES,
            'gripa': self.GRIPA,
            'gripb': self.GRIPB,
            'twista': self.TWISTA,
            'twistb': self.TWISTB,
            'colors': self.COLORS
        }
        with open('app/calibrate.json', 'w') as outfile:
            json.dump(data, outfile)
