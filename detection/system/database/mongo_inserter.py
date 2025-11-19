from detection.detection_tools.traceroute import get_traceroute_list
from detection.system.database.json_factory import jsonify_trace_list
from pymongo import MongoClient, errors
from pprint import pprint
from queue import Queue
import threading
import time

trace_queue = Queue()


class MongoInserter(threading.Thread):
    def __init__(self):
        super().__init__()
        self.collection = "traceroutes"
        self._client = None
        self._db = None
        self.is_connect = False
        self._stop_event = threading.Event()

    def connect(self):
        try:
            print("connect to database...")
            self._client = MongoClient("mongodb://localhost:27017/")
            self._db = self._client["network_monitoring"]

            # Check MongoDB connection
            self._client.admin.command("ping")

            print("connection succeeded")
            self.is_connect = True

        except errors.ServerSelectionTimeoutError:
            print("connection failed (does the server is running?)")

        except Exception as e:
            print(f"unexpected error: {e}")

    def run(self):
        if not self.is_connect:
            print("cannot run thread before connection establishment with database")
            return

        collection = self._db[self.collection]
        while True:
            if trace_queue.empty():
                print("nothing yet...")
                time.sleep(1)
                continue

            items = trace_queue.get()
            sensor_ip, target_ip, data_plane = items
            trace_list = get_traceroute_list(data_plane)

            to_json_doc = jsonify_trace_list(sensor_ip, target_ip, trace_list)
            pprint(to_json_doc)

            result = collection.insert_one(to_json_doc)
            print("Inserted document ID:", result.inserted_id)

            time.sleep(1)

    def stop(self):
        self._stop_event.set()


if __name__ == '__main__':
    client = MongoClient("mongodb://localhost:27017/")

    # Select database
    db = client["network_monitoring"]

    # collection = db["customers"]
    # doc = {"_id": 1,"name": "gns3_home"}
    # result = collection.insert_one(doc)
    # print("Inserted document ID:", result.inserted_id)

    # items = db.customers.find_one({"name": "gns3_home"})
    # for item in items:
    #     print(item.get("_id"))


    # db.create_collection("destinations")
    # db.create_collection("customers")

    # collection = db["customers"]
    # doc = {"name": "gns3_home"}

    # result = collection.insert_one(doc)
    # print("Inserted document ID:", result.inserted_id)
    #
    #customer_id = db.get_collection({"name": "gns3_home", ""})
    #
    # print(customer_id)
    #
    # collection = db["destinations"]
    # doc = {"ip": "198.18.1.254", "customer_id": db.customers.find_one({"name": "gns3_home"}).get("_id")}
    #
    # result = collection.insert_one(doc)
    # print("Inserted document ID:", result.inserted_id)
    #
    # collection = db["customers"]
    # filter_query = {"name": "gns3_home"}
    # new_values = {"$set": {"nprobes": db.customers.find_one({"name": "gns3_home"}).get("nprobes") + 1}}
    # result_one = collection.update_one(filter_query, new_values)




