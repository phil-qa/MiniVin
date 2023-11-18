import unittest
#from tests.test_MapTests import MapTestModule
#from tests.test_PlayerTests import PlayerTestModule
#from tests.test_PathTests import PathTestModule
#from tests.test_GamestateTests import GameStateModuleTests

def create_test_suite():
    loader = unittest.TestLoader()
    suite = loader.discover('./tests', pattern='test_*.py')
    '''
    suite.addTest(loader.loadTestsFromTestCase(MapTestModule))
    suite.addTest(loader.loadTestsFromTestCase(PlayerTestModule))
    suite.addTest(loader.loadTestsFromTestCase(PathTestModule))
    suite.addTest(loader.loadTestsFromTestCase(GameStateModuleTests))
    '''
    return suite

if __name__ == '__main__':
    test_suite = create_test_suite()
    unittest.TextTestRunner(verbosity=2).run(test_suite)