import json

class Calibration(object):
    def __init__(self):
        self.load_from_file()
    
    def load_from_file(self):
        caldata = json.load(open('app/calibrate.json'))
        self.crop = caldata['crop']
        self.sites = caldata['sites']
        self.gripa = caldata['gripa']
        self.gripb = caldata['gripb']
        self.twista = caldata['twista']
        self.twistb = caldata['twistb']
        self.colors = caldata['colors']
        self.color_limits = caldata['color_limits']

    def get_property(self, prop, param):
        value = None
        if prop == "crop":
            value = self.crop[param]
        elif prop == "sites":
            value = self.sites[param]
        elif prop == "gripa":
            value = self.gripa[param]
        elif prop == "gripb":
            value = self.gripb[param]
        elif prop == "twista":
            value = self.twista[param]
        elif prop == "twistb":
            value = self.twistb[param]
        elif prop == "colors":
            value = self.colors[param]
        elif prop == "color_limits":
            value = self.color_limits[param]
        return value

    def set_property(self, prop, param, value):
        if prop == "crop":
            self.crop[param] = value
        elif prop == "sites":
            self.sites[param] = value
        elif prop == "gripa":
            self.gripa[param] = value
        elif prop == "gripb":
            self.gripb[param] = value
        elif prop == "twista":
            self.twista[param] = value
        elif prop == "twistb":
            self.twistb[param] = value
        elif prop == "colors":
            self.colors[param] = value
        elif prop == "color_limits":
            self.color_limits[param] = value
        self.write_to_file()

    def write_to_file(self):
        data = {
            'crop': self.crop,
            'sites': self.sites,
            'gripa': self.gripa,
            'gripb': self.gripb,
            'twista': self.twista,
            'twistb': self.twistb,
            'colors': self.colors,
            'color_limits': self.color_limits
        }
        with open('app/calibrate.json', 'w') as outfile:
            json.dump(data, outfile)
