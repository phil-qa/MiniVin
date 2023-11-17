import unittest

from Main import GameState

class GameStateModuleTests(unittest.TestCase):

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
        test_player = game_state.players[0]
        test_base = game_state.player_bases[0]
        self.assertEqual(game_state.players[0].x_position, game_state.player_bases[0].x_position)
        self.assertEqual(game_state.players[0].y_position, game_state.player_bases[0].y_position)
        self.assertEqual(1,len( game_state.game_map.get_tile(test_base.x_position, test_base.y_position).players_on_tile ))