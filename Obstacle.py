class Obstacle:
    def __init__(self, x_location, y_location, passble):
        self.x_location = x_location
        self.y_location = y_location
        self.coords = [x_location, y_location]
        self.passble = passble
        self.tile = f'{x_location}{y_location}'