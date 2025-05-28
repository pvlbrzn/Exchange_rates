from flask import Flask, render_template, request

from api import get_exchange_rates
from converter import converter_currency


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Главная страница приложения:
    - Вывод курсов валют по умолчанию (USD, EUR, BYN);
    - Поиск курса валюты по аббревиатуре;
    - Конвертация курса выбранной валюты к двум другим.
    :return: HTML страницу
    """
    exchange_rates = get_exchange_rates()
    updated_at = exchange_rates[0]["Date"][:10]

    currency_dict = {cur["Cur_Abbreviation"]: cur for cur in exchange_rates}

    currency_dict["BYN"] = {
        "Cur_ID": 933,
        "Cur_Abbreviation": "BYN",
        "Cur_Name": "Белорусский рубль",
        "Cur_OfficialRate": 1.0,
        "Cur_Scale": 1
    }

    search_result = ''
    convert_result = ''
    default_cur = ['USD', 'EUR', 'RUB']

    if request.method == 'POST':
        if 'search' in request.form:
            user_input_cur = request.form.get('user_input', '').upper()
            rate = currency_dict.get(user_input_cur)
            if rate:
                search_result = f"{rate['Cur_OfficialRate']} BYN за {rate['Cur_Scale']} {user_input_cur}"
            else:
                search_result = 'Такая валюта не найдена, проверьте данные и повторите попытку.'

        elif 'convert' in request.form:
            try:
                amount = float(request.form.get('amount', 0))
                from_cur = request.form.get('from_currency')
                to_cur_1 = request.form.get('to_currency_1')
                to_cur_2 = request.form.get('to_currency_2')

                rate_from = currency_dict.get(from_cur)
                rate_to_1 = currency_dict.get(to_cur_1)
                rate_to_2 = currency_dict.get(to_cur_2)

                result_1 = converter_currency(amount, rate_from, rate_to_1)
                result_2 = converter_currency(amount, rate_from, rate_to_2)

                convert_result = (
                    f'{amount:.2f} {from_cur} = {result_1:.2f} {to_cur_1}<br>'
                    f'{amount:.2f} {from_cur} = {result_2:.2f} {to_cur_2}'
                )
            except Exception as e:
                convert_result = f'Ошибка при конвертации: {e}'

    return render_template(
        template_name_or_list='index.html',
        currency_dict=currency_dict,
        default_cur=default_cur,
        search_result=search_result,
        convert_result=convert_result,
        updated_at=updated_at,
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
