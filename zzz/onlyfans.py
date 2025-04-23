import datetime
d = datetime.datetime(2024, 2, 11, 14, 0, 0)
d1 = datetime.datetime.utcnow()
total = (d1 - d).total_seconds()
hours = total // 3600 + 3
d2 = datetime.datetime.utcnow()

setting_time = "15123123m"
current_time = datetime.datetime.utcnow() + datetime.timedelta(hours=3)
time = current_time.replace(tzinfo=datetime.timezone.utc)
end_time = current_time + datetime.timedelta(hours=33)
varss = ['1', '2', '3']
s= ''
for i in range(len(varss)):
    s += (f"{i+1}\n").join(varss[i])


def array_to_string(input_array):
    output_string = ""

    for i, element in enumerate(input_array, start=1):
        output_string += "\n{}. {}".format(i, element)

    return output_string


input_array = ["first", "second", "third", "fourth"]
result_string = array_to_string(input_array)

current_time = datetime.datetime.utcnow()
end_time = (current_time + datetime.timedelta(hours=12)).replace(microsecond=0)
current_time = current_time.replace(microsecond=0)
differ = end_time - current_time
#differ = differ.replace(tzinfo=datetime.timezone.utc, microsecond=0)
lst = ["1-3214", "2-441", "3-4412 "]

# Инициализация пустого словаря
final_set = {}

# Обработка каждого элемента списка
for element in lst:
    # Разделение элемента по тире
    parts = element.split('-')

    # Извлечение ключа и значения
    key = int(parts[0])
    val = parts[1].strip()

    # Добавление в словарь
    final_set[key] = val

# Вывод результата
d = {1:"12", 2:"123"}

variants = "Черника.*.Андрей.*.Артем.*.Никита.*.Илья"
correct = "Илья.*.Андрей.*.Черника"
variants = list(map(str, variants.split('.*.')))
correct = list(map(str, correct.split('.*.')))
nums = "125"
if variants.index("aasfdas"):
    print("yes")
else: print("no")



