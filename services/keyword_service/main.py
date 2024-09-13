import os

from dotenv import load_dotenv
from module import google_spreadsheets_module
from utils import mongo
from datetime import datetime
import json


def sort_list_by_key(data):
    return sorted(data, key=lambda x: x.get('key_word', ''))


def update_search_product_key_word():
    try:
        spreadsheet_id = os.getenv("GOOGLE_SPREADSHEET_ID")
        table_name = os.getenv("GOOGLE_SPREADSHEET_NAME")
        api_key = os.getenv("GOOGLE_SPREADSHEET_KEY")

        response = google_spreadsheets_module.get_key_word(spreadsheet_id, table_name, api_key)
        json_data = json.loads(response)

        if 'values' not in json_data:
            raise Exception('google spreadsheets empty')

        key_word = [dict(zip(['key_word', 'price_start', 'price_end'], sublist))
                    for sublist in {tuple(sublist) for sublist in json_data["values"]} if sublist]

        db = mongo.connect_to_mongodb()
        collection = db['key_word']
        data = collection.find_one(sort=[('updated_at', -1)])

        if not data or not data.get('list') or sort_list_by_key(data.get('list')) != sort_list_by_key(key_word):
            now = datetime.now()
            timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
            mongo.insert_document(collection, {"list": key_word, "updated_at": timestamp})

    except Exception as error:
        raise Exception(f"{error}")


def main():
    try:
        load_dotenv(dotenv_path="/app/config/keyword.env")
        update_search_product_key_word()
    except Exception as error:
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] - {error}")


if __name__ == "__main__":
    main()
