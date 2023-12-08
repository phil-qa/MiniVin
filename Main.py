import random



from Map import Map
from Mine import Mine
from Obstacle import Obstacle
from Player import Player
from PlayerBase import PlayerBase


class GameState:
    def __init__(self, players = ['amy', 'bob', 'cath'], map_size = 5, debug=False):
        self.map_size = map_size
        self.game_map = Map(map_size)
        self.viz_map = [[0 for x in range(map_size)] for y in range(map_size) ]
        self.game_map.set_objects(len(players), debug)
        self.players = [Player(pl) for pl in players]
        self.player_bases = [PlayerBase(ba.x_position, ba.y_position) for ba in self.game_map.get_objects('player_base')]
        self.assign_players()
        # at this point the map is set up

        self.mines = [Mine(min.x_position, min.y_position, name = min.name) for min in self.game_map.get_objects('mine')]
        self.obstacles = [Obstacle(ob.x_position, ob.y_position, ob.passable) for ob in self.game_map.get_objects('obstacle')]
        self.all_game_objects =[]

        self.all_game_objects.extend(self.players)
        self.all_game_objects.extend(self.mines)
        self.all_game_objects.extend(self.player_bases)
        self.all_game_objects.extend(self.obstacles)
        self._update_player_locations()
        self._update_viz_map()

    def assign_players(self):
        '''
        assignes the players that the session was initialised with to bases.
        :return:
        '''
        for player, base in zip(self.players, self.player_bases):
            player.set(base.x_position, base.y_position, 50)

            base.player = player.name
            base.name = f'{player.name}_base'


    def update_state(self, activity_frame):
        current_positions = self.get_positional()
        obstacle_tiles = {c.name for c in self.obstacles}
        mine_tiles = [c.tile for c in self.mines]
        player_base_tiles = [c.name for c in self.player_bases]

        conflicts, next_state = self.resolve_next_state(activity_frame)

        #resolve conflicts
        #players in fight
        conflict_tiles = set(conflicts.values())
        for conflict_tile in conflict_tiles:
            player_set = [p.key for p in conflicts if p.value == conflict_tile ]
            while any(p.health != 1 for p in player_set):
                fight_outcomes = {}
                for fighter in player_set:
                    fight_outcomes.append({fighter, random.randint(1,10)})
                highest = {fighter for fighter in fight_outcomes if fighter[1] == max([value[1] for value in fight_outcomes ])}
                all = {p for p in player_set}
                losers = all - highest
                for loser in losers:
                    loser.health -= 1
        # send losers back to their bases

        for player in next_state.keys():
            if player.health == 1:
                next_state[player] = player.return_to_base()

        for player in next_state.keys():
            player.move_player(next_state[player])
        self._update_visual_map(self.players,True)


    def resolve_next_state(self, activity_frame):
        '''

        :param activity_frame: dictionary of player names and their next move
        :param mine_tiles: dictionary of mines and their tiles
        :param obstacle_tiles: dictionary of the obstacles and their tiles
        :param player_base_tiles: dictionary of the player bases
        :return:
        '''
        next_state = self.determine_next_state(activity_frame)
        conflicts = {}
        # determine outcomes from interactions with the map objects, get each current_player and where they are going
        for current_player, next_tile in next_state.items():
            # If the proposed move is outside the map bounds the current_player stays the same
            if '-' in next_tile:
                next_state[current_player] = current_player.tile
            out_of_bounds_rule = int(next_state[current_player][0]) > self.map_size - 1 or int(next_state[current_player][1]) > self.map_size - 1
            if out_of_bounds_rule:
                next_state[current_player] = current_player.tile

            #if the next next_tile is in the obstacles then the current_player stops
            elif next_tile in [obstacle.tile for obstacle in  self.obstacles]:
                next_state[current_player] = current_player.tile

            # If next name is a mine name, current_player stays in the same place and gets a coin
            elif next_tile in [mine_tile.tile for mine_tile in self.mines]:
                if current_player.resource < 5:
                    current_player.resource += 1
                next_state[current_player] = current_player.tile

            # if the next name is the current_player base go to it if not stay
            elif next_tile in [player_base.tile for player_base in self.player_bases]:
                if next_tile == current_player.base:
                    next_state[current_player] = next_tile
                else:
                    next_state[current_player] = current_player.tile

        # after all the future states have been determined, run a conflict check
        distinct_values = set(next_state.values()) #distinct values derives from the tiles that the players are moving to or in
        if len(distinct_values) < len(activity_frame): #if the distinct values in the next stte is less than the number of players then there is a conflict
            players_jn_conflict = [[player for player, tile in next_state.items() if player.tile == active_tile] for active_tile in distinct_values]
            for conflict_set in players_jn_conflict:
                while len([player_with_health for player_with_health in conflict_set if player_with_health.health > 1 ]) >1 :
                    conflict_set = self.resolve_conflict(conflict_set)



        for other_player, target_tile in next_state.items(): # is there a collision with the other current_player then conflict
            if other_player != current_player:
                if next_tile == target_tile:
                    if current_player not in conflicts.keys():
                        conflicts[current_player] = next_tile
                    if other_player not in conflicts.keys():
                        conflicts[other_player] = target_tile
        return conflicts, next_state

    def determine_next_state(self, activity_frame):
        """
        determines the next move tile for each player based off the activity frame values
        :param activity_frame: dictionary of the player names and their requested moves
        :return: dictionary of players and their next move tile
        """
        moves = {}
        for player in self.players:
            moves[player] = player.next_tile(activity_frame[player.name])
        return moves



    def player_revert(self, player, original_positions):
        old_state = [pl for pl in original_positions if pl[0] == player.name][0]
        player.update_coords(old_state[1], old_state[2])


    def get_positional(self):
        return [[p.name, p.tile] for p in self.players]

    def move_target(self, direction, player):
        player.move_player(direction)

    def resolve_conflict(self,players):
        fighters = [player for player in players if player.health > 1]
        random_fight_values = [random.randint(1,100) for fighter in fighters]
        winner = players[max( (v, i) for i, v in enumerate(random_fight_values) )[1]]
        for loser in players :
            if loser != winner:
                loser.health -=1
        return players

    def _update_viz_map(self):
        for map_object in self.all_game_objects:
            
            self.viz_map[map_object.y_position][map_object.x_position]=map_object.name

    def _update_player_locations(self):
        '''
        update the tile player positions arrays.
        '''
        # clear all current player positions
        for game_tile in self.game_map.game_tiles:
            game_tile.players_on_tile = []
        for player in self.players:
            active_tile = [tile for tile in self.game_map.game_tiles if tile.tile == player.tile][0]
            active_tile.players_on_tile.append(player.name)


    def _update_visual_map(self, players, debug):
        self.visual_map = ''
        map_size = self.game_map.size
        for row in range(map_size):
            build = ''
            for column in range(map_size):
                object_name = self.game_map.game_tile_map[column][row].symbol
                build += object_name
                players_on_tile = [p for p in players if p.tile == f"{column}{row}"]
                if len(players_on_tile) > 0:
                    build = ''
                    for p in players_on_tile:
                        build += p.symbol
                build+="\t"
            self.visual_map+=build
            if debug:
                print (build)



