
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

    def __init__(self, left, right):
        self.left = left
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

        if sign_index == '1' or sign_index == '2': # для бинарного признака чпд 1 и еще одно
            sign = Sign()
            # для признака генерируем пять вариантов динамик
            sign.numbers_periods = [Number_periods() for i in range(5)]

            # сначала для чпд = 1
            alternative = Alternative()
            alternative.borders.append(Border(0,listPairs[len(listPairs)-1].time))
            sign.numbers_periods[0].alternatives.append(alternative)
            # для другого
            alternative = Alternative()
            num = 0 # считаем какое будет ЧПД
            for j in range(len(listPairs)-1):
                if listPairs[j].value != listPairs[j+1].value: # если значение меняется, то это новый период динамики
                    num+=1
                    alternative.borders.append(Border(listPairs[j].time,listPairs[j+1].time))
            sign.numbers_periods[num].alternatives.append(alternative)

            history.signs.append(sign)

        if sign_index == '4': # если прошли все признаки, то добавляем в ИБ
            history_disease.append(history)


print(5)

