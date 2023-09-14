import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET


# Функция для получения погоды на сегодня или завтра
def word_to_date(word):
    if word == 'сегодня':
        return datetime.now().date()
    elif word == 'завтра':
        return datetime.now().date() + timedelta(days=1)
    else:
        # Если введено другое слово, вы можете вернуть None или вызвать исключение
        raise ValueError("Неподдерживаемое слово")


def get_weather(city, date):
    try:
        api_key = "cb599fda-6a9e-4b67-b722-e5740cd41ac3"
        # Преобразуем слово date в дату
        print(date)
        date_obj = word_to_date(date)

        # Формируем URL для запроса погоды
        url = f'https://api.weather.yandex.ru/v2/forecast?city={city}&extra=true&lang=ru_RU&limit=7&hours=false'
        headers = {
            'X-Yandex-API-Key': api_key
        }

        response = requests.get(url, headers=headers)
        print(response.text)
        response.raise_for_status()  # Проверка на успешный статус ответа

        weather_data = response.json()

        # Ищем информацию о погоде на заданную дату
        for day in weather_data['forecasts']:
            if day['date'] == date_obj.strftime('%Y-%m-%d'):
                temperature = day['parts']['day']['temp_avg']
                condition = day['parts']['day']['condition']
                return f"Погода в городе {city} на {date_obj.strftime('%d.%m.%Y')}: Температура: {temperature}°C"

        return f"Информация о погоде на {date_obj.strftime('%d.%m.%Y')} не найдена."
    except requests.exceptions.RequestException as e:
        print(f"RequestException: {e}")
        return "Произошла ошибка при выполнении запроса к сервису погоды."
    except Exception as e:
        print(f"Error getting weather: {e}")
        return "Произошла неизвестная ошибка при получении информации о погоде."


# Функция для получения мероприятий

def get_poster(city, date):
    return f"Афиша {date} "


def get_traffic(city):
    return "пробки "


def parse_cbr_currency_rates():
    today_date = datetime.now().strftime("%d/%m/%Y")
    url = f"https://cbr.ru/scripts/XML_daily.asp?date_req={today_date}"

    try:
        response = requests.get(url)
        response.raise_for_status()

        root = ET.fromstring(response.text)

        currency_rates = []

        for valute in root.findall('Valute'):
            code = valute.find('CharCode').text
            value = valute.find('Value').text
            value = float(value.replace(',', '.'))
            currency_rates.append((code, value))

        sorted_currency_rates = sorted(currency_rates, key=lambda x: x[1], reverse=True)
        top5_currency_rates = sorted_currency_rates[:5]

        result_string = ""
        for i, (code, rate) in enumerate(top5_currency_rates, start=1):
            result_string += f"{i}. {code}: {rate:.2f} рублей за единицу\n"

        return result_string

    except requests.exceptions.RequestException as e:
        return f"Ошибка при выполнении HTTP-запроса: {e}"
    except ET.ParseError as e:
        return f"Ошибка при парсинге XML: {e}"
    except Exception as e:
        return f"Произошла ошибка: {e}"


# Функция для перевода текста
def translate_text(text):
    url = 'https://libretranslate.de/translate'
    params = {
        'q': text,
        'source': 'ru',
        'target': 'en'  # Перевод с русского на английский
    }

    response = requests.post(url, data=params)
    translation = response.json()

    if response.status_code == 200:
        return translation['translatedText']
    else:
        print(f"Ошибка при переводе: {response.status_code}")


