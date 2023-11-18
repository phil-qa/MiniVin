import unittest
from math import ceil

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
        self.assertEqual(['em', 'em', 'em', 'em'], test_array)

    def test_map_objects_initialise(self):
        '''
        Given a blank map
        When it is initialised with map elements
        Then the map objects are updated to the game tiles
            and the players are added to tiles
        :return:
        '''




        for debug in [True, False]:
            map_size = 5
            map = Map(map_size)
            number_players_in_free_test = [4]
            map.set_objects(players=number_players_in_free_test[0], debug=debug)
            print("Running in debug" if debug else "Runing non debug")

            # tiles have been set correctly according to get tile
            self.assertEqual(len(map.game_tiles), map_size**2, f"The number of game tiles shoud be {map_size**2}")
            map_objects = {}
            map_objects['obstacles'] = map.get_tiles_by_type('obstacle')
            obstacle_count = len(map_objects['obstacles'])
            map_objects['mines'] = map.get_tiles_by_type('mine')
            mine_count = len(map_objects['mines'])
            map_objects['player_bases'] = map.get_tiles_by_type('player_base')
            player_base_count = len(map_objects['player_bases'])
            map_objects['empty'] = map.get_tiles_by_type('empty')
            empty_tiles_count = len(map_objects['empty'])
            print_map(map)
            if debug:
                #Given we have an explicit state then confirm the map draws in the way we wish
                #Are the number of obstacles what we expect
                self.assertEqual(obstacle_count , 1,"The number of obstacles is incorrect")
                #Are the number of mines correct
                self.assertEqual(mine_count, 2, "the number of mines is unexpected")
                #Are the number of player bases correct
                self.assertEqual(player_base_count, 4, "the number of player bases is unexpected")
                self.assertEqual(empty_tiles_count, map_size ** 2 - (obstacle_count + mine_count + player_base_count), "The number of empty tiles is incorrect in debug")
                self.check_literal_naming(empty_tiles_count, map, mine_count, obstacle_count, player_base_count)
            else:
                # there are half the number of one dimension as a non-movable name and the locations are not colliding
                self.assertEqual(len(map_objects['obstacles']), ceil(map_size / 2), "Failed to get all blocking objects in non debug")
                self.assertEqual(len(map_objects['mines']), ceil(map_size /2), "Faied to find all mines")
                # there are half the number of one dimension as gold mine locations
                self.assertEqual(mine_count, ceil(map_size/2), "Failed to get mine objects")

                #verify mine positions
                mines = map.get_objects('mine')
                for mine in mines:
                    self.assertEqual(f'{mine.x_position}{mine.y_position}', mine.tile)

            self.overlap_check(map)



            # the  number of spawn points is equal to the number of players
            self.assertEqual(player_base_count, number_players_in_free_test[0], "Failed to get player base objects")
            spawn_points = map.get_objects('player_base')
            for sp in spawn_points:
                self.assertEqual(f'{sp.x_position}{sp.y_position}', sp.tile)



    def check_literal_naming(self, empty_tiles_count, map, mine_count, obstacle_count, player_base_count):
        # are the tile names correct the naming convention should be typecount
        empty_iterator = empty_tiles_count
        mine_iterator = mine_count
        player_base_iterator = player_base_count
        obstacle_iterator = obstacle_count
        for tiles_on_line in map.game_tile_map:
            for tile in tiles_on_line:
                tile_type = tile.type
                if tile_type == 'obstacle':
                    self.assertEqual(tile.name, f'obstacle{obstacle_count - obstacle_iterator}',
                                     f'incorrect identifier of obstacle {tile.name}, at {tile.tile}')
                    obstacle_iterator -= 1
                elif tile_type == 'mine':
                    self.assertEqual(tile.name, f'mine{mine_count - mine_iterator}',
                                     f'incorrect identifier of mine {tile.name}, at {tile.tile}')
                    mine_iterator -= 1
                elif tile_type == 'player_base':
                    self.assertEqual(tile.name, f'player_base{player_base_count - player_base_iterator}',
                                     f'incorrect identifier of player_base {tile.name}, at {tile.tile}')
                    player_base_iterator -= 1

    def overlap_check(self, map):
        objects = ['mines', 'obstacles', 'player_bases']
        for object in objects:
            tile_values = [mine.tile for mine in map.get_tiles_by_type(object)]
            unique_tile_values = set(tile_values)
            self.assertFalse(len(unique_tile_values) != len(tile_values), f"there are some {object} stuck together ")


def print_map(map : Map):
    print('  ', end='')
    for row in range(len(map.game_tile_map[0])):
        print (row, ' ', end='')
    print('')
    row_number = 0
    for row in map.game_tile_map:

        print(row_number,'', end='')
        row_number+=1
        for column in row:
            print(column.symbol,' ',end='')
        print('')



