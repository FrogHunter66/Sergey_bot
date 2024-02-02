from aiogram.fsm.state import StatesGroup, State
from aiogram.filters.callback_data import CallbackData
class Choose_event(CallbackData, prefix="my"):
    cb:str
    id:int

cb1 = Choose_event(cb="choose", id=1)



class Creation(StatesGroup):
    name_event = State()


class Current(StatesGroup):
    event = State()
    current_test = State()

    event_id = State()
    setting_code = State()
    setting_passing = State()
    setting_time = State()

    type = State()
    question = State()
    variants = State()
    correct = State()
    volume_vars = State()
    num_of_correct = State()


class Current2(StatesGroup):
    event = State()
    current_test = State()

    event_id = State()
    setting_code = State()
    setting_passing = State()
    setting_time = State()

    type = State()
    question = State()
    variants = State()
    correct = State()
    volume_vars = State()
    num_of_correct = State()