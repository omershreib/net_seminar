# this prefix2as loaded file contains data about all the address prefixes used in the GNS3 lab simulation
# and needed because not all the prefixes are announced in the lab (meaning that it is not possible to
# learn about all the prefixes in the project from the localISP routing table alone)
#
# by the way, there is a real prefix2as file that University of Oregon
# shared with the world under a project named RouteViews.
#
# the real prefix2as file can be downloaded in this link:
# https://publicdata.caida.org/datasets/routing/routeviews-prefix2as/
#
# another thing that RouteViews shared is an oix file, which is a real BGP snapshot that contains
# the entire list of address prefix announcements published in the internet
# oix file can be downloaded in this link:
# https://archive.routeviews.org/oix-route-views/

import ipaddress
import csv


def load_prefixes(csv_file):
    """
    load prefix from CSV file

    :param csv_file: prefix csv file
    :return: a list of tuples. each tuples is the following item: (<IPv4Network objects>, <ASN>)
    """
    prefixes = []
    with open(csv_file, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0].lower() == "network":
                continue
            network, mask, asn = row
            cidr = f"{network}/{mask}"
            prefixes.append((ipaddress.ip_network(cidr), int(asn)))
    return prefixes


def ip_to_asn(ip: str, prefixes):
    """

    map IP address to ASN (if not found in prefix file, return None)

    :param ip: IP address
    :param prefixes: loaded prefix object
    :return: ASN
    """
    ip_obj = ipaddress.ip_address(ip)
    for network, asn in prefixes:
        if ip_obj in network:
            return asn
    return None