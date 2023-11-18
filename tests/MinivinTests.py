import unittest
import collections
collections.Callable = collections.abc.Callable

from Player import Player
from Main import GameState
from Pathing import Pathing

class MyTestCase(unittest.TestCase):
    '''
    Map tests
    The map should initialise
    The map objects shall be placed
    The map class shall have a path tool
    '''

    def test_get_object_by_tile(self):
        game_state, amy, bob, cathy = self.set_debug_game_state()
        mine = game_state.game_map.get_tile_object('12')
        amy_position = game_state.game_map.get_tile_object(amy.name)
        obstacle = game_state.game_map.get_tile_object('22')
        self.assertTrue(mine.name == 'mine')
        self.assertTrue(amy_position.name == 'amy')
        self.assertTrue(obstacle.name == 'obstacle')



        # assert direction steps






    '''game sequence tests'''

    #TODO finish up conflict tests
    def test_conflict_states(self):
        game_state = GameState(debug=True)
        self.assertIsNotNone(game_state)
        amy = game_state.players[0]
        bob = game_state.players[1]
        cathy = game_state.players[2]
        game_state.update_state({f'{amy.name}': 'n', f'{bob.name}': 'h', f'{cathy.name}': 'h'})
        game_state.update_state({f'{amy.name}': 'e', f'{bob.name}': 'h', f'{cathy.name}': 'h'})
        self.assertEqual('20', amy.tile, 'Amy is not in the right place in  path block tests')



        # a player fights
        #move amy to a fight place
        game_state.update_state({f'{amy.name}': 'n', f'{bob.name}': 'h', f'{cathy.name}': 'h'}) #amy tries to go north but cannot
        game_state.update_state({f'{amy.name}': 'e', f'{bob.name}': 'h', f'{cathy.name}': 'h'})
        self.assertEqual('30', amy.tile, 'Amy is not in the right place in  conflict tests')
        path_bob_to_amy = Pathing.find_path(bob.tile, amy.tile, game_state.game_map)
        bobs_path = Pathing.translate_path(path_bob_to_amy)
        amy.health = 10  # cripple amy

        for move in bobs_path:
            game_state.update_state({f'{amy.name}': 'h', f'{bob.name}': move, f'{cathy.name}': 'h'})


        #keeping bob the same health
        bobs_health = bob.health + 1
        # player collision
        self.assertNotEqual(bob.name, amy.name)
        # after the fight amy should have only one health and amy should be at the previous name and bob should have a
        # reduction in health and be in amys place
        self.assertEqual(1, amy.health or bob.health)
        self.assertEqual('10', amy.name)
        self.assertEqual('20', bob.name)
        self.assertLess(bobs_health, bob.health)


    def count_specific_objects(self, nested_list, target_object):
        count = 0
        for item in nested_list:
            if isinstance(item, list):
                for target in target_object:
                    count += self.count_specific_objects(item, target)  # Recursively count objects in nested list
            elif item.symbol == target_object:
                count += 1  # Increment count for matching object
        return count

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

if __name__ == '__main__':
    unittest.main()
