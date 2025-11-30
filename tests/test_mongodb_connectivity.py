from config import CONFIG
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import unittest

# mongodb config
MONGO_CLIENT_URL = CONFIG['system']['mongoDB']['client_url']
MONGO_DATABASE = CONFIG['system']['mongoDB']['test_database']
MONGO_COLLECTION = CONFIG['system']['mongoDB']['collection']


class TestMongoDBConnectivity(unittest.TestCase):

    def setUp(self):
        self.database_name = MONGO_DATABASE
        self.collection_name = MONGO_COLLECTION

        try:
            self.client = MongoClient(MONGO_CLIENT_URL)
            self.client.admin.command("ping")

        except ConnectionFailure:
            self.client = None
            self.skipTest("unable to connect to mongoDB")

    def tearDown(self):
        if self.client:
            self.client.close()

    def test_connection(self):
        self.assertIsNotNone(self.client)

    def test_database_exists(self):
        dbs = self.client.list_database_names()
        self.assertIn(self.database_name, dbs, f"database '{self.database_name}' does not exist")

    def test_collection_exists(self):
        collections = self.client[self.database_name].list_collection_names()
        self.assertIn(self.collection_name, collections, f"collection '{self.collection_name}' does not exist")
