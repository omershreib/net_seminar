from pprint import pprint
import subprocess
import re


class Hop:
    def __init__(self, hop_items):
        #print(hop_items)
        self._hop_item = hop_items
        self.hop_num = None
        self.delay_list = []
        self.dest_ip = None
        self.is_dest_exist = False
        self.raw_dest_field = None
        self.set_hop()

    @staticmethod
    def is_ipv4(value):
        return len(re.findall(r'\d+\.\d+\.\d+\.\d+', value)) > 0

    def set_hop(self):
        self.set_hop_num()
        self.set_hop_delay()
        self.set_hop_dest_ip()

    def set_hop_num(self):
        self.hop_num = int(self._hop_item[0][0])

    def set_hop_delay(self):
        # self.delay = get_min_hop_delay(self._hop_item)
        self.delay_list = get_delay_list(self._hop_item)

    def set_hop_dest_ip(self):
        # configuration for Windows os system
        self.raw_dest_field = self._hop_item[0][-1]

        if self.is_ipv4(self.raw_dest_field):
            self.is_dest_exist = True
            self.dest_ip = str(self._hop_item[0][-1]).strip(' ')

    def to_list(self):
        return self.hop_num, self.delay_list, self.dest_ip


def get_delay_list(hop_item):
    delays = []
    for i in range(1, 4):
        delay: str = hop_item[0][i].strip('ms')

        if delay.isnumeric():
            delays.append(float(delay))
            continue

        delays.append(None)

    return delays


def get_min_hop_delay(hop_item):
    valid_delays = []

    for i in range(1, 4):
        delay: str = hop_item[0][i]
        if delay == '*':
            continue

        valid_delays.append(float(delay.strip('ms')))

    return 0 if not valid_delays else min(valid_delays)


def get_traceroute_list(raw_output: str):
    hop_pattern = re.compile(
        r'\s{2}(\d+)\s+([0-9a-z\*]{1,10})\s+([0-9a-z\*]{1,10})\s+([0-9a-z\*]{1,10})\s+([0-9a-zA-Z\. ]{7,18})')
    # hop_pattern = re.compile(r'\s(\d+)([0-9a-zA-Z\. ]{7,18})\s+([0-9a-z\*\.]{1,10})\s+([0-9a-z\*\.]{1,10})\s+([0-9a-z\*\.]{1,10})')

    traceroute_list: list = []

    if '\r\n' in raw_output:
        raw_hop_lines: list = raw_output.replace('<1', '1').replace(' ms', 'ms').split('\r\n')
    else:
        raw_hop_lines: list = raw_output.replace('<1', '1').strip('\r').replace(' ms', 'ms').split('\n')

    for hop_line in raw_hop_lines:
        hop_items = hop_pattern.findall(hop_line)
        if not hop_items:
            continue

        hop = Hop(hop_items)
        traceroute_list.append(hop.to_list())

    return traceroute_list


def traceroute_host(host: str, timeout: int = 1000):
    output = subprocess.check_output(["tracert", '-w', f"{timeout}", "-d", host])
    return output.decode()


def test():
    with open('../../utilities/test_traceroute.csv', 'r') as f:
        test_raw_output = f.read()

    #pprint(get_traceroute_list(test_raw_output))


if __name__ == '__main__':
    response = traceroute_host('1.1.1.1')
    #pprint(get_traceroute_list(response))
