from detection.system.charts.get_delay_chart import get_delay_chart
from unittest.mock import MagicMock
from tests import mocked_collection
import unittest
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os


class TestGetDelayChart(unittest.TestCase):

    def setUp(self):
        # create fake mongo_delay_temp data
        self.fake_data = mocked_collection.collection

        self.filename = "test_delay_actual_chart.png"
        self.test_chart = r'test_files/test_expected_delay_chart.png'

    def test_chart_matches_expected(self):
        # mock collection.find to return our fake data
        mock_collection = MagicMock()
        mock_collection.find.return_value = self.fake_data

        self.excepted_img = mpimg.imread(self.test_chart)

        actual_fig = get_delay_chart(mock_collection)

        actual_fig.tight_layout()
        plt.savefig(self.filename, format="png", dpi=120)
        plt.close(actual_fig)
        plt.clf()

        actual_img = mpimg.imread(self.filename)
        np.testing.assert_allclose(self.excepted_img, actual_img, rtol=1e-5, atol=1e-8)

    def tearDown(self):
        os.remove(self.filename)
