import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup


# Функция для получения погоды на сегодня или завтра
def get_weather(city, date):
    try:
        # Формируем URL для запроса погоды
        url = f'https://wttr.in/{city}?format=%C+%t+%w'

        response = requests.get(url)
        response.raise_for_status()  # Проверка на успешный статус ответа

        weather_info = response.text.strip()
        return f"Погода в городе {city} {date.capitalize()}: {weather_info}"
    except requests.exceptions.RequestException as e:
        print(f"RequestException: {e}")
        return "Произошла ошибка при выполнении запроса к сервису погоды."
    except Exception as e:
        print(f"Error getting weather: {e}")
        return "Произошла неизвестная ошибка при получении информации о погоде."


# Функция для получения мероприятий
def get_poster(city):
    try:
        base_url = f'https://afisha.yandex.ru/{city}/cinema?schedule'

        response = requests.get(base_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        events = []

        event_blocks = soup.find_all('div', class_='events-list__item')

        for event_block in event_blocks:
            event_name = event_block.find('a', class_='event__name').text.strip()
            event_date = event_block.find('time', class_='event__time').text.strip()
            event_location = event_block.find('div', class_='event__place').text.strip()
            events.append(f"Название: {event_name}\nДата: {event_date}\nМесто: {event_location}\n")

        if events:
            return '\n\n'.join(events)
        else:
            return "Мероприятия не найдены."
    except requests.exceptions.RequestException as e:
        print(f"RequestException: {e}")
        return "Произошла ошибка при выполнении запроса к Яндекс.Афише."
    except Exception as e:
        print(f"Error getting events: {e}")
        return "Произошла неизвестная ошибка при получении информации о мероприятиях."

# Пример использования


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


# Пример использования

