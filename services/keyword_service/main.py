from dotenv import load_dotenv
from module.google_module import SheetsApi
from module.mongo_module import MongoClient
from module.kafka_module import KafkaClient
from datetime import datetime
import json


def fetch_keyword():
    try:
        google_sheets = SheetsApi()
        response = google_sheets.get_sheets()
        json_data = json.loads(response)

        if 'values' not in json_data:
            raise Exception('google spreadsheets empty')

        return [dict(zip(['key_word', 'price_start', 'price_end'], sublist))
                for sublist in {tuple(sublist) for sublist in json_data["values"]} if sublist]

    except Exception as error:
        raise Exception(f"{error}")


def save_log(key_word_list):
    try:
        db_client = MongoClient()
        db = db_client.connect()
        collection = db['key_word']

        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        db_client.insert_document(collection, {"list": key_word_list, "created_at": timestamp})
    except Exception as error:
        raise Exception(f"{error}")


def dispatch_keyword(keywords):
    try:
        kafka_client = KafkaClient()
        producer = kafka_client.create_producer()
        if producer:
            message = {}
            kafka_client.send_message(producer, "keywords_topic", message)

    except Exception as error:
        raise Exception(f"Error dispatching to Kafka: {error}")


def main():
    try:
        load_dotenv(dotenv_path="/app/config/keyword.env")

        key_word_list = fetch_keyword()

        save_log(key_word_list)

        dispatch_keyword(key_word_list)

    except Exception as error:
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] - {error}")


if __name__ == "__main__":
    main()
