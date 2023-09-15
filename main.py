import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
import json
import psycopg2
import bd
from api import *
from keyboard import *
from bd import *

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

api_key_weather = '88a577383ce048b2214323259eb7598a'

vk_session = vk_api.VkApi(token='dddce539376035fd9bf5eb91e969ef35c61da8fa84a920c3f9260974db4e1f553b29d827a234d1a03bf46')
vk = vk_session.get_api()
keyboard_states = {}


def send_message(user_id, message_text, keyboard):
    vk.messages.send(
        user_id=user_id,
        message=message_text,
        random_id=random.randint(1, 10000),
        keyboard=keyboard
    )


def handle_event(event):
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        user_id = event.user_id
        message_text = event.text
        keyboard = None

        if user_id not in keyboard_states or keyboard_states[user_id] == "start":
            handle_start(user_id, message_text)
        elif keyboard_states[user_id] == "waiting_for_city":
            handle_waiting_for_city(user_id, message_text)
        elif keyboard_states[user_id] == "waiting_for_confirmation":
            handle_waiting_for_confirmation(user_id, message_text)
        # Другие состояния и обработчики здесь


def handle_start(user_id, message_text):
    keyboard = create_start_keyboard()
    keyboard_states[user_id] = "start"

    city = vk.users.get(user_ids=user_id, fields='city')
    if city and 'city' in city[0]:
        city_name = city[0]['city']['title']
        message_text = f"Ваш текущий город: {city_name}. Если это верный город, нажмите 'Начать' для регистрации или выберите 'Изменить город', если хотите указать другой город."
        keyboard = create_start_city_correction_keyboard()
        keyboard_states[user_id] = "waiting_for_confirmation"
    else:
        message_text = "Ваш текущий город не указан в профиле. Пожалуйста, введите город:"
        keyboard_states[user_id] = "waiting_for_city"

    send_message(user_id, message_text, keyboard)


def handle_waiting_for_city(user_id, message_text):
    city = message_text.strip()
    if not check_user_existence(conn, user_id):
        if bd.register_user(conn, user_id, city):
            message_text = "Регистрация успешно завершена. Теперь вы можете воспользоваться другими функциями."
            keyboard = create_other_keyboard()
            keyboard_states[user_id] = "other"
        else:
            message_text = "Ошибка при регистрации пользователя."
    else:
        message_text = "Пользователь с таким ID уже зарегистрирован."

    send_message(user_id, message_text, keyboard)


def handle_waiting_for_confirmation(user_id, message_text):
    if message_text.lower() == "начать":
        keyboard_states[user_id] = "other"
        message_text = "Регистрация успешно завершена. Теперь вы можете воспользоваться другими функциями."
        keyboard = create_other_keyboard()

        city = vk.users.get(user_ids=user_id, fields='city')
        if city and 'city' in city[0]:
            city_name = city[0]['city']['title']
            bd.register_user(conn, user_id, city_name)
    elif message_text.lower() == "изменить город":
        message_text = "Пожалуйста, введите новый город:"
        keyboard_states[user_id] = "waiting_for_city_correction"

    send_message(user_id, message_text, keyboard)


def handle_weather_request(user_id, message_text):
    message_text = "На какой день вам интересна погода ?"
    keyboard = create_today_or_tomorrow_weather_keyboard()
    keyboard_states[user_id] = "today_or_tomorrow_weather_keyboard"
    send_message(user_id, message_text, keyboard)


def handle_weather_choice(user_id, message_text):
    if message_text.lower() == "назад":
        keyboard_states[user_id] = "other"
        handle_back(user_id)
        return  # Завершаем выполнение функции

    date = None
    if message_text.lower() == "завтра":
        date = "завтра"
    elif message_text.lower() == "сегодня":
        date = "сегодня"
    city = check_user_city(conn, user_id)

    if city:
        weather_info = get_weather(city, date)
        message_text = weather_info
    else:
        message_text = "Вы не указали свой город в профиле. Пожалуйста, укажите город и попробуйте снова."

    keyboard = create_other_keyboard()
    keyboard_states[user_id] = "other"
    send_message(user_id, message_text, keyboard)


def handle_poster_request(user_id, message_text):
    message_text = "На какой день вам нужна афиша ?"
    keyboard = create_today_or_tomorrow_poster_keyboard()
    keyboard_states[user_id] = "today_or_tomorrow_poster_keyboard"
    send_message(user_id, message_text, keyboard)


def handle_poster_choice(user_id, message_text):
    if message_text.lower() == "завтра":
        date = "завтра"
    else:
        date = "сегодня"

    city = vk.users.get(user_ids=user_id, fields='city')
    if city and 'city' in city[0]:
        city_name = city[0]['city']['title']
        poster_info = get_poster(city_name, date)
        message_text = poster_info
    else:
        message_text = "Вы не указали свой город в профиле. Пожалуйста, укажите город и попробуйте снова."

    keyboard = create_other_keyboard()
    keyboard_states[user_id] = "other"
    send_message(user_id, message_text, keyboard)


def handle_traffic_request(user_id):
    message_text = get_traffic(check_user_city(conn, user_id))
    keyboard = create_other_keyboard()
    keyboard_states[user_id] = "other"
    send_message(user_id, message_text, keyboard)


def handle_currency_request(user_id):
    message_text = parse_cbr_currency_rates()
    keyboard = create_other_keyboard()
    keyboard_states[user_id] = "other"
    send_message(user_id, message_text, keyboard)


def handle_back(user_id):
    message_text = "Вы вернулись назад."
    keyboard_states[user_id] = "other"
    keyboard = create_start_keyboard()
    send_message(user_id, message_text, keyboard)


def start_back(user_id):
    message_text = "Вы вернулись назад."
    keyboard_states[user_id] = "start"
    keyboard = create_start_city_correction_keyboard()
    send_message(user_id, message_text, keyboard)


def handle_event(event):
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        user_id = event.user_id
        message_text = event.text
        keyboard = None

        if user_id not in keyboard_states or keyboard_states[user_id] == "start" or keyboard_states[user_id] =="Вы вернулись назад.":
            handle_start(user_id, message_text)
        elif keyboard_states[user_id] == "waiting_for_city":
            handle_waiting_for_city(user_id, message_text)
        elif keyboard_states[user_id] == "waiting_for_confirmation":
            handle_waiting_for_confirmation(user_id, message_text)
        elif keyboard_states[user_id] == "today_or_tomorrow_weather_keyboard":
            handle_weather_choice(user_id, message_text)
        elif keyboard_states[user_id] == "today_or_tomorrow_poster_keyboard":
            handle_poster_choice(user_id, message_text)
        elif keyboard_states[user_id] == "other" and message_text.lower() == "погода":
            handle_weather_request(user_id, message_text)
        elif keyboard_states[user_id] == "other" and message_text.lower() == "афиша":
            handle_poster_request(user_id, message_text)
        elif keyboard_states[user_id] == "other" and message_text.lower() == "пробка":
            handle_traffic_request(user_id)
        elif keyboard_states[user_id] == "other" and message_text.lower() == "валюта":
            handle_currency_request(user_id)
        elif keyboard_states[user_id] == "other" and message_text.lower() == "назад":
            start_back(user_id)


longpoll = VkLongPoll(vk_session)

# Основной цикл обработки событий
for event in longpoll.listen():
    handle_event(event)
