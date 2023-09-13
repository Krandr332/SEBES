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
import requests
from bs4 import BeautifulSoup

def get_poster(city, date):
    try:
        # Определение даты (сегодня или завтра)
        if date.lower() == 'сегодня':
            event_date = (datetime.now() + timedelta(days=0)).date()
        elif date.lower() == 'завтра':
            event_date = (datetime.now() + timedelta(days=1)).date()
        else:
            return "Некорректно указана дата. Используйте 'сегодня' или 'завтра'."

        base_url = f'https://www.timeout.com/{city}'

        response = requests.get(base_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        events = []

        event_blocks = soup.find_all('div', class_='event-card')

        for event_block in event_blocks:
            event_date_str = event_block.find('div', class_='event-card-date').text.strip()
            event_date_obj = datetime.strptime(event_date_str, "%b %d, %Y").date()

            if event_date_obj == event_date:
                event_name = event_block.find('h3', class_='event-card-title').text.strip()
                event_location = event_block.find('div', class_='event-card-venue').text.strip()
                events.append(f"Название: {event_name}\nДата: {event_date_str}\nМесто: {event_location}\n")

                if len(events) == 5:
                    break  # Получено 5 мероприятий, выходим из цикла

        if events:
            return '\n\n'.join(events)
        else:
            return "Мероприятия не найдены."
    except requests.exceptions.RequestException as e:
        print(f"RequestException: {e}")
        return "Произошла ошибка при выполнении запроса к Time Out."
    except Exception as e:
        print(f"Error getting events: {e}")
        return "Произошла неизвестная ошибка при получении информации о мероприятиях."
# Пример использования


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

