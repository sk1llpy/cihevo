import datetime

from aiogram import types, html, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from bot.routers import users as router
from bot.keyboards.default import menu, contact
from bot.keyboards.inline import verify
from bot.decorators import create_session
from bot.states.register import RegisterState
from bot.cache.redis import RedisCache

from sqlalchemy.orm import Session
from db import repository as repo


@router.message(Command("start"))
@create_session
async def start_handler(message: types.Message, state: FSMContext, session: Session):
    cache = RedisCache(300)
    
    spltd = message.text.split()
    if len(spltd) == 2:
        token = spltd[-1]
        token_data = await cache.get_from_cache(f"login_token:{token}")
        datetime_now = datetime.datetime.utcnow()
        
        if token_data: 
            expired = datetime_now > datetime.datetime.fromisoformat(token_data["expires_at"])
            if not expired:
                await message.answer(text=html.bold("Akkauntga web-sayt orqali kirishni tasdiqlaysizmi? ✅"), reply_markup = await verify.button(token = token))
            else:
                await message.answer(text=html.bold("Kirish uchun berilgan vaqt tugagan. 🚫"))
        else:
            await message.answer(text=html.bold("Kirish uchun berilgan vaqt tugagan. 🚫"))

        return
        
    user_is_exist = repo.UsersTableRepository().is_exist("tg_id", value=str(message.from_user.id), session=session)
    
    if user_is_exist:
        text = html.bold("CIHEVO Telegram botiga xush kelibsiz, kerakli bo'limni tanlang. 👇")
        
        await message.answer(text = text, reply_markup = await menu.button())
    else:
        text = html.bold("Ro'yhatdan o'tish uchun ism-familyangizni kiriting, masalan: Abdullayev Bekzod. 👇")
        
        await state.set_state(RegisterState.full_name)
        await message.answer(text = text, reply_markup=types.ReplyKeyboardRemove())


@router.callback_query(lambda call: call.data.startswith("accept") or call.data.startswith("deny"))
async def verify_token_handler(call: types.CallbackQuery):
    cache = RedisCache(expire=300)
    data = call.data
    token = data.split("___")[-1]
    token_data = await cache.get_from_cache(f"login_token:{token}")
    
    if data.startswith("accept"):
        token_data["verified"] = True
        token_data["user_id"] = str(call.from_user.id)
        await cache.put_to_cache(url=f"login_token:{token}", data=token_data)
        await call.message.edit_text(text=html.bold("Kirish muvvafaqiyatli tasdiqlandi! ✅"))
    else:
        await call.message.edit_text(text=html.bold("Kirish bekor qilindi. 🚫"))


@router.message(F.content_type == types.ContentType.TEXT, StateFilter(RegisterState.full_name))
async def full_name_handler(message: types.Message, state: FSMContext):
    first_name = None
    last_name = None
    splitted_text = message.text.split()
    
    if len(splitted_text) in (1,2):
        first_name = splitted_text[0]
        if len(splitted_text) == 2:
            last_name = splitted_text[1]

        await state.update_data(first_name = first_name, last_name = last_name)
        await state.set_state(RegisterState.phone_number)
        
        await message.answer(text = html.bold("Telefon raqamingizni yuboring. 📲"), reply_markup = await contact.button())
    else:
        await message.answer(text = html.bold("Siz notogri formatda kiritdingiz, iltimos qaytadan kiriting. ❌"))


@router.message(F.content_type == types.ContentType.CONTACT, StateFilter(RegisterState.phone_number))
@create_session
async def phone_number_handler(message: types.Message, state: FSMContext, session: Session):
    phone = message.contact.phone_number
    
    if not phone.startswith("+"):
        phone = f"+{phone}"
    
    data = await state.get_data()
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    
    text = html.bold("CIHEVO Telegram botiga xush kelibsiz, kerakli bo'limni tanlang. 👇")
    
    await repo.UsersTableRepository().create_user(
        data = {
            "tg_id": message.from_user.id,
            "tg_username": message.from_user.username,
            "tg_full_name": message.from_user.full_name,
            "first_name": first_name, 
            "last_name": last_name,
            "phone_number": phone
        },
        session=session
    )
    await state.clear()
    await message.answer(text=text, reply_markup = await menu.button())


@router.message(F.text, F.chat.type == "private")
async def website_handler(message: types.Message):
    await message.answer(text=f"""<b>Katalogga kirish uchun bosing!</b>""", reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text=f"Katalog", web_app=types.WebAppInfo(url="https://cihevoboutique.uz"))]]))
    