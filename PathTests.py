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