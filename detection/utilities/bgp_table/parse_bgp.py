from pyparsing import Word, Combine, Optional, oneOf, nums, Group, OneOrMore, Literal, ParseException
from ipaddress import IPv4Address, IPv4Network
import pandas as pd


# define grammar components
status_code = Combine(Optional(oneOf("r * >")) + Optional(Literal(">")))
ip_octet = Word(nums, max=3)
ip_addr = Combine(ip_octet + "." + ip_octet + "." + ip_octet + "." + ip_octet)
prefix = Combine(ip_addr + Optional("/" + Word(nums)))
next_hop = ip_addr
metric = Word(nums)
locprf = Word(nums)
weight = Word(nums)
path = Group(OneOrMore(Word(nums)))
origin = oneOf("i e ?")

bgp_fields = ["status", "network", "next_hop", "metric", "locprf", "weight", "path", "origin"]

# Cisco did the life of dev-nets programmer very hard and made the parsing of the routing table very complicated
# there is something called "Cisco Genie Parser" that should do the life easier in terms of Cisco output parsing
# but unfortunately, at least for what Ia know, it is currently support only linux
#
# my solution was to perform 3 version of possible parsing and take the best of them
bgp_line_v1 = (
        status_code("status")
        + prefix("network")
        + next_hop("next_hop")
        + metric("metric")
        + locprf("locprf")
        + weight("weight")
        + Optional(path("path"))
        + origin("origin")
)

bgp_line_v2 = (
        status_code("status")
        + prefix("network")
        + next_hop("next_hop")
        + metric("metric")
        + weight("weight")
        + Optional(path("path"))
        + origin("origin")
)

bgp_line_v3 = (
        status_code("status")
        + prefix("network")
        + next_hop("next_hop")
        + weight("weight")
        + Optional(path("path"))
        + origin("origin")
)

def load_bgp_table_file(filename):
    """
    Load BGP Snapshot Table From File

    the BGP snapshot is made by performing the Cisco IOS command "show ip bgp" on a Cisco IOS router
    that runs BGP (also known as BGP speaker).

    for further information:
    https://www.cisco.com/c/en/us/td/docs/ios/iproute_bgp/command/reference/irg_book/irg_bgp5.html

    :param filename: the filename of the BGP snapshot
    :return: a list contains only the bgp routes lines
    """
    flag = False
    file_lines = []

    with open(filename, 'r') as f:
        for line in f:
            if flag and ('>' in line):
                file_lines.append(line.strip('\n'))

            if 'Network' in line:
                flag = True

    return file_lines


def normalize_network(net_str):
    """
    normalize network by added /<mask> to a given string network address

    :param net_str: string network address
    :return: "normalized" IPv4Network object (by default define with /24)
    """
    if "/" not in net_str:
        return IPv4Network(net_str + "/24", strict=False)
    return IPv4Network(net_str, strict=False)


def bgp_table_to_dict(bgp_file):
    """
    BGP Table to Dictionary

    parse a given BGP snapshot file and create a list of BGP routes, so every
    route in this list is equivalences to route line in the original BGP snapshot file

    Note:
    ----
    this parsing algorithm is absolutely not perfect and will likely NOT work under the following condition:
        1. a route with a pre-configured weight value
        (this is a Cisco property attribute that overcome local preference)

        2. a route that their path is a singleton of [32768]

    :param bgp_file: BGP snapshot file (downloaded from FTP server)
    :return: a list of BGP routes
    """
    table = load_bgp_table_file(bgp_file)
    bgp_routes = []
    for row in table:
        results = []
        try:
            result_v1 = bgp_line_v1.parseString(row)
            results.append(result_v1)
        except ParseException:
            results.append(None)

        try:
            result_v2 = bgp_line_v2.parseString(row)
            results.append(result_v2)
        except ParseException:
            results.append(None)

        try:
            result_v3 = bgp_line_v3.parseString(row)
            results.append(result_v3)
        except ParseException:
            results.append(None)

        for i, result in enumerate(results):

            if not result:
                continue

            keys = list(result.keys())
            bgp_route: dict = {bgp_field: None for bgp_field in bgp_fields}

            if result['next_hop'] != '0.0.0.0' and 'path' not in keys:
                continue

            if 'weight' in keys and result['weight'] not in ['0', '32768']:
                continue

            if 'path' in keys and result['path'][0] in ['0', '32768']:
                continue

            for key in keys:
                if key == 'path':
                    bgp_route[key] = list(result[key])

                else:
                    bgp_route[key] = result[key]

            bgp_routes.append(bgp_route)

    return bgp_routes
