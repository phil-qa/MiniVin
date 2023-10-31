import unittest
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
        self.assertEqual(len(map.map_array), 4, "The map should be the same size as requtested")
        test_array = [symbol.symbol for symbol in map.map_array[0]]
        self.assertEqual([0, 0, 0, 0], test_array)

    def test_map_objects_initialise(self):

        map = Map(4)
        map.set_objects(players=4, debug=False)
        # tiles have been set correctly
        for y_line in map.map_array:
            for o in y_line:
                observable_object = map.get_object(o.x_position, o.y_position)
                self.assertEqual(observable_object.name, o.name,
                                 f'the map object at {o.x_position}{o.y_position} is not correct')
        # there are half the number of one dimension as a non movable name and the locations are not colliding
        self.assertEqual(self.count_specific_objects(map.map_array, ['o']), 2, "Failed to get blocking objects")
        blocking_objects = map.get_objects('obstacle')
        self.assertNotEqual(blocking_objects[0].coords, blocking_objects[1].coords,
                            "the blocking objects are glued together")
        for bo in blocking_objects:
            self.assertEqual(f'{bo.x_position}{bo.y_position}', bo.name)

        # there are 4 player spawn points
        self.assertEqual(self.count_specific_objects(map.map_array, ['b']), 4, "Failed to get player base objects")
        spawn_points = map.get_objects('player_base')
        for sp in spawn_points:
            self.assertEqual(f'{sp.x_position}{sp.y_position}', sp.name)

        # there are half the number of one dimension as gold mine locations
        self.assertEqual(self.count_specific_objects(map.map_array, ['m']), 2, "Failed to get mine objects")
        mines = map.get_objects('mine')
        for mine in mines:
            self.assertEqual(f'{mine.x_position}{mine.y_position}', mine.name)
        self.assertEqual(len(map.get_objects('player_base')), 4, "Failed to find the correct number of player bases")


if __name__ == '__main__':
    unittest.main()
