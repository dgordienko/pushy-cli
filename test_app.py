import json
import os
from pathlib import Path

from dotenv import load_dotenv
import requests

load_dotenv()


def test_load_env():
    key = os.getenv('PUSHY_SECRET_KEY')
    assert key != None
    query_path = os.path.join(
        Path(__file__).parent.absolute(), 'query', 'endpoint.json')
    assert query_path != None
    with open(query_path, 'r') as _file:
        payload = json.load(_file)
        assert payload != None


def test_send_query():
    url = "{}{}".format(os.getenv('PUSHY_URL'), os.getenv('PUSHY_SECRET_KEY'))
    assert url != None
    query_path = os.path.join(
        Path(__file__).parent.absolute(), 'query', 'endpoint.json')
    with open(query_path, 'r') as _file:
        payload = json.load(_file)

    reserv = os.getenv('BASE_ADRESS')
    payload['payload']['value'] = reserv
    assert payload['payload']['value'] == reserv

    payload['message'] = '{}.\n{}'.format(
        payload['message'], 'Подключен основной канал')

    to = os.getenv('TOPIC_SETTINGS')
    body = {
        'to': to,
        'data': payload
    }
    payload = json.dumps(body, ensure_ascii=False).encode('utf-8')
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url=url, data=payload, headers=headers)
    assert response.status_code == 200
