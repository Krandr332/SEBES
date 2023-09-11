import json
import psycopg2
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random

import bd
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

# Инициализация VK API
vk_session = vk_api.VkApi(token ='dddce539376035fd9bf5eb91e969ef35c61da8fa84a920c3f9260974db4e1f553b29d827a234d1a03bf46')
vk = vk_session.get_api()
keyboard_states = {}

# Функция для создания клавиатуры "Начать"
def create_start_keyboard():
    keyboard = {
        "one_time": True,
        "buttons": [
            [
                {
                    "action": {
                        "type": "text",
                        "payload": "{\"button\": \"start\"}",
                        "label": "Начать"
                    },
                    "color": "primary"
                }
            ]
        ]
    }
    return json.dumps(keyboard, ensure_ascii=False).encode('utf-8')

# Функция для создания клавиатуры с кнопками "Начать", "Изменить город"
def create_start_city_correction_keyboard():
    keyboard = {
        "one_time": True,
        "buttons": [
            [
                {
                    "action": {
                        "type": "text",
                        "payload": "{\"button\": \"start\"}",
                        "label": "Начать"
                    },
                    "color": "primary"
                },
                {
                    "action": {
                        "type": "text",
                        "payload": "{\"button\": \"change_city\"}",
                        "label": "Изменить город"
                    },
                    "color": "negative"
                }
            ]
        ]
    }
    return json.dumps(keyboard, ensure_ascii=False).encode('utf-8')

# Функция для создания клавиатуры с другими кнопками
def create_other_keyboard():
    keyboard = {
        "one_time": False,
        "buttons": [
            [
                {
                    "action": {
                        "type": "text",
                        "payload": "{\"button\": \"1\"}",
                        "label": "Кнопка 1"
                    },
                    "color": "default"
                }
            ],
            [
                {
                    "action": {
                        "type": "text",
                        "payload": "{\"button\": \"2\"}",
                        "label": "Кнопка 2"
                    },
                    "color": "positive"
                }
            ]
        ]
    }
    return json.dumps(keyboard, ensure_ascii=False).encode('utf-8')

# Функция для отправки сообщения с клавиатурой
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

        # Проверяем текущее состояние клавиатуры пользователя
        if user_id not in keyboard_states or keyboard_states[user_id] == "start":
            # Если пользователь новый или в состоянии "Начать", отправляем клавиатуру "Начать"
            keyboard = create_start_keyboard()
            keyboard_states[user_id] = "start"

            # Получаем информацию о пользователе из профиля ВКонтакте
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
            # Если пользователь находится в состоянии "waiting_for_city", обрабатываем введенный город
            city = message_text.strip()
            user_id = event.user_id

            if bd.register_user(conn, user_id, city):
                message_text = "Регистрация успешно завершена. Теперь вы можете воспользоваться другими функциями."
                keyboard = create_other_keyboard()
                keyboard_states[user_id] = "other"
            else:
                message_text = "Ошибка при регистрации пользователя."
        elif keyboard_states[user_id] == "waiting_for_confirmation":
            if message_text.lower() == "начать":
                keyboard_states[user_id] = "other"
                message_text = "Регистрация успешно завершена. Теперь вы можете воспользоваться другими функциями."
                keyboard = create_other_keyboard()

                user_info = vk.users.get(user_ids=user_id, fields='city')
                bd.register_user(conn, user_id, user_info[0]['city']['title'])

            elif message_text.lower() == "изменить город":
                message_text = "Пожалуйста, введите новый город:"
                keyboard_states[user_id] = "waiting_for_city_correction"
        elif keyboard_states[user_id] == "waiting_for_city_correction":
            # Обновляем город пользователя
            city = message_text.strip()
            if bd.register_user(conn, user_id, city):
                message_text = "Город успешно изменен. Теперь вы можете воспользоваться другими функциями."
                keyboard = create_other_keyboard()
                keyboard_states[user_id] = "other"
            else:
                message_text = "Ошибка при изменении города пользователя."
        else:
            # Если пользователь в другом состоянии, отправляем клавиатуру с другими кнопками
            keyboard = create_other_keyboard()
            keyboard_states[user_id] = "other"

        send_message(user_id, message_text, keyboard)

# Создание экземпляра Long Poll
longpoll = VkLongPoll(vk_session)

# Основной цикл обработки событий
for event in longpoll.listen():
    handle_event(event)
