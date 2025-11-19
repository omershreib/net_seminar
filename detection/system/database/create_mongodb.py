from pymongo import MongoClient
from datetime import datetime

# Connect to MongoDB (adjust URI if needed)
client = MongoClient("mongodb://localhost:27017/")

# Select database
db = client["network_monitoring"]

# Drop collection if it already exists (optional, for clean setup)
db.drop_collection("traceroutes")

# Create a time series collection
db.create_collection(
    "traceroutes",
    timeseries={
        "timeField": "timestamp",   # field to store time of traceroute
        "metaField": "sensor_id",   # metadata field (sensor identifier)
        "granularity": "seconds"    # granularity of time series
    }
)



# # Reference to the collection
# collection = db["traceroutes"]
#
# # Example traceroute hops
# example_hops = [
#     {"hop": 1, "ip": "192.168.1.1", "rtts_ms": [1.2, 1.1, 1.3], "responded": True},
#     {"hop": 2, "ip": "10.0.0.1", "rtts_ms": [5.4, 5.1, 5.2], "responded": True},
#     {"hop": 3, "responded": False},  # no response (* * *)
#     {"hop": 4, "ip": "8.8.8.8", "rtts_ms": [20.3, 19.8, 20.1], "responded": True}
# ]

# # Example sensor and destination info
# sensor_id = "sensor-123"
# sensor_ip = "192.168.1.100"
# destination_ip = "8.8.8.8"
#
# # Document structure
# doc = {
#     "timestamp": datetime.now(),  # required for time series
#     "sensor_id": sensor_id,
#     "sensor_ip": sensor_ip,
#     "destination_ip": destination_ip,
#     "hops": example_hops
# }
#
# # Insert into collection
# result = collection.insert_one(doc)
# print("Inserted document ID:", result.inserted_id)
