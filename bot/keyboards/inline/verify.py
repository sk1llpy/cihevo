from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def button(token: str):
    return InlineKeyboardMarkup(
        inline_keyboard = [
            [
                InlineKeyboardButton(text = "✅ Ha, tasdiqlayman", callback_data=f"accept___{token}"),
                InlineKeyboardButton(text = "🚫 Yo'q, tasdiqlamayman", callback_data=f"reject___{token}")
            ]
        ]
    )