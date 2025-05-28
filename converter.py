def converter_currency(amount, rate_from, rate_to):
    """
    Конвертирует сумму из одной валюты в другую.

    :param amount: Сумма для конвертации (Float)
    :param rate_from: Данные валюты, из которой конвертируем (dict)
    :param rate_to: Данные валюты, в которую конвертируем (dict)
    :return:
    """
    from_byn = rate_from['Cur_OfficialRate'] / rate_from['Cur_Scale']
    to_byn = rate_to['Cur_OfficialRate'] / rate_to['Cur_Scale']
    return (amount * from_byn) / to_byn
