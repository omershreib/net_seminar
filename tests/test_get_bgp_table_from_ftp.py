import os

from detection.dashboard.tools.get_bgp_table_from_ftp import pull_bgp_table
from external.bgp_table_to_ftp import upload_to_ftp
import unittest


class TestGetBGPTableFromFTP(unittest.TestCase):

    def setUp(self):
        self.filename = 'test_bgp_table.txt'
        self.is_setup_succeeded = upload_to_ftp(filename=self.filename)

        if not self.is_setup_succeeded:
            self.skipTest("unable to upload BGP snapshot to FTP server")

    def test_pull_bgp_table(self):
        result = pull_bgp_table(self.filename, filepath=self.filename)
        self.assertTrue(result)
        
    def tearDown(self):
        os.remove(self.filename)
        
