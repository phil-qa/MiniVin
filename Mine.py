class Mine:
    def __init__(self, x_loc, y_loc, name):
        self.name = name
        self.x_location = x_loc
        self.y_location = y_loc
        self.coords = [x_loc, y_loc]
        self.tile = f'{x_loc}{y_loc}'

