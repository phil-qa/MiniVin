import math
import random


class Map:
    def __init__(self, size):
        self.map_array = []
        self.size = size
        self.initialise_empty_map(size)


    def initialise_empty_map(self, size):
        '''
        Function to initise the map,
        :param size: int x and y size, debug
        :return:
        '''
        blank_build = []
        for y in range(size):
            blank_build.append([MapObject('empty',x,y ) for x in range(size)])
        self.map_array = blank_build

    def set_objects(self, players, debug):
        '''
        Function to set the game space objects, based on the size of the map, if in debug then set the static map
        :param players: int number of players arriving
        :param debug: bool for if the static map is to be setup fort testing
        :return:
        '''
        if debug:
            self.map_array[2][2] = MapObject('obstacle')
            self.map_array[1][1] = \
            self.map_array[1][3] = \
            self.map_array[3][1] = \
            self.map_array[3][3] = MapObject('player_base')
            self.map_array[2][1] = \
            self.map_array[2][3] = MapObject('mine')
            return
        blocking_object_count = math.ceil(self.size/2)
        self.set_positions(MapObject('obstacle'), blocking_object_count)
        for p in range(players):
            player_map_object = MapObject('player_base')
            player_map_object.symbol = 'b'
            self.set_positions(player_map_object, 1)
        self.set_positions(MapObject('mine'), blocking_object_count)

    def get_objects(self,object_type):
        found_objects = []
        for line in self.map_array:
            found_objects.extend([ob for ob in line if ob.type == object_type])
        return found_objects

    def get_object(self, x, y):
        return self.map_array[x][y]

    def set_positions(self, map_object, number):
        '''
        Function to add objects to the map
        :param type: list of object types
        :param number: number of type to be added
        :return:
        '''
        for element in range(number):
            while True:
                rand_x = random.randint(0,self.size - 1)
                rand_y = random.randint(0,self.size - 1)
                map_location = self.map_array[rand_x][rand_y]
                if map_location.type == 'empty':
                    self.map_array[rand_x][rand_y] = map_object
                    break





class MapObject:
    def __init__(self, type, x_location = 0, y_location = 0):
        self.name = type
        self.type = type
        self.x_location = x_location
        self.y_location = y_location
        if type == 'empty':
            self.symbol = 0
            self.resource = 0
            self.passable = True
        elif type == 'obstacle':
            self.symbol = 'o'
            self.resource = 0
            self.passable = False
        elif type == 'mine':
            self.symbol = 'm'
            self.resource = random.randint(16,32)
            self.passable = False
        elif type == 'player_base':
            self.symbol = self.name
            self.resource = 0
            self.passable = False


