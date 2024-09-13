import requests
import traceback


def get_key_word(spreadsheet_id, table_name, api_key):
    try:
        if not spreadsheet_id or not table_name or not api_key:
            raise Exception(f"need parameter:spreadsheet_id({spreadsheet_id}) table_name({table_name}) key({api_key})")

        result = requests.get(
            f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{table_name}?alt=json&key={api_key}")
        if result.status_code != 200:
            raise Exception(f"google spreadsheets api request fail:{result}")

        return result.text
    except Exception:
        raise Exception(f"{traceback.format_exc()}")
