import networkx as nx


class Pathing:
    import networkx as nx

    @classmethod
    def check_outer_edge(cls, actual_x, actual_y, potential_x, potential_y, dimension):
        if actual_x + potential_x >= 0 and actual_x + potential_x <= dimension:
            if actual_y + potential_y >= 0 and actual_y + potential_y <= dimension:
                return True
            else:
                return False

    @classmethod
    def check_target_passable(cls,target_x, target_y, map_object):
        if map_object.game_tile_map[target_x][target_y].passable:
            return True
        else:
            return False

    @classmethod
    def build_map(cls, source_map):
        dimension = source_map.size - 1
        graph = nx.Graph()
        for y in range(dimension):
            for x in range(dimension):
                potentials = [[-1, 0], [+1, 0], [0, -1], [0, +1]]
                key = f'{x}{y}'
                local_cells = []
                for potential in potentials:
                    node_in_map = Pathing.check_outer_edge(x, y, potential[0], potential[1], dimension)
                    target_can_be_entered = Pathing.check_target_passable(x + potential[0], y + potential[1], source_map)
                    if node_in_map and target_can_be_entered:
                        local_cells.append(f'{x + potential[0]}{y + potential[1]}')
                graph.add_node(key)
                for n in local_cells:
                    graph.add_edge(key, n)
        return graph

    # Create a graph object. build offhand in original map

    @classmethod
    def build_graph(cls, map):
        return cls.build_map(map)

    @staticmethod
    def find_path(start, end, map):
        graph = Pathing.build_graph(map)
        shortest_path = list(nx.shortest_path(Pathing.build_graph(map), start, end))
        if shortest_path[-1] != end:
            shortest_path.append(end)

        return shortest_path


    @staticmethod
    def convert_tile_transisiton_to_direction(source_tile, target_tile):
        source_x = int(source_tile[0])
        source_y = int(source_tile[1])
        destination_x = int(target_tile[0])
        destination_y = int(target_tile[1])
        if destination_x < source_x:
            return 'w'
        elif destination_x > source_x:
            return 'e'
        elif destination_y < source_y:
            return 'n'
        elif destination_y > source_y:
            return 's'
        return None

    @staticmethod
    def translate_path(tile_objects):
        direction_steps = []
        for index in range(1,len(tile_objects)):
            direction_steps.append(Pathing.convert_tile_transisiton_to_direction(tile_objects[index-1], tile_objects[index]))
        return direction_steps