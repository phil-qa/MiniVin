import unittest


from GameTile import GameTile
from Map import Map

class MapTestModule(unittest.TestCase):
    def test_map_initialises(self):
        '''
        Given a map
        When it is initialised
        Then the map consists of tiles according to the size requested
            And they are empty
            And there are no players assigned
        :return:
        '''
        map = Map(4)
        self.assertEqual(len(map.game_tile_map), 4, "The map should be the same size as requested")
        self.assertTrue(all(isinstance(tile,GameTile) for tile in map.game_tile_map[0]), f"The map should consist of game tiles, {type(map.game_tile_map[0][0])}")
        test_array = [symbol.symbol for symbol in map.game_tile_map[0]]
        self.assertEqual([0, 0, 0, 0], test_array)

    def test_map_objects_initialise(self):
        '''
        Given a blank map
        When it is initialised with map elements
        Then the map objects are updated to the game tiles
            and the players are added to tiles
        :return:
        '''
        map_size = 5
        map = Map(map_size)


        for debug in [True, False]:
            map.set_objects(players=4, debug=debug)
            print("Running in debug" if debug else "Runing non debug")
            # tiles have been set correctly according to get tile
            self.assertEqual(len(map.game_tiles), map_size**2, f"The number of game tiles shoud be {map_size**2}")
            map_objects = {}
            map_objects['obstacles'] = map.get_tiles_by_type('obstacle')
            map_objects['mines'] = map.get_tiles_by_type('mine')
            map_objects['player_bases'] = map.get_tiles_by_type('player_base')
            if debug:
                #Are the number of obstacles what we expect
                self.assertEqual(len(map_objects['obstacles']),1,"The number of obstacles is incorrect")
                #Are the number of mines correct
                self.assertEqual(len(map_objects['mines']), 2, "the number of mines is unexpected")
                #Are the number of player bases correct
                self.assertEqual(len(map_objects['player_bases']), 4, "the number of player bases is unexpected")
            else:
                # there are half the number of one dimension as a non-movable name and the locations are not colliding
                self.assertEqual(len(map_objects['obstacles']), map_size / 2, "Failed to get all blocking objects in non debug")
                 # check blocking objects dont collide
                if(len(map_objects['obstacles'])>1):
                    tile_values = [obstacle.tile for obstacle in map_objects['obstacles'].values()]
                    unique_tile_values = set(tile_values)
                    self.assertFalse(len(unique_tile_values) != len(tile_values), "there are some obstacles stuck together ")


            for tiles_on_line in map.game_tile_map:
                for tile in tiles_on_line:
                    observed_tile = map.get_tile(tile.x_position, tile.y_position)
                    self.assertEqual(observed_tile.name, tile.name,
                                     f'the map object at {tile.x_position}{tile.y_position} is not correct')

            blocking_objects = map.get_objects('obstacle')
            self.assertNotEqual(blocking_objects[0].coords, blocking_objects[1].coords,
                                "the blocking objects are glued together")
            for bo in blocking_objects:
                self.assertEqual(f'{bo.x_position}{bo.y_position}', bo.name)

            # there are 4 player spawn points
            self.assertEqual(self.count_specific_objects(map.game_tile_map, ['b']), 4, "Failed to get player base objects")
            spawn_points = map.get_objects('player_base')
            for sp in spawn_points:
                self.assertEqual(f'{sp.x_position}{sp.y_position}', sp.name)

            # there are half the number of one dimension as gold mine locations
            self.assertEqual(self.count_specific_objects(map.game_tile_map, ['m']), 2, "Failed to get mine objects")
            mines = map.get_objects('mine')
            for mine in mines:
                self.assertEqual(f'{mine.x_position}{mine.y_position}', mine.name)
            self.assertEqual(len(map.get_objects('player_base')), 4, "Failed to find the correct number of player bases")


if __name__ == '__main__':
    unittest.main()
