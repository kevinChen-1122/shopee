import pymongo
import os

DB_HOST = os.getenv("MONGO_DB_HOST", "mongodb")
DB_NAME = os.getenv('MONGO_DB_DATABASE')
DB_PORT = int(os.getenv('MONGO_DB_PORT', 27017))
DB_USERNAME = os.getenv('MONGO_DB_USERNAME')
DB_PASSWORD = os.getenv('MONGO_DB_PASSWORD')


def connect_to_mongodb():
    try:
        client = pymongo.MongoClient(DB_HOST,
                                     DB_PORT,
                                     username=DB_USERNAME,
                                     password=DB_PASSWORD)
        db = client[DB_NAME]
        return db
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        return None


def insert_document(collection, document):
    try:
        collection.insert_one(document)
    except Exception as e:
        print(f"Failed to insert document: {e}")


def insert_documents(collection, documents):
    try:
        collection.insert_many(documents)
    except Exception as e:
        print(f"Failed to insert document: {e}")


def find_documents(collection, query=None):
    try:
        if query:
            documents = collection.find(query)
        else:
            documents = collection.find()
        return list(documents)
    except Exception as e:
        print(f"Failed to find documents: {e}")
        return []


def update_document(collection, query, update_data):
    try:
        collection.update_one(query, {"$set": update_data})
    except Exception as e:
        print(f"Failed to update document: {e}")


def delete_document(collection, query):
    try:
        collection.delete_one(query)
    except Exception as e:
        print(f"Failed to delete document: {e}")


def update_documents(collection, query):
    try:
        bulk_operations = [pymongo.UpdateOne({"product_link": doc["product_link"]}, {"$set": doc}, upsert=True) for
                           doc in query]
        collection.bulk_write(bulk_operations)
    except Exception as e:
        print(f"Failed to replace document: {e}")
