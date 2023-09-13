import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random

from api import translate_text, get_weather, get_poster
from keyboard import *
import bd
from bd import *
import psycopg2


api_key_weather = '88a577383ce048b2214323259eb7598a'
# Параметры подключения к базе данных PostgreSQL
db_host = 'localhost'
db_port = '5432'
db_name = 'vk'
db_user = 'postgres'
db_password = '1'

# Подключение к базе данных
conn = psycopg2.connect(
    dbname=db_name,
    user=db_user,
    password=db_password,
    host=db_host,
    port=db_port
)

# Инициализация VK API
vk_session = vk_api.VkApi(token='dddce539376035fd9bf5eb91e969ef35c61da8fa84a920c3f9260974db4e1f553b29d827a234d1a03bf46')  # Замените на ваш токен VK API
vk = vk_session.get_api()
keyboard_states = {}


def send_message(user_id, message_text, keyboard):
    vk.messages.send(
        user_id=user_id,
        message=message_text,
        random_id=random.randint(1, 10000),
        keyboard=keyboard
    )


# Функция для обработки событий
def handle_event(event):
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        user_id = event.user_id
        message_text = event.text
        keyboard = None

        if user_id not in keyboard_states or keyboard_states[user_id] == "start":
            keyboard = create_start_keyboard()
            keyboard_states[user_id] = "start"

            user_info = vk.users.get(user_ids=user_id, fields='city')
            if user_info and 'city' in user_info[0]:
                city_name = user_info[0]['city']['title']
                message_text = f"Ваш текущий город: {city_name}. Если это верный город, нажмите 'Начать' для регистрации или выберите 'Изменить город', если хотите указать другой город."
                keyboard = create_start_city_correction_keyboard()
                keyboard_states[user_id] = "waiting_for_confirmation"
            else:
                message_text = "Ваш текущий город не указан в профиле. Пожалуйста, введите город:"
                keyboard_states[user_id] = "waiting_for_city"
        elif keyboard_states[user_id] == "waiting_for_city":
            city = message_text.strip()
            user_id = event.user_id

            if not check_user_existence(conn, user_id):
                if bd.register_user(conn, user_id, city):
                    message_text = "Регистрация успешно завершена. Теперь вы можете воспользоваться другими функциями."
                    keyboard = create_other_keyboard()
                    keyboard_states[user_id] = "other"
                else:
                    message_text = "Ошибка при регистрации пользователя."
            else:
                message_text = "Пользователь с таким ID уже зарегистрирован."
        elif keyboard_states[user_id] == "waiting_for_confirmation":
            if message_text.lower() == "начать":
                keyboard_states[user_id] = "other"
                message_text = "Регистрация успешно завершена. Теперь вы можете воспользоваться другими функциями."
                keyboard = create_other_keyboard()

                user_info = vk.users.get(user_ids=user_id, fields='city')
                if user_info and 'city' in user_info[0]:
                    city_name = user_info[0]['city']['title']
                    bd.register_user(conn, user_id, city_name)
            elif message_text.lower() == "изменить город":
                message_text = "Пожалуйста, введите новый город:"
                keyboard_states[user_id] = "waiting_for_city_correction"
        elif keyboard_states[user_id] == "waiting_for_city_correction":
            city = message_text.strip()
            if bd.update_user_city(conn, user_id, city):
                message_text = "Город успешно изменен. Теперь вы можете воспользоваться другими функциями."
                keyboard = create_other_keyboard()
                keyboard_states[user_id] = "other"
            else:
                message_text = "Ошибка при изменении города пользователя."
        elif keyboard_states[user_id] == "other" and message_text.lower() == "погода":
            message_text = "На какой день вам интересна погода ?"
            keyboard = create_today_or_tomorrow_weather_keyboard()
            keyboard_states[user_id] = "today_or_tomorrow_weather_keyboard"
        elif keyboard_states[user_id] == "today_or_tomorrow_weather_keyboard":
            if message_text.lower() == "завтра":
                date = "завтра"
            else:
                date = "сегодня"
            user_info = check_user_city(conn, user_id)
            print(translate_text(user_info))
            if user_info:
                weather_info = get_weather(translate_text(user_info), date)
                message_text = weather_info
            else:
                message_text = "Вы не указали свой город в профиле. Пожалуйста, укажите город и попробуйте снова."

            keyboard = create_other_keyboard()
            keyboard_states[user_id] = "other"
        elif keyboard_states[user_id] == "other" and message_text.lower() == "афиша":
            message_text = "На какой день вам нужна афиша ?"
            keyboard = create_today_or_tomorrow_poster_keyboard()
            keyboard_states[user_id] = "today_or_tomorrow_poster_keyboard"
        elif keyboard_states[user_id] == "today_or_tomorrow_poster_keyboard":
            if message_text.lower() == "завтра":
                date = "завтра"
            else:
                date = "сегодня"

            user_info = vk.users.get(user_ids=user_id, fields='city')
            if user_info and 'city' in user_info[0]:
                city_name = user_info[0]['city']['title']
                poster_info = get_poster(city_name, date)
                message_text = poster_info
            else:
                message_text = "Вы не указали свой город в профиле. Пожалуйста, укажите город и попробуйте снова."

            keyboard = create_other_keyboard()
            keyboard_states[user_id] = "other"
        elif keyboard_states[user_id] == "other" and message_text.lower() == "пробка":
            message_text = "пробки - хз"
            keyboard = create_other_keyboard()
            keyboard_states[user_id] = "other"
        elif keyboard_states[user_id] == "other" and message_text.lower() == "валюта":
            message_text = "валюта - хз"
            keyboard = create_other_keyboard()
            keyboard_states[user_id] = "other"
        else:
            keyboard = create_other_keyboard()
            keyboard_states[user_id] = "other"

        send_message(user_id, message_text, keyboard)


# Создание экземпляра Long Poll
longpoll = VkLongPoll(vk_session)

# Основной цикл обработки событий
for event in longpoll.listen():
    handle_event(event)
