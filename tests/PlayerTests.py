import unittest
from Player import Player

class PlayerTestModule(unittest.TestCase):
    def test_player_initialises(self):
        player = Player("bob")
        self.assertIsNotNone(player)
        self.assertEqual("bob", player.name)

    def test_player_set(self):
        player = Player("bob")
        player.set(x_pos=0, y_pos=0, health=30)
        self.assertEqual(0, player.x_position)
        self.assertEqual(0, player.y_position)
        self.assertEqual(30, player.health)
        self.assertEqual(30, player.max_health)
        self.assertEqual(0, player.resource)
        self.assertEqual('00', player.tile)

