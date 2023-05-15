class Player:
    def __init__(self, identifier):
        self.name = identifier
        self.x_pos = None
        self.y_pos = None
        self.health = None
        self.max_health = None
        self.resource = 0


    def set(self,x_pos, y_pos, health):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.max_health = self.health = health