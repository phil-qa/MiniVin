from Map import Map
from Mine import Mine
from Obstacle import Obstacle
from Player import Player
from PlayerBase import PlayerBase


class GameState:
    def __init__(self, players = ['amy', 'bob', 'cath'], map_size = 5, debug=False):
        self.game_map = Map(map_size)
        self.game_map.set_objects(len(players), debug)
        self.players = [Player(pl) for pl in players]
        self.player_bases = [PlayerBase(ba.x_location, ba.y_location) for ba in self.game_map.get_objects('player_base')]
        self.assign_players()
        self.mines = [Mine(min.x_location, min.y_location, min.resource) for min in self.game_map.get_objects('mine')]
        self.obstacles = [Obstacle(ob.x_location, ob.y_location, ob.passable) for ob in self.game_map.get_objects('obstacle')]

    def assign_players(self):
        for p, b in zip(self.players, self.player_bases):
            p.x_pos = b.x_location
            p.y_pos = b.y_location
            b.player = f'{p.name}_base'

    def update_state(self, activity_frame):
        current_positions = self.get_positional()


    def get_positional(self):
        return [[p.name, p.x_pos, p.y_pos] for p in self.players]

    def move_target(self, direction, player):
        if direction == 'n':
            player.y_pos -=1
        elif direction == 'e':
            player.x_pos += 1
        elif direction == 's':
            player.y_pos += 1
        elif direction == 'w':
            player.x_pos -=1
        elif direction == 's':
            return
        return None



