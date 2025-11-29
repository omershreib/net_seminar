from detection.system.sensor.traceroute import traceroute_host, get_traceroute_list, get_delay_list
from tests.is_available import is_gns3lab_available
import unittest

GNS3LAB_AVAILABLE = is_gns3lab_available()


@unittest.skipUnless(GNS3LAB_AVAILABLE is True, "gns3 lab is not available")
class TestTraceroute(unittest.TestCase):
    def setUp(self):
        self._test_trace_file = r'test_files/test_traceroute_raw_data.txt'

        with open(self._test_trace_file) as f:
            self.test_traceroute = f.read()

    def test_traceroute_host(self):
        connectivity_string = 'Trace complete.'
        test_lab_host = '198.18.1.13'
        response = traceroute_host(test_lab_host)

        self.assertTrue(connectivity_string in response, msg=f"traceroute {test_lab_host}\nresponse: {response}")

    def test_get_traceroute_list(self):
        expected_result = [(1, [9.0, 10.0, 10.0], '192.0.0.254'),
                           (2, [28.0, 30.0, 31.0], '23.9.1.1'),
                           (3, [26.0, 30.0, 30.0], '10.0.0.1'),
                           (4, [45.0, 51.0, 40.0], '10.0.0.9'),
                           (5, [89.0, 93.0, 139.0], '10.0.0.18'),
                           (6, [72.0, 72.0, 72.0], '198.18.1.13')]

        actual_result = get_traceroute_list(self.test_traceroute)

        self.assertEqual(expected_result, actual_result)

    def test_get_delay_list(self):
        test_hop_item = [('2', '14ms', '20ms', '20ms', '23.9.1.1 ')]
        expected_result = [14, 20, 20]
        actual_result = get_delay_list(test_hop_item)

        self.assertEqual(expected_result, actual_result)
