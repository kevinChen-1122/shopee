import pymongo
import os


class MongoClient:
    def __init__(self, db_host=None, db_name=None, db_port=None, db_username=None, db_password=None):
        self.db_host = db_host or os.getenv("MONGO_DB_HOST", "mongodb")
        self.db_name = db_name or os.getenv("MONGO_DB_DATABASE")
        self.db_port = db_port or int(os.getenv("MONGO_DB_PORT", 27017))
        self.db_username = db_username or os.getenv("MONGO_DB_USERNAME")
        self.db_password = db_password or os.getenv("MONGO_DB_PASSWORD")
        self.db = None
        self.client = None

    def connect(self):
        try:
            self.client = pymongo.MongoClient(self.db_host,
                                              self.db_port,
                                              username=self.db_username,
                                              password=self.db_password)
            self.db = self.client[self.db_name]
            return self.db
        except Exception as e:
            print(f"Failed to connect to MongoDB: {e}")
            return None

    def insert_document(self, collection, document):
        try:
            collection.insert_one(document)
        except Exception as e:
            print(f"Failed to insert document: {e}")

    def insert_documents(self, collection, documents):
        try:
            collection.insert_many(documents)
        except Exception as e:
            print(f"Failed to insert documents: {e}")

    def find_documents(self, collection, query=None):
        try:
            if query:
                documents = collection.find(query)
            else:
                documents = collection.find()
            return list(documents)
        except Exception as e:
            print(f"Failed to find documents: {e}")
            return []

    def update_document(self, collection, query, update_data):
        try:
            collection.update_one(query, {"$set": update_data})
        except Exception as e:
            print(f"Failed to update document: {e}")

    def delete_document(self, collection, query):
        try:
            collection.delete_one(query)
        except Exception as e:
            print(f"Failed to delete document: {e}")

    def update_documents(self, collection, query):
        try:
            bulk_operations = [pymongo.UpdateOne({"product_link": doc["product_link"]}, {"$set": doc}, upsert=True) for
                               doc in query]
            collection.bulk_write(bulk_operations)
        except Exception as e:
            print(f"Failed to replace document: {e}")
