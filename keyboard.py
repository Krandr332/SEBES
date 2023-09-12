import json


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
                        "label": "Погода"
                    },
                    "color": "default"
                }
            ],
            [
                {
                    "action": {
                        "type": "text",
                        "payload": "{\"button\": \"2\"}",
                        "label": "Пробка"
                    },
                    "color": "default"
                }
            ],
            [
                {
                    "action": {
                        "type": "text",
                        "payload": "{\"button\": \"2\"}",
                        "label": "Афиша"
                    },
                    "color": "default"
                }
            ],
            [
                {
                    "action": {
                        "type": "text",
                        "payload": "{\"button\": \"2\"}",
                        "label": "Валюта"
                    },
                    "color": "positive"
                }
            ]
        ]
    }
    return json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
def create_today_or_tomorrow_weather_keyboard():
    keyboard = {
        "one_time": False,
        "buttons": [
            [
                {
                    "action": {
                        "type": "text",
                        "payload": "{\"button\": \"1\"}",
                        "label": "Сегодня"
                    },
                    "color": "default"
                }
            ],
            [
                {
                    "action": {
                        "type": "text",
                        "payload": "{\"button\": \"2\"}",
                        "label": "Завтра"
                    },
                    "color": "default"
                }
            ]

        ]
    }

    return json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
def create_today_or_tomorrow_poster_keyboard():
    keyboard = {
        "one_time": False,
        "buttons": [
            [
                {
                    "action": {
                        "type": "text",
                        "payload": "{\"button\": \"1\"}",
                        "label": "Сегодня"
                    },
                    "color": "default"
                }
            ],
            [
                {
                    "action": {
                        "type": "text",
                        "payload": "{\"button\": \"2\"}",
                        "label": "Завтра"
                    },
                    "color": "default"
                }
            ]

        ]
    }

    return json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
