from detection.utilities import as_relationships
import unittest


class TestASRelationships(unittest.TestCase):
    def test_get_as_relationships(self):
        excepted_result = {100: {'customers': [], 'other_peers': [], 'providers': [200]},
                           200: {'customers': [100, 666], 'other_peers': [300], 'providers': [200]},
                           300: {'customers': [400, 666], 'other_peers': [200], 'providers': []},
                           400: {'customers': [], 'other_peers': [], 'providers': [300]},
                           666: {'customers': [], 'other_peers': [], 'providers': [200, 300]}}

        actual_result = as_relationships.get_as_relationships()

        self.assertEqual(excepted_result, actual_result)
