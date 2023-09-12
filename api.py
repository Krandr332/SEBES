import requests

api_key = '7d935d33bd809c021d28837d720e5eb6'


# Функция для получения погоды на сегодня или завтра
def get_weather(city, date):
    try:
        base_url = 'http://api.openweathermap.org/data/2.5/forecast'
        params = {
            'q': city,
            'appid': api_key,
            'units': 'metric',  # Используйте 'imperial' для градусов по Фаренгейту
        }

        response = requests.get(base_url, params=params)
        data = response.json()

        # Проверяем, есть ли в ответе информация о погоде
        if 'list' in data:
            for forecast in data['list']:
                if date.lower() in forecast['dt_txt'].lower():
                    weather_info = forecast['main']
                    temperature = weather_info['temp']
                    humidity = weather_info['humidity']
                    return f"Погода на {date.capitalize()}: Температура: {temperature}°C, Влажность: {humidity}%"

        return "Информация о погоде не найдена."
    except requests.exceptions.RequestException as e:
        print(f"RequestException: {e}")
        return "Произошла ошибка при выполнении запроса к API погоды."
    except Exception as e:
        print(f"Error getting weather: {e}")
        return "Произошла неизвестная ошибка при получении информации о погоде."


def get_poster():
    return "aboba"


import requests


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
