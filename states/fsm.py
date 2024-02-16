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
    current_quest = State()

    event_id = State()
    setting_code = State()
    setting_passing = State()
    setting_time = State()

    setting_code2 = State()
    setting_passing2 = State()
    setting_time2 = State()

    rebuild_quest = State()
    type = State()
    question = State()
    variants = State()
    correct = State()

    rebuild_type = State()
    rebuild_question = State()
    rebuild_variants = State()
    rebuild_correct = State()

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

class User(StatesGroup):
    id = State()
    username = State()
    first_name = State()
    last_name = State()
    test_code = State()

    answer = State()
    current_test = State()
    current_quest = State()
    choose_quest = State()
    time = State()

    final_res = State()
    result = State()