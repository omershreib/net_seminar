from config import CONFIG
from detection.utilities.prefix2as import prefix2as
from ipaddress import IPv4Network
import unittest


class TestPrefix2AS(unittest.TestCase):

    def setUp(self):
        self.prefixes = prefix2as.load_prefixes(CONFIG['utilities']['prefix2as'])

    def test_load_prefixes(self):
        expected_result = [(IPv4Network('1.1.1.1/32'), 100),
                           (IPv4Network('2.2.2.2/32'), 200),
                           (IPv4Network('3.3.3.3/32'), 300),
                           (IPv4Network('4.4.4.4/32'), 400),
                           (IPv4Network('6.6.6.6/32'), 666),
                           (IPv4Network('192.168.10.0/24'), 100),
                           (IPv4Network('10.0.0.2/32'), 100),
                           (IPv4Network('10.0.0.1/32'), 200),
                           (IPv4Network('10.0.0.6/32'), 200),
                           (IPv4Network('172.16.1.0/24'), 200),
                           (IPv4Network('10.0.0.5/32'), 666),
                           (IPv4Network('10.0.0.13/32'), 666),
                           (IPv4Network('10.0.0.10/32'), 200),
                           (IPv4Network('10.0.0.9/32'), 300),
                           (IPv4Network('10.0.0.14/32'), 300),
                           (IPv4Network('10.0.0.17/32'), 300),
                           (IPv4Network('10.0.0.18/32'), 400),
                           (IPv4Network('198.18.1.0/24'), 400)]

        actual_result = self.prefixes

        self.assertEqual(expected_result, actual_result)

    def test_ip_to_asn(self):
        actual_results = []
        test_ips = ['1.1.1.1', '2.2.2.2', '3.3.3.3', '4.4.4.4', '6.6.6.6',
                    '192.168.10.100', '10.0.0.2', '10.0.0.1', '10.0.0.6', '172.16.1.0',
                    '10.0.0.5', '10.0.0.13', '10.0.0.10', '10.0.0.9', '10.0.0.14',
                    '10.0.0.17', '10.0.0.18', '198.18.1.13', '7.7.7.7']

        expected_results = [100, 200, 300, 400, 666, 100, 100, 200, 200, 200, 666, 666,
                            200, 300, 300, 300, 400, 400, None]

        for ip in test_ips:
            actual_results.append(prefix2as.ip_to_asn(ip, self.prefixes))

        self.assertEqual(expected_results, actual_results)
