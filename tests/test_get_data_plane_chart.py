from config import CONFIG
from detection.system.charts.get_data_plane_chart import get_data_plane_chart
from detection.utilities.as_relationships import get_as_relationships
from detection.utilities.prefix2as import prefix2as
import unittest
import numpy as np
import os
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

AS_RELATIONSHIPS = get_as_relationships()


class TestGetDataPlaneChart(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_chart = r'test_files/test_expected_data_plane_chart.png'
        self.prefixes = prefix2as.load_prefixes(CONFIG['utilities']['prefix2as'])

    def test_get_data_plane_chart(self):
        expected_hop_to_asn_dict = {'10.0.0.1': 200,
                                    '10.0.0.18': 400,
                                    '10.0.0.9': 300,
                                    '192.0.0.254': None,
                                    '198.18.1.13': 400,
                                    '23.9.1.1': None}

        trace_hops = [{'hop_num': 1, 'hop_ip': '192.0.0.254', 'delays': [7.0, 10.0, 9.0], 'responded': True},
                      {'hop_num': 2, 'hop_ip': '23.9.1.1', 'delays': [16.0, 20.0, 20.0], 'responded': True},
                      {'hop_num': 3, 'hop_ip': '10.0.0.1', 'delays': [31.0, 30.0, 30.0], 'responded': True},
                      {'hop_num': 4, 'hop_ip': '10.0.0.9', 'delays': [67.0, 61.0, 72.0], 'responded': True},
                      {'hop_num': 5, 'hop_ip': '10.0.0.18', 'delays': [68.0, 72.0, 82.0], 'responded': True},
                      {'hop_num': 6, 'hop_ip': '198.18.1.13', 'delays': [76.0, 103.0, 102.0], 'responded': True}]

        self.excepted_img = mpimg.imread(self.test_chart)

        actual_fig, actual_hop_to_asn_dict = get_data_plane_chart(trace_hops=trace_hops,
                                                                  prefixes=self.prefixes,
                                                                  sensor_asn=100)
        filename = "test_actual_chart.png"
        actual_fig.tight_layout()
        plt.savefig(filename, format="png", dpi=120)
        plt.close(actual_fig)
        plt.clf()

        actual_img = mpimg.imread("test_actual_chart.png")
        np.testing.assert_allclose(self.excepted_img, actual_img, rtol=1e-5, atol=1e-8)

        self.assertEqual(expected_hop_to_asn_dict, actual_hop_to_asn_dict)
        os.remove(filename)
