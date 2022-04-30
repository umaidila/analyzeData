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


class IndexPointer:
    pointers = []

    def step(self, indexShift):
        t = 1
        while True:
            if self.pointers[-t] < len(indexShift) - 1:  # указатель не в конце то двигаем в сторону конца
                self.pointers[-t] += 1
                # и сдвигаем после него те что справа
                for h in range(t - 1):
                    self.pointers[-t + h + 1] = self.pointers[-t] + h + 1
                    if self.pointers[-t + h + 1] >= len(indexShift):
                        continue
                return True
            else:
                if t == len(self.pointers):
                    return False  # если слева нет элементов чтоб двигать то заканчиваем
                else:
                    t += 1


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
                     in range(it, i + 1)]
        listValues = [listPairs[t].value for t in range(len(listPairs))]
        it = i + 1
        for pair in listPairs:
            print(pair.time, pair.value)

        if sign_index == '1':  # если начали с первого признака, значит создаем новую историю болезни
            history = History_Disease()
            signList = []

        if sign_index == '1' or sign_index == '2':  # для бинарного признака чпд 1 и еще одно
            sign = Sign()
            # для признака генерируем пять вариантов динамик

            sign.numbers_periods = [Number_periods() for j in range(5)]

            # сначала для чпд = 1
            alternative = Alternative()
            alternative.borders = [Border(0, listPairs[len(listPairs) - 1].time)]
            # sign.numbers_periods[0].alternatives.append(alternative)  # append на все элементы (пофиксить) (сначала создать объекты потом присоединять)
            sign.numbers_periods[0].alternatives = [alternative]
            # для другого чпд
            alternative = Alternative()
            num = 0  # считаем какое будет ЧПД
            listBorders = []
            for j in range(1, len(listPairs) - 1):
                if listPairs[j].value != listPairs[j + 1].value:  # если значение меняется, то это новый период динамики
                    num += 1
                    listBorders.append(Border(listPairs[j].time, listPairs[j + 1].time))
            listBorders.append([Border(0, listPairs[len(listPairs) - 1].time)])
            num += 1
            alternative.borders = listBorders
            sign.numbers_periods[num - 1].alternatives = alternative
            signList.append(sign)

        if sign_index == '3' or sign_index == '4':  # для перечислимого признака
            sign = Sign()

            sign.numbers_periods = [Number_periods() for j in range(5)]
            indexShift = []  # массив индексов, где меняются значения

            for g in range(len(listPairs) - 1):  # заполним этот массив
                if listPairs[g].value != listPairs[g + 1].value:
                    indexShift.append(g)

            for j in range(5):  # формируем множестов альтернатив для каждого периода динамики
                # с двумя работает нормально

                # случай с одним периодом разобрать отдельно
                if j == 0:
                    alternative = Alternative()
                    alternative.borders = [Border(0, listPairs[len(listPairs) - 1].time)]
                    sign.numbers_periods[0].alternatives = [alternative]
                    continue

                if len(indexShift) < j:
                    continue  # если число смен значений меньше чисел периодов, то нельзя расставить границы

                # if j == 2:
                #    continue # временно!!!!!!!!!!!!!!!

                indexPointer = IndexPointer()
                indexPointer.pointers = [j1 for j1 in range(j)]  # список итераторов по списку индексов списка значений
                listAlternatives = []  # начинается с 1
                stopFlag = True
                pointers = []
                listShift = []

                while stopFlag:
                    stopFlag1 = False
                    # проверяем, соответствует ли границы условиям существования
                    for t in indexPointer.pointers:
                        if t >= len(indexShift):  # проверка на выход за массив
                            indexPointer.step(indexShift)
                            continue

                    if stopFlag1:
                        stopFlag = indexPointer.step(indexShift)
                        continue

                    listShift = []

                    for t in indexPointer.pointers:
                        listShift.append(indexShift[t])
                    listShift = [0] + listShift + [len(listPairs) - 1]
                    ## убрать это и сделать отдельную проверку на краевых значениях

                    for t1 in range(0, len(listShift) - 2):  # проверка есть ли значения из левого периода в правом
                        for h1 in listValues[listShift[t1]:listShift[t1 + 1] + 1]:
                            if h1 in listValues[listShift[t1 + 1] + 1:listShift[t1 + 2]+1]:
                                stopFlag1 = True
                    if stopFlag1:
                        stopFlag = indexPointer.step(indexShift)
                        continue

                    # если всё хорошо делаем границы и добавляем в список альтернатив
                    alternative = Alternative()
                    listBorders = [Border(listPairs[listShift[t]].time,
                                          listPairs[listShift[t] + 1].time) for t in
                                   range(1,len(listShift)-1)]
                    listBorders.append(Border(0,listPairs[len(listPairs)-1].time))
                    alternative.borders = listBorders
                    listAlternatives.append(alternative)

                    stopFlag = indexPointer.step(indexShift)

                sign.numbers_periods[j].alternatives = listAlternatives

        if sign_index == '4':  # если прошли все рассматриваемые признаки, то добавляем в ИБ
            history.signs = signList
            history_disease.append(history)

print(5)
