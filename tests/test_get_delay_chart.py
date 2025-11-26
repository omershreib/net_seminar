from detection.system.charts.get_delay_chart import get_delay_chart
from unittest.mock import MagicMock
from tests import mocked_collection
import unittest
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

class TestGetDelayChart(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_chart = r'test_files/test_expected_delay_chart.png'

    def setUp(self):
        # Create fake mongo_delay_temp data
        self.fake_data = mocked_collection.collection

        # Patch get_data_plane_delay to just return item['delay']
        # and set_delay_scatter to return a fresh fig, ax

        # get_data_plane_delay = lambda item: item["delay"]
        # set_delay_scatter = lambda: plt.subplots()

    def test_chart_matches_expected(self):
        # Mock collection.find to return our fake data
        mock_collection = MagicMock()
        mock_collection.find.return_value = self.fake_data

        self.excepted_img = mpimg.imread(self.test_chart)

        # Run the function
        actual_fig = get_delay_chart(mock_collection, limit=25, threshold=150)

        # Save the generated figure
        filename = "test_actual_chart.png"
        actual_fig.tight_layout()
        plt.savefig(filename, format="png", dpi=120)
        plt.close(actual_fig)
        plt.clf()

        actual_img = mpimg.imread("test_actual_chart.png")
        np.testing.assert_allclose(self.excepted_img, actual_img, rtol=1e-5, atol=1e-8)
