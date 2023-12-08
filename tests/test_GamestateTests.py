import unittest

from Main import GameState

class GameStateModuleTests(unittest.TestCase):

    def test_game_state_initialises(self):
        '''#given a game startup with four players
        #when the game initialises
        #then the map shall be generated
        and the players shall be creates
        and the state objects shall be created
        and the players shall be at their bases

        given a move state
        the players shall move according to the direction unless when the play7er attempts to move :
        there is an obstacle, the player will remain at location
        there is a mine, the player will mine a resource to a max of 5 times
        there is a map edge, the player will remain at location
        there is another player base, the player will renmain at location
        there is a player base, the player shall move to it and hand over resources and have moves refreshed

        '''
        #normal game start, randomised elements
        self.game_state = GameState(players=['amy', 'bob', 'cath', 'don'], map_size=8)
        self.assertIsNotNone(self.game_state.game_map, "Map not initialised")
        self.assertEqual(len(self.game_state.players), 4, "Number of players incorrect")
        for player in self.game_state.players:
            self.assertIsNotNone(player.coords, f"player {player.name} has not got coordinates set")
        self.assertEqual(len(self.game_state.mines), 4, "Number of mines incorrect")
        for mine in self.game_state.mines:
            self.assertIsNotNone(mine.coords, f"a mine has no coordinates")
        self.assertEqual(len(self.game_state.obstacles), 4, "Number of obstacles incorrect")
        for obstacle in self.game_state.obstacles:
            self.assertIsNotNone(obstacle.coords)
        self.assertEqual(len(self.game_state.player_bases), 4, "Number of bases incorrect")
        for base in self.game_state.player_bases:
            self.assertIsNotNone(base.coords)

        test_player = self.game_state.players[0]
        test_base = self.game_state.player_bases[0]
        self.assertEqual(test_player.x_position, test_base.x_position)
        self.assertEqual(test_player.y_position, test_base.y_position)
        self.assertEqual(1,len( self.game_state.game_map.get_tile(test_base.x_position, test_base.y_position).players_on_tile ))
        stop = 'stop'


    def test_game_state_events(self):
        '''
        given an initialised map
        when a player moves
        then the gamestate understands the response on target
         01234
        0*****
        1*a*c*
        2*m.**
        3*b***
        4***m*
        '''

        game_state, amy, bob, cathy = self.set_debug_game_state
        starting_positions = game_state.players.copy()
        #the initial state is correct
        self.initial_state_positions(game_state, amy, bob, cathy)

        #test that the state can be changed with a simple string entry for each player
        game_state.update_state({f'{amy.name}': 'e', f'{bob.name}': 'w', f'{cathy.name}': 's'})

        self.confirm_changes_from_simple_input(game_state, amy, bob, cathy)

        #move again
        game_state.update_state({f'{amy.name}': 'n', f'{bob.name}': 'w', f'{cathy.name}': 'e'})
        self.confirm_positions_after_second_move(game_state, amy, bob,cathy)

        # cathy is at the edge and should not be able to move over it
        game_state.update_state({f'{amy.name}': 'n', f'{bob.name}': 's', f'{cathy.name}': 'e'})
        self.confirm_positions_after_third_move(game_state, amy, bob, cathy)

        # try to move onto an obstacle and cant
        game_state.update_state({f'{amy.name}': 's', f'{bob.name}': 'h', f'{cathy.name}': 'h'})
        game_state.update_state({f'{amy.name}': 's', f'{bob.name}': 'h', f'{cathy.name}': 'h'})
        self.confirm_player_cant_move_over_obstacle(game_state,amy,bob,cathy)

        #test a mine stops movement
        game_state.update_state({f'{amy.name}': 'w', f'{bob.name}': 'h', f'{cathy.name}': 'h'})
        game_state.update_state({f'{amy.name}': 's', f'{bob.name}': 'h', f'{cathy.name}': 'h'})
        self.a_player_cant_move_onto_a_mine(game_state, amy, bob, cathy)

        #test maximum mine is 5 coins
        game_state.update_state({f'{amy.name}': 's', f'{bob.name}': 'h', f'{cathy.name}': 'h'})
        game_state.update_state({f'{amy.name}': 's', f'{bob.name}': 'h', f'{cathy.name}': 'h'})
        game_state.update_state({f'{amy.name}': 's', f'{bob.name}': 'h', f'{cathy.name}': 'h'})
        game_state.update_state({f'{amy.name}': 's', f'{bob.name}': 'h', f'{cathy.name}': 'h'})
        game_state.update_state({f'{amy.name}': 's', f'{bob.name}': 'h', f'{cathy.name}': 'h'})
        self.a_player_can_only_mine_5_coins(game_state,amy, bob, cathy)

        #test conflicts
        # a player assaulting another has an advantage
        # move bob 0,4 to amy 1,1 - update amy needs to move because shes in her base
        original_gamestate = game_state
        game_state.update_state({f'{amy.name}': 'w', f'{bob.name}': 'n', f'{cathy.name}': 'n'}) # bob to 0 3 cathy to 0 0 amy to 0 1
        game_state.update_state({f'{amy.name}': 'h', f'{bob.name}': 'n', f'{cathy.name}': 'h'})  # bob to 0 2
        game_state.update_state({f'{amy.name}': 'h', f'{bob.name}': 'n', f'{cathy.name}': 'h'})  # bob to 0 1 attacks amy
        self.a_player_conflict_resolves(original_gamestate, game_state)



    def initial_state_positions(self, state_data, amy, bob, cathy):
        self.assertEqual([1, 1], amy.coords, "Amy isnt in the right start point")
        self.assertEqual('11', amy.tile, "Tile for amy isnt right")
        self.assertEqual([1, 3], bob.coords, "bob isnt in the right start point")
        self.assertEqual('13', bob.tile, "Bobs name is not at the right place")
        self.assertEqual([3, 1], cathy.coords, "cathy isnt in the right start point ")
        self.assertEqual('31', cathy.tile, "Tile for cathy isnt right")

    def confirm_changes_from_simple_input(self, state_data,amy, bob, cathy):
        #note that cathy tries to move into a mine and this rejects the motion.
        self.assertEqual([2, 1], amy.coords, "Amy isnt in the right place")
        self.assertEqual('21', amy.tile, "Tile for amy isnt right")
        self.assertEqual([0, 3], [bob.x_position, bob.y_position], "Bob isnt in the right place")
        self.assertEqual('03', bob.tile, "Tile for bob isnt right")
        self.assertEqual([3, 1], [cathy.x_position, cathy.y_position], "Cathy isnt in the right place")
        self.assertEqual('31', cathy.tile, "Tile for cathy isnt right")
        tile_cathy_is_on = state_data.game_map.get_tile(cathy.x_position,cathy.y_position)
        self.assertEqual(1,len(tile_cathy_is_on.players_on_tile),"there should be at least one player on the tile")

    def confirm_positions_after_second_move(self, state_data, amy, bob, cathy):
        print('testing the second move')
        self.assertEqual([2, 0], amy.coords, "Amy isnt in the right place")
        self.assertEqual([0, 3], [bob.x_position, bob.y_position], "Bob isnt in the right place")
        self.assertEqual([4, 1], [cathy.x_position, cathy.y_position], "Cathy isnt in the right place")

    def confirm_positions_after_third_move(self, state_data, amy, bob, cathy):
        self.assertEqual([2, 0], amy.coords, "Amy isnt in the right place")
        self.assertEqual([0, 4], [bob.x_position, bob.y_position], "Bob isnt in the right place")
        self.assertEqual([4, 1], [cathy.x_position, cathy.y_position], "Cathy isnt in the right place")

    def confirm_player_cant_move_over_obstacle(self, state_data, amy, bob, cathy):
        self.assertEqual([2, 1], [amy.x_position, amy.y_position], "Amy tried to move into an obstacle at 2,2 she should not be there")
        self.assertEqual([0, 4], [bob.x_position, bob.y_position], "Bob isnt in the right place")
        self.assertEqual([4, 1], [cathy.x_position, cathy.y_position], "Cathy isnt in the right place")

    def a_player_cant_move_onto_a_mine(self, game_state, amy, bob, cathy):
        self.assertEqual([1, 1], [amy.x_position, amy.y_position], "Amy isnt in the right place")
        self.assertEqual('11', amy.tile, "Tile for amy isnt right")
        self.assertEqual([0, 4], [bob.x_position, bob.y_position], "Bob isnt in the right place")
        self.assertEqual([4, 1], [cathy.x_position, cathy.y_position], "Cathy isnt in the right place")
        self.assertEqual(1, amy.resource, "amy  didnt get a coin")

    def a_player_can_only_mine_5_coins(self, game_state, amy, bob, cathy):
        self.assertEqual(5, amy.resource, "amys got an odd amount of coins")

    #conflicts
    def a_player_conflict_resolves(self, original_game_state, new_gamestate):
        original_players = original_game_state.players
        new_players = new_gamestate.players
        original_amy = self.get_player('amy',original_players)
        new_amy = self.get_player('amy', new_players)
        original_bob = self.get_player('bob', original_players)
        new_bob = self.get_player('bob', new_players)
        self.assertNotEqual(original_amy.health, new_amy.health)


    @property
    def set_debug_game_state(self):
        object_array = [GameState(debug=True)]

        object_array.append(object_array[0].players[0])
        object_array.append(object_array[0].players[1])
        object_array.append(object_array[0].players[2])
        game_state = object_array[0]
        amy = object_array[1]
        bob = object_array[2]
        cathy = object_array[3]
        return game_state, amy, bob, cathy


    def get_player(self, name, player_array):
        return [player for player in player_array if player.name == name][0]