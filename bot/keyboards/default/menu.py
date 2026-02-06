from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

async def button():
    return ReplyKeyboardMarkup(keyboard = [
        [
            KeyboardButton(text = "🛍 Katalog")
        ],
        [
            KeyboardButton(text = "😍 Aksiya"),
            KeyboardButton(text = "🛒 Buyurtmalarim")
        ],
        [
            KeyboardButton(text = "☎️ Murojaat")
        ]
    ], resize_keyboard = True, one_time_keyboard = True)