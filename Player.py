from Pathing import Pathing


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
        self.previous_tile = None
        self.returning = False

    def set(self,x_pos, y_pos, health):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.coords = [x_pos,y_pos]
        self.tile = f'{x_pos}{y_pos}'
        self.previous_tile = self.tile
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
        try:
            print(f"{self.name} is moving from {self.previous_tile} to {tile}")
            if tile != self.previous_tile:
                self.previous_tile = self.tile
            self.coords = [int(tile[0]), int(tile[1])]
            self.x_pos = self.coords[0]
            self.y_pos = self.coords[1]
            self.tile = tile
        except() as e:
            print(e.message)

    def go_back(self):
        self.tile = self.previous_tile

    def return_to_base(self, map):
        self.returning = True
        path_to_base = Pathing.find_path(self.tile, self.base, map)
        return path_to_base[1]

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
