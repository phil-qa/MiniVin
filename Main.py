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
        self.player_bases = [PlayerBase(ba.x_position, ba.y_position) for ba in self.game_map.get_objects('player_base')]
        self.assign_players()
        self.mines = [Mine(min.x_position, min.y_position, name = min.name) for min in self.game_map.get_objects('mine')]
        self.obstacles = [Obstacle(ob.x_position, ob.y_position, ob.passable) for ob in self.game_map.get_objects('obstacle')]

    def assign_players(self):
        for player, base in zip(self.players, self.player_bases):
            player.set(base.x_position, base.y_position, 50)
            base.player = f'{player.name}_base'
        test = 'stop'

    def update_state(self, activity_frame):
        current_positions = self.get_positional()
        obstacle_tiles = [c.tile for c in self.obstacles]
        mine_tiles = [c.tile for c in self.mines]
        player_base_tiles = [c.tile for c in self.player_bases]

        next_state = self.determine_next_state(activity_frame)

        conflicts = {}

        #determine outcomes from interactions with the map objects
        for player, tile in next_state.items():
            if tile in obstacle_tiles:
                next_state[player] = player.tile
            elif tile in mine_tiles:
                if player.resource <5:
                    player.resource += 1
                next_state[player] = player.tile
            elif tile in player_base_tiles:
                if tile == player.base:
                    next_state[player] = tile
                else:
                    next_state[player]=player.tile
            for other_player, target_tile in next_state.items():
                if other_player != player:
                    if tile == target_tile:
                        conflicts.add(player, tile)
                        conflicts.add(other_player, target_tile)



        print('stop')

        '''        for player, activity in activity_frame.items():
            active_player = [pl for pl in self.players if pl.name == player][0]
            self.move_target(direction = activity, player = active_player)
            if active_player.x_pos < 0 or active_player.x_pos == self.map_size or active_player.y_pos <0 or active_player.y_pos == self.map_size:
                self.player_revert(active_player, current_positions)

            if active_player.coords in obstacle_coords:
                self.player_revert(active_player,current_positions)

            if active_player.coords in mine_coords:
                if active_player.resource < 5:
                    active_player.resource += 1
                self.player_revert(active_player, current_positions)'''

    def determine_next_state(self, activity_frame):
        moves = {}
        for player in self.players:
            moves[player] = player.next_tile(activity_frame[player.name])
        return moves



    def player_revert(self, player, original_positions):
        old_state = [pl for pl in original_positions if pl[0] == player.name][0]
        player.update_coords(old_state[1], old_state[2])


    def get_positional(self):
        return [[p.name, p.x_pos, p.y_pos] for p in self.players]

    def move_target(self, direction, player):
        player.move_player(direction)




