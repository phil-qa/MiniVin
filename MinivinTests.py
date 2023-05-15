import unittest
import collections
collections.Callable = collections.abc.Callable
from Map import Map
from Player import Player
from Main import GameState

class MyTestCase(unittest.TestCase):
    def test_map_initialises(self):
        map = Map(4)
        self.assertEqual(len(map.map_array), 4)  # add assertion here
        test_array = [symbol.symbol for symbol in map.map_array[0]]
        self.assertEqual([0,0,0,0], test_array)

    def test_map_objects_initialise(self):

        map = Map(4)
        map.set_objects(players=4, debug=False)
        #there are half the number of one dimension as a non movable tile and the locations are not colliding
        self.assertEqual(self.count_specific_objects(map.map_array,['o']), 2, "Failed to get blocking objects")
        blocking_objects = map.get_objects('obstacle')
        self.assertNotEqual(blocking_objects[0].coords, blocking_objects[1].coords, "the blocking objects are glued together")
        #there are 4 player spawn points
        self.assertEqual(self.count_specific_objects(map.map_array,['b']),4, "Failed to get player base objects")
        #there are half the number of one dimension as gold mine locations
        self.assertEqual(self.count_specific_objects(map.map_array,['m']),2, "Failed to get mine objects")
        self.assertEqual(len(map.get_objects('player_base')),4, "Failed to find the correct number of player bases")

    def test_get_object_at_location(self):
        map = Map(4)
        map.set_objects(players=4, debug=True)
        single_object = map.get_object(0,0)
        self.assertIsNotNone(single_object)
        self.assertEqual(single_object.x_location,0)
        self.assertEqual(single_object.y_location, 0)

    '''
    player Tests 
    '''
    def test_player_initialises(self):
        player = Player("bob")
        self.assertIsNotNone(player)
        self.assertEqual("bob", player.name)

    def test_player_set(self):
        player = Player("bob")
        player.set(x_pos = 0, y_pos = 0, health = 30)
        self.assertEqual(0, player.x_pos)
        self.assertEqual(0, player.y_pos)
        self.assertEqual(30, player.health)
        self.assertEqual(30, player.max_health)
        self.assertEqual(0, player.resource)


    '''game sequence tests'''
    def test_game_state_initialises(self):
        '''#given a game startup with four players
        #when the game initialises
        #then the map shall be generated
        and the players shall be creates
        and the state objects shall be created
        and the players shall be at their bases

        '''

        game_state = GameState(players=['amy', 'bob', 'cath', 'don'], map_size=8)
        self.assertIsNotNone(game_state.game_map, "Map not initialised")
        self.assertEqual(len(game_state.players), 4, "Number of players incorrect")
        self.assertEqual(len(game_state.mines), 4, "Number of mines incorrect")
        self.assertEqual(len(game_state.obstacles), 4, "Number of obstacles incorrect")
        self.assertEqual(len(game_state.player_bases), 4, "Number of bases incorrect")
        self.assertEqual(game_state.players[0].x_pos, game_state.player_bases[0].x_location)
        self.assertEqual(game_state.players[0].y_pos, game_state.player_bases[0].y_location)

    def test_motion_events(self):
        '''
        given an initialised map
        when a player moves
        then the gamestate understands the response on target
         01234
        0*****
        1*a*b*
        2*m.**
        3*c***
        4*****
        '''
        game_state = GameState(debug=True)
        self.assertIsNotNone(game_state)
        amy = game_state.players[0]
        bob = game_state.players[1]
        cathy = game_state.players[2]

        starting_positions = game_state.players.copy()
        #players move on update
        game_state.update_state({f'{amy.name}' : 'e', f'{bob.name}' : 'n', f'{cathy.name}': 's'})
        self.assertEqual([amy.x_pos, amy.y_pos], [2,1], "Amy isnt in the right place")




    def count_specific_objects(self, nested_list, target_object):
        count = 0
        for item in nested_list:
            if isinstance(item, list):
                for target in target_object:
                    count += self.count_specific_objects(item, target)  # Recursively count objects in nested list
            elif item.symbol == target_object:
                count += 1  # Increment count for matching object
        return count



if __name__ == '__main__':
    unittest.main()
