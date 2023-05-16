from Map import Map
from Mine import Mine
from Obstacle import Obstacle
from Player import Player
from PlayerBase import PlayerBase


class GameState:
    def __init__(self, players = ['amy', 'bob', 'cath'], map_size = 5, debug=False):
        self.map_size = map_size
        self.game_map = Map(map_size)
        self.game_map.set_objects(len(players), debug)
        self.players = [Player(pl) for pl in players]
        self.player_bases = [PlayerBase(ba.x_location, ba.y_location) for ba in self.game_map.get_objects('player_base')]
        self.assign_players()
        self.mines = [Mine(min.x_location, min.y_location, min.resource) for min in self.game_map.get_objects('mine')]
        self.obstacles = [Obstacle(ob.x_location, ob.y_location, ob.passable) for ob in self.game_map.get_objects('obstacle')]

    def assign_players(self):
        for player, base in zip(self.players, self.player_bases):
            player.x_pos = base.x_location
            player.y_pos = base.y_location
            base.player = f'{player.name}_base'
        test = 'stop'

    def update_state(self, activity_frame):
        current_positions = self.get_positional()
        for player, activity in activity_frame.items():
            active_player = [pl for pl in self.players if pl.name == player][0]
            self.move_target(direction = activity, player = active_player)
            if active_player.x_pos < 0 or active_player.x_pos == self.map_size or active_player.y_pos <0 or active_player.y_pos == self.map_size:
                self.player_revert(active_player, current_positions)


            obstacles = [c.coords for c in self.game_map.get_objects('obstacle')]

            if active_player.coords in obstacles:
                print(f"player {active_player.name}, it obstacle at {[c for c in obstacles if c == active_player.coords]}")
                self.player_revert(active_player,current_positions)

    def player_revert(self, player, original_positions):
        old_state = [pl for pl in original_positions if pl[0] == player.name][0]
        player.x_pos = old_state[1]
        player.y_pos = old_state[2]

    def get_positional(self):
        return [[p.name, p.x_pos, p.y_pos] for p in self.players]

    def move_target(self, direction, player):
        player.move_player(direction)




