import json
import requests


def fetch_app_access_token(app_id, app_secret):
    url = "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal/"
    headers = {"Content-Type": "application/json; charset=utf-8"}
    payload = json.dumps({"app_id": app_id, "app_secret": app_secret})
    response = requests.post(url, headers=headers, data=payload)
    return response.json().get('app_access_token')


def fetch_spreadsheet_data(access_token, spreadsheet_token, sheet_id):
    url = f"https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/values/{sheet_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    return response.json()


def format_sheet_data(data):
    return {
        row[0]: {"base_url": row[1], "api_key": row[2]}
        for row in data['data']['valueRange']['values'][1:]
    }


if __name__ == '__main__':
    sheet_data = fetch_spreadsheet_data(
        fetch_app_access_token(..., ...),
        ...,
        ...,
    )
    with open('api.json', 'w', encoding='utf-8') as f:
        json.dump(format_sheet_data(sheet_data), f, ensure_ascii=False, indent=2)
    
