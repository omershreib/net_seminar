from config import CONFIG


def get_latest_data_plane_id(collection):
    """
    Get Latest Data Plane ID

    :param collection: mongoDB MongoClient object (should equal to db['traceroutes'])
    :return an uuid string of the latest collection result's id
    """
    destination_ip = CONFIG['system']['monitor_setup']['destination_ip']
    sensor_ip = CONFIG['system']['monitor_setup']['sensor_ip']
    sensor_id = CONFIG['sensors_dict'][sensor_ip]

    mongo_projection = {'_id': 1}
    mongo_filter = {'sensor_id': sensor_id, 'destination_ip': destination_ip}
    mongo_sort = list({'timestamp': -1}.items())

    result = collection.find_one(
        filter=mongo_filter,
        projection=mongo_projection,
        sort=mongo_sort)

    return result['_id']


if __name__ == '__main__':
    from pymongo import MongoClient
    from bson import ObjectId

    # prev: 6922db3e1456de9ce70f7aa8
    # current: 6922db4f70e2244faa2a3393
    # next: 6922db531456de9ce70f7aa9

    # mongodb config
    MONGO_CLIENT_URL = CONFIG['system']['mongoDB']['client_url']
    MONGO_DATABASE = CONFIG['system']['mongoDB']['database']
    MONGO_COLLECTION = CONFIG['system']['mongoDB']['collection']

    # mongoDB connection setup
    client = MongoClient(MONGO_CLIENT_URL)
    db = client[MONGO_DATABASE]
    collection = db[MONGO_COLLECTION]

    curr_data_plane = collection.find_one({"sensor_id": 2, "_id": ObjectId("6922db531456de9ce70f7aa9")})
    print(curr_data_plane['hops'])
