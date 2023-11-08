import unittest
from MapTests import MapTestModule
from PlayerTests import PlayerTestModule

def create_test_suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(MapTestModule))
    suite.addTest(loader.loadTestsFromTestCase(PlayerTestModule))

    return suite

if __name__ == '__main__':
    test_suite = create_test_suite()
    unittest.TextTestRunner(verbosity=2).run(test_suite)