class a:
    def __init__(self, mat):
        self.table = mat

    def deleteNone(self):
        self.table = [row for row in self.table if any(row)]

    def deleteDubles(self):
        seen = set()
        unique_arrays = []

        for array in self.table:
            array_tuple = tuple(array)
            if array_tuple not in seen:
                seen.add(array_tuple)
                unique_arrays.append(array)

        self.table = unique_arrays

    def deleteColumns(self):
        if not self.table:
            return []
        transposed = list(zip(*self.table))
        seen = set()
        unique_columns = []
        for col in transposed:
            if col not in seen:
                seen.add(col)
                unique_columns.append(col)
        result = list(map(list, zip(*unique_columns)))
        self.table = result

    def transpose(self):
        self.table = list(map(list, zip(*self.table)))

    def format(self):
        first = list()
        second = list()
        third = list()
        four = list()
        for j in range(len(self.table[0])):
            first.append(list(map(str, self.table[0][j].split()))[-1])
            second.append((self.table[1][j]).replace("-", '/'))
            third.append(self.table[2][j].replace("Нет", "0")
                         .replace("Да", "1"))
            four.append(self.table[3][j].replace(" ", "-"))
        self.table = [first, second, third, four]


def main(table):
    o = a(table)
    o.deleteColumns()
    o.deleteDubles()
    o.deleteNone()
    o.transpose()
    o.format()
    return o.table


# row[2][0:2] + '-' + row[2][3:5] + '-' + row[2][6:8]
# Пример исходной таблицы
input_table = [[None, None, None, None, None],
               ['Назар Ч. Дагидук', '99-04-20', 'Нет', "072 666-0751", "072 666-0751"],
               ['Тимур М. Цигедиди', '01-03-19', 'Нет', "414 115-0946", "414 115-0946"],
               ['Назар Ч. Дагидук', '99-04-20', 'Нет', "072 666-0751", "072 666-0751"],
               ['Давид С. Нугецман', '03-04-23', 'Да', "459 912-5036", "459 912-5036"]]

# Обработка таблицы и вывод результата
result_table = main(input_table)

print(result_table)
