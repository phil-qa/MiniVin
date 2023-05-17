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

        given a move state
        the players shall move according to the direction unless when the play7er attempts to move :
        there is an obstacle, the player will remain at location
        there is a mine, the player will mine a resource to a max of 5 times
        there is a map edge, the player will remain at location
        there is antother player base, the player will renmain at location
        there is a player base, the player shall move to it and hand over resources and have moves refreshed

        '''

        game_state = GameState(players=['amy', 'bob', 'cath', 'don'], map_size=8)
        self.assertIsNotNone(game_state.game_map, "Map not initialised")
        self.assertEqual(len(game_state.players), 4, "Number of players incorrect")
        for player in game_state.players:
            self.assertIsNotNone(player.coords, f"player {player.name} has not got coordinates set")
        self.assertEqual(len(game_state.mines), 4, "Number of mines incorrect")
        for mine in game_state.mines:
            self.assertIsNotNone(mine.coords, f"a mine has no coordinates")
        self.assertEqual(len(game_state.obstacles), 4, "Number of obstacles incorrect")
        for obstacle in game_state.obstacles:
            self.assertIsNotNone(obstacle.coords)
        self.assertEqual(len(game_state.player_bases), 4, "Number of bases incorrect")
        for base in game_state.player_bases:
            self.assertIsNotNone(base.coords)
        self.assertEqual(game_state.players[0].x_pos, game_state.player_bases[0].x_location)
        self.assertEqual(game_state.players[0].y_pos, game_state.player_bases[0].y_location)

    def test_motion_events(self):
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
        game_state = GameState(debug=True)
        self.assertIsNotNone(game_state)
        amy = game_state.players[0]
        bob = game_state.players[1]
        cathy = game_state.players[2]

        starting_positions = game_state.players.copy()

        self.assertEqual([1, 1], amy.coords, "Amy isnt in the right start point")
        self.assertEqual([1, 3], bob.coords, "bob inst in the right start point")
        self.assertEqual([3, 1], cathy.coords, "cathy isnt in the right start point ")
        # players move on update

        game_state.update_state({f'{amy.name}': 'e', f'{bob.name}': 'w', f'{cathy.name}': 's'})

        self.assertEqual([2, 1], amy.coords, "Amy isnt in the right place")
        self.assertEqual([0, 3], [bob.x_pos, bob.y_pos], "Bob isnt in the right place")
        self.assertEqual([3, 2], [cathy.x_pos, cathy.y_pos], "Cathy isnt in the right place")

        # players cant go over the map edges

        game_state.update_state({f'{amy.name}': 'n', f'{bob.name}': 'w', f'{cathy.name}': 'e'})

        self.assertEqual([2, 0], amy.coords, "Amy isnt in the right place")
        self.assertEqual([0, 3], [bob.x_pos, bob.y_pos], "Bob isnt in the right place")
        self.assertEqual([4, 2], [cathy.x_pos, cathy.y_pos], "Cathy isnt in the right place")

        game_state.update_state({f'{amy.name}': 'n', f'{bob.name}': 's', f'{cathy.name}': 'e'})

        self.assertEqual([2, 0], amy.coords, "Amy isnt in the right place")
        self.assertEqual([0, 4], [bob.x_pos, bob.y_pos], "Bob isnt in the right place")
        self.assertEqual([4, 2], [cathy.x_pos, cathy.y_pos], "Cathy isnt in the right place")

        # players cant go onto an obstacle at [2,2]

        game_state.update_state({f'{amy.name}': 's', f'{bob.name}': 'h', f'{cathy.name}': 'h'})

        self.assertEqual([2, 1], [amy.x_pos, amy.y_pos], "Amy isnt in the right place")
        self.assertEqual([0, 4], [bob.x_pos, bob.y_pos], "Bob isnt in the right place")
        self.assertEqual([4, 2], [cathy.x_pos, cathy.y_pos], "Cathy isnt in the right place")

        game_state.update_state({f'{amy.name}': 's', f'{bob.name}': 'h', f'{cathy.name}': 'h'})

        self.assertEqual([2, 1], [amy.x_pos, amy.y_pos], "Amy isnt in the right place")
        self.assertEqual([0, 4], [bob.x_pos, bob.y_pos], "Bob isnt in the right place")
        self.assertEqual([4, 2], [cathy.x_pos, cathy.y_pos], "Cathy isnt in the right place")

        # # player approaching a mine tile does not move

        game_state.update_state({f'{amy.name}': 'w', f'{bob.name}': 'h', f'{cathy.name}': 'h'})
        game_state.update_state({f'{amy.name}': 's', f'{bob.name}': 'h', f'{cathy.name}': 'h'})

        self.assertEqual([1, 1], [amy.x_pos, amy.y_pos], "Amy isnt in the right place")
        self.assertEqual([0, 4], [bob.x_pos, bob.y_pos], "Bob isnt in the right place")
        self.assertEqual([4, 2], [cathy.x_pos, cathy.y_pos], "Cathy isnt in the right place")

        # a player that has approached a mine tile has harvested one coin
        self.assertEqual(1, amy.resource, "amy  didnt get a coin")

        # a player can only mine five coins
        game_state.update_state({f'{amy.name}': 's', f'{bob.name}': 'h', f'{cathy.name}': 'h'})
        game_state.update_state({f'{amy.name}': 's', f'{bob.name}': 'h', f'{cathy.name}': 'h'})
        game_state.update_state({f'{amy.name}': 's', f'{bob.name}': 'h', f'{cathy.name}': 'h'})
        game_state.update_state({f'{amy.name}': 's', f'{bob.name}': 'h', f'{cathy.name}': 'h'})
        game_state.update_state({f'{amy.name}': 's', f'{bob.name}': 'h', f'{cathy.name}': 'h'})

        self.assertEqual(5, amy.resource, "amys got an odd amount of coins")




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
