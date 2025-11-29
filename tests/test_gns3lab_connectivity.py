from is_available import is_gns3lab_available
import subprocess
import unittest


class TestGNS3LabConnectivity(unittest.TestCase):

    def setUp(self):
        self.components_list = ['198.18.1.13', '198.18.1.254', '203.0.113.1', '203.0.113.254']

    @staticmethod
    def ping_lab_component(ip):
        connectivity_string = "Packets: Sent = 4, Received = 4, Lost = 0 (0% loss)"
        ping_response = subprocess.check_output(["ping", ip])

        return connectivity_string in ping_response.decode()

    def test(self):
        for component_ip in self.components_list:
            response = self.ping_lab_component(component_ip)
            self.assertTrue(response, msg=f"ping to {component_ip}\nresponse: {response}")
