class Obstacle:
    def __init__(self, x_location, y_location, passble):
        self.x_position = x_location
        self.y_position = y_location
        self.coords = [x_location, y_location]
        self.passble = passble
        self.name = f'obstacle'