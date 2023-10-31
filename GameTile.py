import random
class GameTile:
    def __init__(self, type, instance, x_location=0, y_location=0):
        self.name = f'{type}{str(instance)}'
        self.type = type
        self.x_position = x_location
        self.y_position = y_location
        self.tile = f'{x_location}{y_location}'
        self.players_on_tile = []
        if type == 'empty':
            self.symbol = 0
            self.resource = 0
            self.passable = True
        elif type == 'obstacle':
            self.symbol = 'o'
            self.resource = 0
            self.passable = False
        elif type == 'mine':
            self.symbol = 'm'
            self.resource = random.randint(16, 32)
            self.passable = False
        elif type == 'player_base':
            self.symbol = self.name
            self.resource = 0
            self.passable = False
            self.symbol = 'b'

    def update_location(self, x, y):
        self.x_position = x
        self.y_position = y
        self.coords = [x, y]
        self.tile = f'{x}{y}'