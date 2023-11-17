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
    def test_game_state_initialises(self):
        '''#given a game startup with four players
        #when the game initialises
        #then the map shall be generated
        and the players shall be creates
        and the state objects shall be created
        and the players shall be at their bases

        given a move state
        the players shall move according to the direction unless when the play7er attempts to move :
        there is an obstacle, the player will remain at location
        there is a mine, the player will mine a resource to a max of 5 times
        there is a map edge, the player will remain at location
        there is antother player base, the player will renmain at location
        there is a player base, the player shall move to it and hand over resources and have moves refreshed

        '''

        game_state = GameState(players=['amy', 'bob', 'cath', 'don'], map_size=8)
        self.assertIsNotNone(game_state.game_map, "Map not initialised")
        self.assertEqual(len(game_state.players), 4, "Number of players incorrect")
        for player in game_state.players:
            self.assertIsNotNone(player.coords, f"player {player.name} has not got coordinates set")
        self.assertEqual(len(game_state.mines), 4, "Number of mines incorrect")
        for mine in game_state.mines:
            self.assertIsNotNone(mine.coords, f"a mine has no coordinates")
        self.assertEqual(len(game_state.obstacles), 4, "Number of obstacles incorrect")
        for obstacle in game_state.obstacles:
            self.assertIsNotNone(obstacle.coords)
        self.assertEqual(len(game_state.player_bases), 4, "Number of bases incorrect")
        for base in game_state.player_bases:
            self.assertIsNotNone(base.coords)
        self.assertEqual(game_state.players[0].x_position, game_state.player_bases[0].x_position)
        self.assertEqual(game_state.players[0].y_position, game_state.player_bases[0].y_position)


    def test_game_state_events(self):
        '''
        given an initialised map
        when a player moves
        then the gamestate understands the response on target
         01234
        0*****
        1*a*c*
        2*m.**
        3*b***
        4***m*
        '''

        game_state, amy, bob, cathy = self.set_debug_game_state
        starting_positions = game_state.players.copy()

        self.assertEqual([1, 1], amy.coords, "Amy isnt in the right start point")
        self.assertEqual('11', amy.tile, "Tile for amy isnt right")
        self.assertEqual([1, 3], bob.coords, "bob isnt in the right start point")
        self.assertEqual('13', bob.tile, "Bobs name is not at the right place")
        self.assertEqual([3, 1], cathy.coords, "cathy isnt in the right start point ")
        self.assertEqual('31', cathy.tile, "Tile for cathy isnt right")
        # players move on update

        game_state.update_state({f'{amy.name}': 'e', f'{bob.name}': 'w', f'{cathy.name}': 's'})

        self.assertEqual([2, 1], amy.coords, "Amy isnt in the right place")
        self.assertEqual('21', amy.tile, "Tile for amy isnt right")
        self.assertEqual([0, 3], [bob.x_position, bob.y_position], "Bob isnt in the right place")
        self.assertEqual('03', bob.tile, "Tile for bob isnt right")
        self.assertEqual([3, 2], [cathy.x_position, cathy.y_position], "Cathy isnt in the right place")
        self.assertEqual('32', cathy.tile, "Tile for cathy isnt right")
        # players cant go over the map edges

        game_state.update_state({f'{amy.name}': 'n', f'{bob.name}': 'w', f'{cathy.name}': 'e'})

        self.assertEqual([2, 0], amy.coords, "Amy isnt in the right place")
        self.assertEqual([0, 3], [bob.x_position, bob.y_position], "Bob isnt in the right place")
        self.assertEqual([4, 2], [cathy.x_position, cathy.y_position], "Cathy isnt in the right place")

        game_state.update_state({f'{amy.name}': 'n', f'{bob.name}': 's', f'{cathy.name}': 'e'})

        self.assertEqual([2, 0], amy.coords, "Amy isnt in the right place")
        self.assertEqual([0, 4], [bob.x_position, bob.y_position], "Bob isnt in the right place")
        self.assertEqual([4, 2], [cathy.x_position, cathy.y_position], "Cathy isnt in the right place")

        # players cant go onto an obstacle at [2,2]

        game_state.update_state({f'{amy.name}': 's', f'{bob.name}': 'h', f'{cathy.name}': 'h'})

        self.assertEqual([2, 1], [amy.x_position, amy.y_position], "Amy isnt in the right place")
        self.assertEqual([0, 4], [bob.x_position, bob.y_position], "Bob isnt in the right place")
        self.assertEqual([4, 2], [cathy.x_position, cathy.y_position], "Cathy isnt in the right place")

        game_state.update_state({f'{amy.name}': 's', f'{bob.name}': 'h', f'{cathy.name}': 'h'})

        self.assertEqual([2, 1], [amy.x_position, amy.y_position], "Amy tried to move into an obstacle at 2,2 she should not be there")
        self.assertEqual([0, 4], [bob.x_position, bob.y_position], "Bob isnt in the right place")
        self.assertEqual([4, 2], [cathy.x_position, cathy.y_position], "Cathy isnt in the right place")

        # # player approaching a mine name does not move

        game_state.update_state({f'{amy.name}': 'w', f'{bob.name}': 'h', f'{cathy.name}': 'h'})
        game_state.update_state({f'{amy.name}': 's', f'{bob.name}': 'h', f'{cathy.name}': 'h'})


        self.assertEqual([1, 1], [amy.x_position, amy.y_position], "Amy isnt in the right place")
        self.assertEqual('11', amy.name, "Tile for amy isnt right")
        self.assertEqual([0, 4], [bob.x_position, bob.y_position], "Bob isnt in the right place")
        self.assertEqual([4, 2], [cathy.x_position, cathy.y_position], "Cathy isnt in the right place")

        # a player that has approached a mine name has harvested one coin
        self.assertEqual(1, amy.resource, "amy  didnt get a coin")

        # a player can only mine five coins
        game_state.update_state({f'{amy.name}': 's', f'{bob.name}': 'h', f'{cathy.name}': 'h'})
        game_state.update_state({f'{amy.name}': 's', f'{bob.name}': 'h', f'{cathy.name}': 'h'})
        game_state.update_state({f'{amy.name}': 's', f'{bob.name}': 'h', f'{cathy.name}': 'h'})
        game_state.update_state({f'{amy.name}': 's', f'{bob.name}': 'h', f'{cathy.name}': 'h'})
        game_state.update_state({f'{amy.name}': 's', f'{bob.name}': 'h', f'{cathy.name}': 'h'})

        self.assertEqual(5, amy.resource, "amys got an odd amount of coins")


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
