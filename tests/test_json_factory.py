from config import CONFIG
from detection.system.sensor.traceroute import get_traceroute_list
from detection.system.database.json_factory import jsonify_trace_list
from datetime import datetime
import unittest


class TestJSONFactory(unittest.TestCase):
    def test_jsonify_trace_list(self):
        lab_sensor_ip = '192.0.0.3'
        lab_destination_ip = '198.18.1.13'

        test_hops = [(1, [9.0, 10.0, 10.0], '192.0.0.254'),
                     (2, [28.0, 30.0, 31.0], '23.9.1.1'),
                     (3, [26.0, 30.0, 30.0], '10.0.0.1'),
                     (4, [45.0, 51.0, 40.0], '10.0.0.9'),
                     (5, [89.0, 93.0, 139.0], '10.0.0.18'),
                     (6, [72.0, 72.0, 72.0], '198.18.1.13')]

        expected_result = {'destination_ip': '198.18.1.13',
                           'hops': [{'delays': [9.0, 10.0, 10.0],
                                     'hop_ip': '192.0.0.254',
                                     'hop_num': 1,
                                     'responded': True},
                                    {'delays': [28.0, 30.0, 31.0],
                                     'hop_ip': '23.9.1.1',
                                     'hop_num': 2,
                                     'responded': True},
                                    {'delays': [26.0, 30.0, 30.0],
                                     'hop_ip': '10.0.0.1',
                                     'hop_num': 3,
                                     'responded': True},
                                    {'delays': [45.0, 51.0, 40.0],
                                     'hop_ip': '10.0.0.9',
                                     'hop_num': 4,
                                     'responded': True},
                                    {'delays': [89.0, 93.0, 139.0],
                                     'hop_ip': '10.0.0.18',
                                     'hop_num': 5,
                                     'responded': True},
                                    {'delays': [72.0, 72.0, 72.0],
                                     'hop_ip': '198.18.1.13',
                                     'hop_num': 6,
                                     'responded': True}],
                           'sensor_id': 2,
                           'timestamp': datetime.now()}

        # input = sensor_ip, destination_ip, hops
        actual_result = jsonify_trace_list(lab_sensor_ip, lab_destination_ip, test_hops)

        self.assertAlmostEqual(expected_result, actual_result)
