class PlayerBase:
    def __init__(self, x_location, y_location):
        self.x_position = x_location
        self.y_position = y_location
        self.resource = 0
        self.player = None
        self.coords = [x_location, y_location]
        self.name = f'{x_location}{y_location}'


