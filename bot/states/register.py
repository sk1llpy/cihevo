from aiogram.fsm.state import State, StatesGroup

class RegisterState(StatesGroup):
    full_name = State()
    phone_number = State()