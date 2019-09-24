import json

class Calibration(object):
    def __init__(self):
        caldata = json.load(open('app/calibrate.json'))
        self.CROP = caldata['crop']
        self.SITES = caldata['sites']
        self.GRIPA = caldata['gripa']
        self.GRIPB = caldata['gripb']
        self.TWISTA = caldata['twista']
        self.TWISTB = caldata['twistb']
        self.COLORS = caldata['colors']
        self.COLOR_LIMITS = caldata['color_limits']

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
        elif prop == "color_limits":
            value = self.COLOR_LIMITS[param]
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
        elif prop == "color_limits":
            self.COLOR_LIMITS[param] = value
        self.write_to_file()

    def write_to_file(self):
        data = {
            'crop': self.CROP,
            'sites': self.SITES,
            'gripa': self.GRIPA,
            'gripb': self.GRIPB,
            'twista': self.TWISTA,
            'twistb': self.TWISTB,
            'colors': self.COLORS,
            'color_limits': self.COLOR_LIMITS
        }
        with open('app/calibrate.json', 'w') as outfile:
            json.dump(data, outfile)
