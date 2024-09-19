import os

import requests
import traceback


class SheetsApi:
    def __init__(self, spreadsheet_id=None, table_name=None, api_key=None):
        self.spreadsheet_id = spreadsheet_id or os.getenv("GOOGLE_SPREADSHEET_ID")
        self.table_name = table_name or os.getenv("GOOGLE_SPREADSHEET_NAME")
        self.api_key = api_key or os.getenv("GOOGLE_SPREADSHEET_KEY")

        if not self.spreadsheet_id:
            raise ValueError("Spreadsheet ID is required")
        if not self.table_name:
            raise ValueError("Table name is required")
        if not self.api_key:
            raise ValueError("API key is required")

        self.base_url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{table_name}?alt=json&key={api_key}"

    def get_sheets(self):
        try:
            response = requests.get(self.base_url)

            if response.status_code != 200:
                raise Exception(f"google spreadsheets api request fail:{response}")

            return response.text
        except Exception:
            raise Exception(f"{traceback.format_exc()}")
