
import pandas
import xlwings

diseases = ['Заболевание 1', 'Заболевание 2']
signs = ['Признак 1', 'Признак 2', 'Признак 3', 'Признак 4', 'Признак 5', 'Признак 6']
history_disease = ['ИБ1', 'ИБ2', 'ИБ3', 'ИБ4', 'ИБ5', 'ИБ6', 'ИБ7', 'ИБ8', 'ИБ9', 'ИБ10']

file = pandas.ExcelFile('task_2(2).xls')
data_excel = file.parse('Sheet1')

length = len(data_excel)
print(length)


class Pair:

    def __init__(self, time, value):
        self.time = time
        self.value = value


class Border:
    left = 0
    right = -1
    '''
    def __init__(self, left, right):
        self.left = left
        self.right = right
    '''
    def __init__(self,right):
        self.right = right


class Alternative:
    borders = []


class Number_periods:
    alternatives = []


class Sign:
    numbers_periods = []


class History_Disease:
    signs = []


history_disease = []

history_disease_index = 1
disease_index = 1
sign_index = 1

listPairs = []

it = 0  # индекс для отмерения интервалов строк

for i in range(length):
    # сначала сдвинем индексы
    history_disease_index = data_excel['История болезни'][i][2] if len(data_excel['История болезни'][i]) == 3 else \
        data_excel['История болезни'][i][-2:]
    disease_index = data_excel['Заболевание'][i][12]
    sign_index = data_excel['Признак'][i][8]
    print(history_disease_index, ' ', disease_index, ' ', sign_index)

    # если мы на последней строчке признака, то делаем список пар
    if i == length - 1 or sign_index != data_excel['Признак'][i + 1][8]:
        # print('delo')
        listPairs = [Pair(data_excel['Время момента наблюдения'][j], data_excel['Значение момента наблюдения'][j]) for j
                     in range(it, i)]
        it = i + 1
        for pair in listPairs:
            print(pair.time, pair.value)

        if sign_index == '1':  # если начали с первого признака, значит создаем новую историю болезни
            history = History_Disease()

        if sign_index == '1' or sign_index == '2': # для бинарного признака
            sign = Sign()
            # для признака генерируем пять вариантов динамик
            sign.numbers_periods = [Number_periods() for i in range(5)]

            for i1 in range(len(sign.numbers_periods)):
                while True:
                    alternative = Alternative()
                    if i1+1 == 1: # если один период динамики то альтернатива одна
                        alternative.borders.append(Border(listPairs[len(listPairs)-1].time))
                        print(alternative.borders[0].right)
                        break
                break
