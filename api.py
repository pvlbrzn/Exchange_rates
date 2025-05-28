import requests


API_URL = "https://api.nbrb.by/exrates/rates?periodicity=0"


def get_exchange_rates():
    """
    Получает список текущих курсов валют НБ РБ
    :return: Список словарей с данными курса валют.
    Если ошибка запроса вернет пустой список.
    """
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f'Не удалось получить данные: {e}')
        return []
