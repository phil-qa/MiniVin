import unittest
from Main import GameState
from Pathing import Pathing
import collections
collections.Callable = collections.abc.Callable
class PathTestModule(unittest.TestCase):
    def test_get_path(self):
        game_state, amy, bob, cathy = self.set_debug_game_state
        mine = game_state.mines[0]

        path_amy_to_mine1 = Pathing.find_path(amy.tile, mine.tile, game_state.game_map)
        # path request is not null
        self.assertIsNotNone(path_amy_to_mine1, 'No path objects returned from request amy to mine')
        # path does not go over an impassble object
        for tile in path_amy_to_mine1[1:-2]:
            x = int(tile[0])
            y = int(tile[1])
            object_at_location = game_state.game_map.get_tile(x, y)
            self.assertEqual(True, object_at_location.passable, f"stepped on a non passable square at {tile}")


    def test_translate_tile_direction(self):
        source_tile = '22'
        self.assertEqual('n', Pathing.convert_tile_transisiton_to_direction(source_tile,'21'))
        self.assertEqual('e', Pathing.convert_tile_transisiton_to_direction(source_tile, '32'))
        self.assertEqual('s', Pathing.convert_tile_transisiton_to_direction(source_tile, '23'))
        self.assertEqual('w', Pathing.convert_tile_transisiton_to_direction(source_tile, '12'))


    def test_pathing(self):
        game_state, amy, bob, cathy = self.set_debug_game_state

        path_cathy_to_bob = Pathing.find_path(cathy.tile, bob.tile, game_state.game_map)
        self.assertTrue(len(path_cathy_to_bob) > 0, 'The path from cathy to bob is not long enough')
        self.assertEqual('31', path_cathy_to_bob[0], 'The path from cathy to bob does not start at cathy')
        self.assertEqual('13', path_cathy_to_bob[-1], 'The path from cathy to bob does not end at bob')
        translated_path = Pathing.translate_path(path_cathy_to_bob)
        self.assertEqual('w', translated_path[0])
        self.assertEqual('s', translated_path[1])
        self.assertEqual('s', translated_path[2])
        self.assertEqual('w', translated_path[-1])

    def test_pathing_includes_obstacles(self):
        '''
        This test only shows that the pathing system does not care about obstacles, the caring about
        them should reside within a game state change. This is a SRP requirement
        '''
        game_state = GameState(debug=True)
        self.assertIsNotNone(game_state)
        amy = game_state.players[0]
        bob = game_state.players[1]
        cathy = game_state.players[2]

        path_bob_to_amy = Pathing.find_path(bob.tile, amy.tile, game_state.game_map)
        blocking_objects = [game_object.tile for game_object in game_state.game_map.game_tiles if game_object.passable == False]
        self.assertIsNotNone(path_bob_to_amy, "there should be a path from bon to amy")
        any_in_path = [path_item for path_item in path_bob_to_amy if path_item in blocking_objects]
        self.assertTrue (len(any_in_path)>0, msg=f"There should be some blocking objects but there are none")



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