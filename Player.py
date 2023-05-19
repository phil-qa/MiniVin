class Player:
    def __init__(self, identifier):
        self.name = identifier
        self.x_pos = None
        self.y_pos = None
        self.health = None
        self.max_health = None
        self.resource = 0
        self.target_x = None
        self.target_y = None
        self.coords = None
        self.target_coords = None
        self.tile = None


    def set(self,x_pos, y_pos, health):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.coords = [x_pos,y_pos]
        self.tile = f'{x_pos}{y_pos}'
        self.max_health = self.health = health

    def set_target(self,x_pos, y_pos):
        self.target_x = x_pos
        self.target_y = y_pos
        self.target_coords = [x_pos,y_pos]

    def move_player(self, direction):
        if direction == 'n':
            self.y_pos -= 1
        elif direction == 'e':
            self.x_pos += 1
        elif direction == 's':
            self.y_pos += 1
        elif direction == 'w':
            self.x_pos -= 1
        elif direction == 'h':
            return
        self.coords = [self.x_pos, self.y_pos]
        self.tile = f'{self.x_pos}{self.y_pos}'