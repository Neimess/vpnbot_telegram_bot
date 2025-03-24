from aiogram.fsm.state import State, StatesGroup


class RegistrationState(StatesGroup):
    waiting_for_name = State()


class AdminState(StatesGroup):
    waiting_for_user_id_lookup = State()
    waiting_for_user_id_delete = State()
    waiting_for_user_id_extend = State()
