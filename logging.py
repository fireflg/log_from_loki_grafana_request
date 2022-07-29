import logging
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

import requests

logging.basicConfig(level='DEBUG', format='[%(levelname)s] %(asctime)s: %(message)s')


start_date = datetime.strptime('2022/06/01 10:52:19', '%Y/%m/%d %H:%M:%S')
timestamp = datetime.timestamp(start_date)
logging.debug(f'Начнем поиск с даты {start_date}, таймштамп будет {timestamp}')

for i in range(1, 1001):
    timedelta_from = timedelta(hours=i)
    timedelta_to = timedelta(hours=i+1)

    timestamp_from = datetime.timestamp(start_date + timedelta_from)
    timestamp_to = datetime.timestamp(start_date + timedelta_to)
    logging.debug(f'Поиск будет задан с {timestamp_from} по {timestamp_to}')

    url_from = str(timestamp_from)[:-2]
    url_to = str(timestamp_to)[:-2]
    base_url = 'https://grafana.monitoring.your_link/api/datasources/proxy/11/loki/api/v1'
    query_part = 'direction=BACKWARD&limit=300000&query=%7Bnamespace%3D%22highload%22%2Ccontainer%3D%22dzmbridge%22%7D'
    url = f'{base_url}/query_range?{query_part}&start={url_from}000000000&end={url_to}000000000&step=5'
    logging.debug(f'Полный урл be like {url}')

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ.get('GRAFANA_TOKEN')}"
    }
    log_request = requests.get(url=url, headers=headers)
    if log_request.status_code != 200:
        logging.error(f'Что-то пошло не так с запросом логов:\n{log_request.status_code} - {log_request.content}')
    else:
        logs = log_request.text
        logging.debug(f'Вынули кусок логов:\n{logs}')

        with open('logs_from_loki.txt', 'a') as f:
            f.write(logs + '\n')
            logging.debug('Записали в файл, поехали дальше...')
logging.info('Записал, что мог, смотри файл!')
