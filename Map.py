from GameTile import GameTile
import math
import random
import re

import Pathing


class Map:
    def __init__(self, size):
        self.game_tile_map = []
        self.game_tiles = []
        self.size = size
        self._initialise_empty_map(size)
        self.visual_map = ''

    def _initialise_empty_map(self, size):
        '''
        Initialise an empty map,
        :param size: int x and y size
        :return:
        '''
        instance_iterator = 0
        for y in range(size):
            line=[]
            for x in range(size):
                new_tile = GameTile('empty', instance_iterator,x,y)
                line.append(new_tile)
                instance_iterator +=1
            self.game_tile_map.append(line)
        y=1



    

    def set_objects(self, players, debug):
        '''
        Set the game space objects, based on the size of the map, if in debug then set the static map
        :param players: int number of players arriving
        :param debug: bool for if the static map is to be setup for testing
        :return:
        '''
        if debug:
            '''
            '''
            self.game_tile_map[2][2] = GameTile('obstacle', 0)
            self.game_tile_map[1][1] = GameTile('player_base', 0)
            self.game_tile_map[1][3] = GameTile('player_base', 1)
            self.game_tile_map[3][1] = GameTile('player_base', 2)
            self.game_tile_map[3][3] = GameTile('player_base', 3)
            self.game_tile_map[1][2] = GameTile('mine', 0)
            self.game_tile_map[3][2] = GameTile('mine', 1)

            for x in range(5):
                for y in range(5):
                    target_object = self.game_tile_map[x][y]
                    target_object.update_location(x, y)
                    print(f"x:{x} , y:{y} object :{target_object.coords}, type: {target_object.name}")
        else:
            blocking_object_count = math.ceil(self.size / 2)
            self.create_map_object('obstacle', blocking_object_count)
            self.create_map_object('player_base', players)
            self.create_map_object('mine', blocking_object_count)
        for column in range(self.size):
            for row in range(self.size):
                self.game_tiles.append(self.game_tile_map[column][row])


    def get_objects(self, object_type):
        found_objects = []
        for line in self.game_tile_map:
            found_objects.extend([ob for ob in line if ob.type == object_type])
        return found_objects

    def get_tile(self, x, y):
        return self.game_tile_map[x][y]
    def get_tiles_by_type(self, type):
        '''
        Get tiles from tile pool by type
        :param type (str):
        :return List[GameTile]:
        '''
        return [tile for tile in self.game_tiles if tile.type == type]


    def get_path(self, object_1, object_2):
        return Pathing.find_path(object_1.coords, object_2.coords, self)

    def create_map_object(self, map_object_type, number):
        '''
        Add objects to the map
        :param type: list of object types
        :param number(int): number of type to be added
        :return:
        '''
        instance = 0
        for element in range(number):
            map_object = GameTile(map_object_type, instance)
            instance += 1

            while True:
                rand_x = random.randint(0, self.size - 1)
                rand_y = random.randint(0, self.size - 1)
                map_location = self.game_tile_map[rand_x][rand_y]
                if map_location.type == 'empty':
                    self.game_tile_map[rand_x][rand_y] = map_object
                    map_object.update_location(rand_x, rand_y)
                    break








