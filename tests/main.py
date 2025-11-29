import unittest
import os


def run_tests():
    loader = unittest.TestLoader()
    suite = loader.discover(os.curdir)
    print(f"Total Number of TestCases: {suite.countTestCases()}")

    runner = unittest.TextTestRunner()
    runner.run(suite)


if __name__ == '__main__':
    run_tests()
