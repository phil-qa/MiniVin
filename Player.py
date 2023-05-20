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
        self.base = self.tile

    def set_target(self,x_pos, y_pos):
        self.target_x = x_pos
        self.target_y = y_pos
        self.target_coords = [x_pos,y_pos]

    def update_coords(self, x, y):
        self.coords = [x,y]
        self.x_pos = x
        self.y_pos = y
        self.tile=f'{x}{y}'

    def move_player(self, tile):
        self.coords = [tile[0], tile[1]]
        self.tile = tile

    def next_tile(self, direction):
        x = self.x_pos
        y = self.y_pos
        if direction == 'n':
            y -= 1
        elif direction == 'e':
            x += 1
        elif direction == 's':
            y += 1
        elif direction == 'w':
            x -= 1
        elif direction == 'h':
            return f'{self.x_pos}{self.y_pos}'
        return f'{x}{y}'
