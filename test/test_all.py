import unittest
from test.CommTests.test_Comm import CommTests
from test.AutomatonTests.test_FtpAutomaton import FtpAutomatonTests

def create_suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(CommTests())
    test_suite.addTest(FtpAutomatonTests())
    return test_suite

if __name__ == '__main__':
    suite = create_suite()

    runner = unittest.TextTestRunner()
    runner.run(suite)
