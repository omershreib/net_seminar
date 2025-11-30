import subprocess
import re


class Hop:
    """Traceroute Hop Class Object"""

    def __init__(self, hop_items, os_type):
        self._hop_item = hop_items
        self.hop_num = None
        self.delay_list = []
        self.dest_ip = None
        self.is_dest_exist = False
        self.raw_dest_field = None
        self._os_type = os_type
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
        self.delay_list = get_delay_list(self._hop_item, self._os_type)

    def set_hop_dest_ip(self):
        # configuration for Windows OS system
        if self._os_type == "Windows":
            self.raw_dest_field = self._hop_item[0][-1]

            if self.is_ipv4(self.raw_dest_field):
                self.is_dest_exist = True
                self.dest_ip = str(self._hop_item[0][-1]).strip(' ')

        if self._os_type == "Linux":
            self.raw_dest_field = self._hop_item[0][1]

            if self.is_ipv4(self.raw_dest_field):
                self.is_dest_exist = True
                self.dest_ip = str(self._hop_item[0][1]).strip(' ')

    def to_list(self):
        return self.hop_num, self.delay_list, self.dest_ip


def get_delay_list(hop_item, os_type="Windows"):
    delays = []

    if os_type == "Windows":
        for i in range(1, 4):
            delay: str = hop_item[0][i].strip('ms')

            if delay.isnumeric():
                delays.append(float(delay))
                continue

            delays.append(None)

    if os_type == "Linux":
        for i in range(1, 4):

            # if the valid hop line format does not exist
            if len(hop_item[0]) < 5:
                delays.append(None)
                continue

            delay_temp: str = hop_item[0][i + 1].replace('ms', '').strip().split('.')

            if len(delay_temp) == 2:
                delay = delay_temp[0]

            else:
                delays.append(None)
                continue

            if delay.isnumeric():
                delays.append(float(delay))
                continue

            delays.append(None)

    return delays


def get_traceroute_list(raw_output: str, os_type: str = "Windows"):
    """
    parse a traceroute raw data output and return a list of Hops class objects

    Note:
    ----
    this code is likely support only Windows OS system and not linux, since the parsing is assumed
    to receive traceroute response output in the Windows's CMD format.

    :param os_type: Windows or Linux
    :param raw_output: the traceroute raw data known CMD response
    :return: list of Hops class objects that their collection provide the entire traceroute
    """
    traceroute_list: list = []

    if os_type == "Windows":
        # regex pattern to match: <hop_num>, <delay_1>, <delay_2>, <delay_3>, <hop_ip>
        hop_pattern = re.compile(
            r'\s{2}(\d+)\s+([0-9a-z\*]{1,10})\s+([0-9a-z\*]{1,10})\s+([0-9a-z\*]{1,10})\s+([0-9a-zA-Z\. ]{7,18})')

    else:
        # try Linux form
        # regex pattern to match: <hop_num>, <hop_ip>, <delay_1>, <delay_2>, <delay_3>
        hop_pattern = re.compile(
            r'\s{1}(\d+)\s+([0-9a-zA-Z\.]{7,18})\s+([0-9a-z\*\.\s]{1,10})\s+([0-9a-z\*\.\s]{1,10})\s+([0-9a-z\*\.\s]{'
            r'1,10})')

    # clean raw output with any text that is not the numeric value of the delay
    if '\r\n' in raw_output:
        raw_hop_lines: list = raw_output.replace('<1', '1').replace(' ms', 'ms').split('\r\n')
    else:
        raw_hop_lines: list = raw_output.replace('<1', '1').strip('\r').replace(' ms', 'ms').split('\n')

    for hop_line in raw_hop_lines:
        hop_items = hop_pattern.findall(hop_line)

        if not hop_items:
            if '* * *' in hop_line:
                hop_items = str(hop_line).split(' ')
            else:
                continue

        hop = Hop(hop_items, os_type)
        traceroute_list.append(hop.to_list())

    return traceroute_list


def traceroute_host(host: str, timeout: int = 1000, os_type: str = "Windows"):
    """
    perform traceroute task and return the raw data response

    :param os_type: Windows or Linux
    :param host: the traceroute target IP address
    :param timeout: timeout of this traceroute procedure (prefer to set a lower
                    timeout value compare to Windows's 4 seconds default timeout)

    :return: decoded string output
    """
    if os_type == "Linux":
        output = subprocess.check_output(["traceroute", "-n", host])
    else:
        output = subprocess.check_output(["tracert", '-w', f"{timeout}", "-d", host])

    return output.decode()


if __name__ == '__main__':
    from pprint import pprint

    os_type = "Windows"
    output = traceroute_host('1.1.1.1', os_type=os_type)
    mylist = get_traceroute_list(output, os_type=os_type)

    pprint(mylist)


