from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import subprocess


def is_mongo_available(uri="mongodb://localhost:27017"):
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=2000)
        client.admin.command("ping")
        client.close()
        return True
    except ConnectionFailure:
        return False


def is_gns3lab_available():
    lab_host_ip = '198.18.1.13'
    connectivity_string = "Packets: Sent = 4, Received = 4, Lost = 0 (0% loss)"
    ping_response = subprocess.check_output(["ping", lab_host_ip])

    return connectivity_string in ping_response.decode()
