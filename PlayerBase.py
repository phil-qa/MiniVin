class PlayerBase:
    def __init__(self, x_location, y_location):
        self.x_location = x_location
        self.y_location = y_location
        self.resource = 0
        self.player = None
        self.coords = [x_location, y_location]

