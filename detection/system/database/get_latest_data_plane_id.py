def get_latest_data_plane_id(collection):
    # draw delay chart according to latest position
    mongo_project = {
        'sensor_id': 2,
        'destination_ip': '198.18.1.13'
    }
    mongo_filter = {'sensor_id': 2, 'destination_ip': '198.18.1.13'}
    mongo_sort = list({'timestamp': -1}.items())

    result = collection.find_one(
        filter=mongo_filter,
        projection=mongo_project,
        sort=mongo_sort)

    return result['_id']