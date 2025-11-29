from config import CONFIG
from datetime import datetime


def jsonify_trace_list(sensor_ip, destination_ip, hops):
    """
    Jsonify Traceroute List

    this function create a json document of a given traceroute probe ready to be inserted to mongoDB.

    :param sensor_ip: IP address of the sensor perform this traceroute
    :param destination_ip: IP address of the monitored target
    :param hops: list of traceroute hops raw data
    :return: a dictionary with the traceroute document insert format
    """
    json_hops = []

    for hop in hops:
        hop_num, delays, hop_ip = hop
        json_hop = {}

        if hop_ip:
            json_hop = {"hop_num": hop_num, "hop_ip": hop_ip, "delays": delays, "responded": True}

        if not hop_ip:
            json_hop = {"hop_num": hop_num, "delays": delays, "responded": False}

        json_hops.append(json_hop)

    json_doc = {
        "timestamp": datetime.now(),  # required for time series
        "sensor_id": CONFIG['sensors_dict'][sensor_ip],
        "destination_ip": destination_ip,
        "hops": json_hops
    }

    return json_doc
