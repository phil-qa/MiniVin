import unittest
from tests.MapTests import MapTestModule
from tests.PlayerTests import PlayerTestModule
from tests.PathTests import PathTestModule
from tests.GamestateTests import GameStateModuleTests

def create_test_suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(MapTestModule))
    suite.addTest(loader.loadTestsFromTestCase(PlayerTestModule))
    suite.addTest(loader.loadTestsFromTestCase(PathTestModule))
    suite.addTest(loader.loadTestsFromTestCase(GameStateModuleTests))

    return suite

if __name__ == '__main__':
    test_suite = create_test_suite()
    unittest.TextTestRunner(verbosity=2).run(test_suite)