import math
import random
from collections import deque


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
            blank_build.append([MapObject('empty', x, y) for x in range(size)])
        self.map_array = blank_build

    def set_objects(self, players, debug):
        '''
        Function to set the game space objects, based on the size of the map, if in debug then set the static map
        :param players: int number of players arriving
        :param debug: bool for if the static map is to be setup fort testing
        :return:
        '''
        if debug:
            self.map_array[2][2] = MapObject('obstacle', 0)
            self.map_array[1][1] = MapObject('player_base', 0)
            self.map_array[1][3] = MapObject('player_base', 1)
            self.map_array[3][1] = MapObject('player_base', 2)
            self.map_array[3][3] = MapObject('player_base', 3)
            self.map_array[1][2] = MapObject('mine', 0)
            self.map_array[3][3] = MapObject('mine', 1)

            for x in range(4):
                for y in range(4):
                    target_object = self.map_array[x][y]
                    target_object.update_location(x, y)
                    print(f"x:{x} , y:{y} object :{target_object.coords}, type: {target_object.name}")
            return

        blocking_object_count = math.ceil(self.size / 2)
        self.create_map_object('obstacle', blocking_object_count)
        self.create_map_object('player_base', players)
        self.create_map_object('mine', blocking_object_count)

    def get_objects(self, object_type):
        found_objects = []
        for line in self.map_array:
            found_objects.extend([ob for ob in line if ob.type == object_type])
        return found_objects

    def get_object(self, x, y):
        return self.map_array[x][y]

    def get_path(self, object_1, object_2):
        return utility.find_path(self.map_array, object_1.coords, object_2.coords)

    def create_map_object(self, map_object_type, number):
        '''
        Function to add objects to the map
        :param type: list of object types
        :param number: number of type to be added
        :return:
        '''
        instance = 0
        for element in range(number):
            map_object = MapObject(map_object_type, instance)
            instance += 1
            while True:
                rand_x = random.randint(0, self.size - 1)
                rand_y = random.randint(0, self.size - 1)
                map_location = self.map_array[rand_x][rand_y]
                if map_location.type == 'empty':
                    self.map_array[rand_x][rand_y] = map_object
                    map_object.update_location(rand_x, rand_y)
                    break


class MapObject:
    def __init__(self, type, instance, x_location=0, y_location=0):
        self.name = f'{type}{str(instance)}'
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
            self.resource = random.randint(16, 32)
            self.passable = False
        elif type == 'player_base':
            self.symbol = self.name
            self.resource = 0
            self.passable = False
            self.symbol = 'b'

    def update_location(self, x, y):
        self.x_location = x
        self.y_location = y
        self.coords = [x, y]


class utility:
    @staticmethod
    def find_path(map, start, end):
        # possible directions
        directions = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        # record of visited so that they are not re-visited
        visited = set()
        # build a path matrix
        matrix = []
        for y in range(len(map)):
            row = []
            for x in range(len(map)):
                if map[y][x].passable == True:
                    row.append(0)
                else:
                    row.append(1)

        rows, columns = len(map), len(map)

        queue = deque()

        queue.append([0, 0, 0])  # row column and distance

        # implement bfs
        while len(queue) > 0:
            current_row, current_column, current_distance = queue.popleft()
            if current_row == rows - 1 and current_row == columns - 1:  # this is the end corner of the map
                return current_distance

            if matrix[current_row][current_column] == 1:
                continue
            #iterate through the directions
            for direction in directions:
                next_row, next_column = current_row + direction[0], current_column + direction[1]
                if 0 <= next_row < rows and 0 <= next_column < columns and (next_row, next_column) not in visited:
                    queue.append([next_row, next_column, current_distance +1])
                    visited.add(((next_row, next_column)))
        return -1