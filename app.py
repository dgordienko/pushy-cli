import json
import os
import sys
from pathlib import Path

import requests
import typer
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

app = typer.Typer()


@app.command()
def connection(connection: str):
    '''
        Уставновка подключения к оконечной точки для мобильных телефонов\n
        [base] -  основное подключение\n
        [reserv] - подключение на резервный канал

    '''
    try:

        headers = {'Content-Type': 'application/json'}
        to = os.getenv('TOPIC_SETTINGS')
        url = "{}{}".format(os.getenv('PUSHY_URL'),
                            os.getenv('PUSHY_SECRET_KEY'))
        query_path = os.path.join(
            Path(__file__).parent.absolute(), 'query', 'endpoint.json')
        with open(query_path, 'r') as _file:
            payload = json.load(_file)

        if connection == 'base':
            logger.info('Установка подключения на основной адрес')
            payload['payload']['value'] = os.getenv('BASE_ADRESS')
            payload['message'] = '{}.\n{}'.format(
                payload['message'], 'Подключен основной канал')

        elif connection == 'reserv':
            logger.info('Установка подключения на резервный адрес')
            payload['payload']['value'] = os.getenv('RESERV_ADRESS')
            payload['message'] = '{}.\n{}'.format(
                payload['message'], 'Подключен резервный канал')
        elif connection not in ['reserv', 'base']:
            raise Exception('Неизвестный тип подключения')

        body = {
            'to': to,
            'data': payload
        }
        payload = json.dumps(body, ensure_ascii=False).encode('utf-8')
        response = requests.post(url=url, data=payload, headers=headers)
        logger.info('{}{}'.format(
            'Установка параметров завершена. Код ответа - ', response.status_code))
    except Exception as exception:
        info = sys.exc_info()
        logger.error(info)
        logger.error(exception)


if __name__ == "__main__":
    app()
