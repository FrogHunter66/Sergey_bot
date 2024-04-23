import pickle
from aiogram.enums import ParseMode
from bot import bot
from aiogram import Router, F
from aiogram.types import CallbackQuery
import datetime
from filters.Old_User import Old_user
from aiogram.fsm.context import FSMContext

from set_logs1.logger_all1 import log_exceptions1
from states.fsm import User
from keyboard.users_kb.ikb_pass_test import ikb_pass_test, answer
from keyboard.users_kb.ikb_choose_quests import ikb_get_all_quests, Take_quest
from utils.db_api.quck_commands import questions, users, tests
from utils.db_api.quck_commands import results

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
            await query.message.answer(f"""☑️Вопрос <b>с единственным выбором ответа.</b>
🕒Время до заврешения теста - <b>{differ}</b>
    
{text}
{variants}""", reply_markup=kb, parse_mode=ParseMode.HTML)
        elif type_quest == 2:
            kb = await ikb_pass_test(id_quest, mark)
            await query.message.answer(f"""🔢Вопрос <b>со множественным выбором ответа.</b>
🕒Время до заврешения теста - {differ}
            
{text}
{variants}""", reply_markup=kb, parse_mode=ParseMode.HTML)
        else:
            await query.message.answer("⛔Произошла ошибка во время выполнения теста")
        await state.set_state(User.answer)
    else:
        await query.message.answer("⏰Время на выполнение теста вышло")
        await state.clear()


@router.callback_query(answer.filter(F.cb=="ikb_answer"), User.answer, Old_user())
async def take_quest(query: CallbackQuery, state: FSMContext, callback_data: answer):
    global test_result
    current_ans = callback_data.id
    data = await state.get_data()
    id_quest = data.get("current_quest")
    current_quest = await questions.get_current(id_quest)
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
        await query.message.answer("⛔Произошла ошибка во время выполнения теста")

    try:
        mark = test_result.get(id_quest)
    except:
        mark = None
    new_kb = await ikb_pass_test(id_quest, mark)
    await bot.edit_message_reply_markup(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id,
        reply_markup=new_kb,
        inline_message_id=query.inline_message_id
    )


@router.callback_query(User.answer, F.data=="ikb_save_answer", Old_user())
async def save(query: CallbackQuery, state: FSMContext):
    await state.set_state(User.choose_quest)
    data = await state.get_data()
    id_test = data.get("current_test")
    kb = await ikb_get_all_quests(id_test)
    end_time_not_serialized = data.get("time")
    end_time = deserialize_datetime(end_time_not_serialized).replace(microsecond=0)
    current_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=3)).replace(microsecond=0)
    if end_time > current_time:
        differ = (end_time - current_time)
        await query.message.answer(f"""👉Выберите вопрос
🕒Время до окончания теста - <b>{differ}</b>""", reply_markup=kb, parse_mode=ParseMode.HTML)


async def get_final_result(all_quests):
    global test_result
    lst_res = list()

    result_pluses = 0
    result_minuses = 0
    print("TEST RESULT", test_result)
    for quest in all_quests:
        if quest.type == 1:
            correct = quest.correct_answer
            variants = quest.variants
            variants = list(map(str, variants.split(".*.")))
            num = variants.index(correct) + 1

            if test_result.get(quest.id_quest) == str(num):
                result_pluses += 1
                lst_res.append(1)
            else:
                lst_res.append(0)
                result_minuses += 1
        elif quest.type == 2:
            correct = quest.correct_answer
            correct = list(map(str, correct.split(".*.")))
            variants = quest.variants
            variants = list(map(str, variants.split(".*.")))
            nums = str(test_result.get(quest.id_quest))
            print("INFO", correct, variants, nums)
            flag = True
            for i in nums:
                if variants[int(i) - 1] not in correct:
                    flag = False
                    print("FOR INCORRECT", variants[int(i) - 1])
                    break
            if flag: result_pluses += 1
            else: result_minuses += 1
    test_result.clear()
    return lst_res

@router.callback_query(User.choose_quest, F.data=="ikb_finish", Old_user())
async def save(query: CallbackQuery, state: FSMContext):
    global test_result
    data = await state.get_data()
    id_test = data.get("current_test")
    all_quests = await questions.get_questions(id_test)
    lst_res = await get_final_result(all_quests)
    pluses = lst_res.count(1)
    minuses = lst_res.count(0)
    await results.add_result(id_test=id_test, id_user=query.from_user.id, result=lst_res)
    test = await tests.get_current(id_event=1, id_test=id_test)
    if test.notifications:
        for admin in test.notifications:
            await bot.send_message(chat_id=admin, text=f"""📊Результат пользователя <b>{data.get("username") if data.get("username") else "Неопознанно"}</b>

Имя <b>{data.get("first_name")}</b>

Тест <b>{test.name}</b>:

🎯 Выполнение - <b>{(pluses / len(all_quests) * 100) // 1} % </b>

✅ Правильных ответов - <b>{pluses}</b>
    
❌ Неправильных ответов - <b>{len(all_quests) - pluses}</b>
    
    
#results""", parse_mode=ParseMode.HTML)



    await query.message.answer(f"""📊Ваш результат: 

Тест <b>{test.name}</b>:

🎯 Выполнения - <b>{(pluses / len(all_quests) * 100)//1} %</b>

✅ Правильных ответов - <b>{pluses} </b>

❌ Неправильных ответов - <b>{len(all_quests) - pluses}</b>


#results""", parse_mode=ParseMode.HTML)
    await state.clear()
