import pickle
from bot import bot
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Router, F
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram import types
from aiogram.filters import Command
import datetime
from keyboard.ikb_actions_question import ikb_actions_qustion, ikb_actions_rebuild_qustion
from keyboard.inline_main_menu import ikb_main_menu
from keyboard.ikb_back import ikb_back
from keyboard.save_event import ikb_save
from keyboard.ikb_all_events import ikb_all_events
from filters.is_admin import Admin
from filters.is_new_user import New_User
from filters.Old_User import Old_user
from utils.db_api.quck_commands import event
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from states.fsm import Creation, Current, Current2, User
from keyboard.list_tests import ikb_all_tests, Choose_test
from keyboard.ikb_current_test import ikb_current_test
from keyboard.ikb_settings_test import ikb_settings_test
from keyboard.ikb_timer import ikb_timer, Choose_timeer
from keyboard.ikb_adding_questions import ikb_adding_questions
from keyboard.ikb_types_questions import ikb_types_of_questions
from keyboard.list_tests import ikb_all_tests
from keyboard.ikb_rebuilding_test import ikb_rebuild
from keyboard.list_questions import ikb_all_questions, Choose_quest
from keyboard.users_kb.ikb_start import ikb_start
from keyboard.users_kb.ikb_pass_test import ikb_pass_test, answer
from keyboard.users_kb.ikb_choose_quests import ikb_get_all_quests, Take_quest
from utils.db_api.quck_commands import tests, questions
from keyboard.users_kb.ikb_start_test import ikb_start_test
from keyboard.users_kb.ikb_back_code import ikb_back_code
from utils.db_api.quck_commands import users
router = Router()
test_result = {}

def array_to_string(input_array):
    output_string = ""

    for i, element in enumerate(input_array, start=1):
        output_string += "\n{}. {}".format(i, element)

    return output_string


def deserialize_datetime(serialized_dt):
    return pickle.loads(bytes.fromhex(serialized_dt))


def get_set(state):
    final = list(map(str, state.split(",")))
    # Инициализация пустого словаря
    final_set = {}

    # Обработка каждого элемента списка
    for element in final:
        # Разделение элемента по тире
        parts = element.split('-')

        # Извлечение ключа и значения
        key = int(parts[0])
        val = parts[1].strip()

        # Добавление в словарь
        final_set[key] = val
    return final_set


@router.callback_query(Take_quest.filter(F.cb=="ikb_quest"), User.choose_quest, Old_user())
async def take_quest(query: CallbackQuery, state: FSMContext, callback_data: Take_quest):
    global test_result
    id_quest = callback_data.id
    print("id_quest - ", id_quest)
    current_quest = await questions.get_current(id_quest)
    await state.update_data(current_quest=id_quest)
    text = current_quest.text
    variants = list(map(str, current_quest.variants.split(".*.")))
    variants = array_to_string(variants)
    type_quest = current_quest.type
    try:
        mark = test_result.get(id_quest)
    except:
        mark = None
    data = await state.get_data()
    end_time_not_serialized = data.get("time")
    end_time = deserialize_datetime(end_time_not_serialized).replace(microsecond=0)
    current_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=3)).replace(microsecond=0)
    if end_time > current_time:
        differ = end_time-current_time
        if type_quest == 1:
            kb = await ikb_pass_test(id_quest, mark)
            await query.message.answer(f"""Вопрос с единственным выбором ответа.
Время до заврешения теста - {differ}
    
{text}
{variants}""", reply_markup=kb)
        elif type_quest == 2:
            kb = await ikb_pass_test(id_quest, mark)

            await query.message.answer(f"""Вопрос со множественным выбором ответа.
Время до заврешения теста - {differ}
            
{text}
{variants}""", reply_markup=kb)
        else:
            await query.message.answer("Еще какой то тип вопроса")
        await state.set_state(User.answer)
    else:
        await query.message.answer("⏰Время на выполнение теста вышло")
        await state.clear()
# async def edit_message_reply_markup(
#         self,
#         chat_id: Optional[Union[int, str]] = None,
#         message_id: Optional[int] = None,
#         inline_message_id: Optional[str] = None,
#         reply_markup: Optional[InlineKeyboardMarkup] = None,
#         request_timeout: Optional[int] = None,

@router.callback_query(answer.filter(F.cb=="ikb_answer"), User.answer, Old_user())
async def take_quest(query: CallbackQuery, state: FSMContext, callback_data: answer):
    global test_result
    current_ans = callback_data.id
    data = await state.get_data()
    id_quest = data.get("current_quest")
    current_quest = await questions.get_current(id_quest)
    variants = list(map(str, current_quest.variants.split(".*.")))
    result = str(data.get("result"))
    type_quest = current_quest.type


    if type_quest == 1:
        test_result[id_quest] = str(current_ans)
        await state.update_data(result=current_ans)
    elif type_quest == 2:
        try:
            if test_result[id_quest]:
                if (test_result.get(id_quest)).count(str(current_ans)) == 0:
                    test_result[id_quest] = str(current_ans) + test_result.get(id_quest)
                else:
                    test_result[id_quest] = (test_result.get(id_quest))[:test_result.get(id_quest).index(str(current_ans))] + test_result.get(id_quest)[test_result.get(id_quest).index(str(current_ans)) + 1:]
            else:
                test_result[id_quest] = str(current_ans)
        except:
            test_result[id_quest] = str(current_ans)
    else:
        await query.message.answer("Так не бывает")

    try:
        mark = test_result.get(id_quest)
    except:
        mark = None
    print("mark ", mark)
    new_kb = await ikb_pass_test(id_quest, mark)


    await bot.edit_message_reply_markup(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id,
        reply_markup=new_kb,
        inline_message_id=query.inline_message_id
    )
    print(test_result)


@router.callback_query(User.answer, F.data=="ikb_save_answer", Old_user())
async def save(query: CallbackQuery, state: FSMContext):
    await state.set_state(User.choose_quest)
    data = await state.get_data()
    res = data.get("result")
    id_quest = data.get("current_quest")
    final = data.get("final_res")
    if res:
        if final:
            ans_final = f"{id_quest}-{res},{final}"
            await state.update_data(final_res=ans_final)
        else:
            ans_final = f"{id_quest}-{res}"
            await state.update_data(final_res=ans_final)
    else:
        if final:
            ans_final = f"{id_quest}-0,{final}"
            await state.update_data(final_res=ans_final)
        else:
            ans_final = f"{id_quest}-0"
            await state.update_data(final_res=ans_final)

    data_new = await state.get_data()
    #print("funal_res ", data_new.get("final_res"), "id_quest ", id_quest, "res ",  res)

    await state.update_data(result="")
    id_test = data.get("current_test")
    kb = await ikb_get_all_quests(id_test)
    end_time_not_serialized = data.get("time")
    end_time = deserialize_datetime(end_time_not_serialized).replace(microsecond=0)
    current_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=3)).replace(microsecond=0)
    if end_time > current_time:
        differ = (end_time - current_time)
        await query.message.answer(f"Выберите вопрос, время до окончания тестировани - {differ}", reply_markup=kb)




@router.callback_query(User.choose_quest, F.data=="ikb_finish", Old_user())
async def save(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    id_test = data.get("current_test")
    all_quests = await questions.get_questions(id_test)
    result_pluses = 0
    result_minuses = 0

    global test_result
    for quest in all_quests:
        if quest.type == 1:
            correct = quest.correct_answer
            variants = quest.variants
            variants = list(map(str, variants.split(".*.")))
            num = variants.index(correct)+1

            if test_result.get(quest.id_quest) == str(num):
                result_pluses += 1
                print("1st type good")
            else:
                result_minuses += 1
                print("1st type ploho")


        elif quest.type == 2:
            correct = quest.correct_answer
            correct = list(map(str, correct.split(".*.")))
            variants = quest.variants
            variants = list(map(str, variants.split(".*.")))
            nums = list()
            for cor in correct:
                nums.append(str(variants.index(cor)+1))


            try:
                user_answers = test_result.get(quest.id_quest)
                user_answers = [m for m in user_answers]
                flag = True
                print("2nd type zashlo")
                print("user ", user_answers)
                print("correct ", nums)
                for answer in user_answers:
                    if answer not in nums:
                        flag = False
                        result_minuses += 1
                        break
                if flag:
                    print('2nd type good')
                    result_pluses += 1
                else:
                    print('2nd type ploho')
                    result_minuses -= 1
            except:
                print("2nd type ne zachlo")
                result_minuses += 1
    test_result.clear()
    await query.message.answer(f"📊Ваш результат - {result_pluses} правильных ответов, {result_minuses} - неправильных ответов")
    await state.clear()
