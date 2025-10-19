from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class keyboards_text:
    TEXT_weather = 'Погода в моего городе'
    TEXT_change = 'Сменить город'
    TEXT_profile = 'Профиль'

main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=keyboards_text.TEXT_weather)],
    [KeyboardButton(text=keyboards_text.TEXT_change)],
    [KeyboardButton(text=keyboards_text.TEXT_profile)]
    ], resize_keyboard=True)