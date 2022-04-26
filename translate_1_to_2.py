import re

import pandas
import xlwings
import random

diseases = ['Заболевание 1', 'Заболевание 2']
signs = ['Признак 1', 'Признак 2', 'Признак 3', 'Признак 4', 'Признак 5', 'Признак 6']
history_disease = ['ИБ1', 'ИБ2', 'ИБ3', 'ИБ4', 'ИБ5', 'ИБ6', 'ИБ7', 'ИБ8', 'ИБ9', 'ИБ10']

history_disease_col = []
diseases_col = []
signs_col = []
period_number_col = []
period_length_col = []
number_observation_in_period_col = []

row_num = 0

file = pandas.ExcelFile('task_1.xls')
data_excel = file.parse('1. МБЗ')
number_period_dynamic = [int(item) for item in data_excel['Unnamed: 15'][:12]]
bottom_border = [int(item) for item in data_excel['Unnamed: 25'][1:39]]
upper_border = [int(item) for item in data_excel['Unnamed: 26'][1:39]]
values_for_periods = [str(item) for item in data_excel['Unnamed: 20'][1:39]]
print(number_period_dynamic)
print(bottom_border)
print(upper_border)
print(values_for_periods)

row_index = 0
history_disease_index = 0
disease_index = 0
signs_index = 0
period_number_index = 0

while True:
    history_disease_col.append(history_disease[history_disease_index])
    diseases_col.append(diseases[disease_index])
    signs_col.append(signs[signs_index])
    period_number_col.append(period_number_index + 1)
    period_length_col.append(random.randint(bottom_border[row_index % 38], upper_border[row_index % 38]))
    number_observation_in_period_col.append(random.randint(1, 3))

    row_index += 1
    if period_number_index == number_period_dynamic[
        disease_index * 6 + signs_index] - 1:  # если прошли по всем периодам динамики переходим к след признаку
        period_number_index = 0
        signs_index += 1
        if signs_index == len(signs):  # прошли по признакам - переходим к болезни и обнуляем признаки
            signs_index = 0
            disease_index = 1 if disease_index == 0 else 0
            history_disease_index += 1
            if history_disease_index == len(history_disease):
                break
    else:
        period_number_index += 1

df1 = pandas.DataFrame({'История болезни': history_disease_col,
                        'Заболевание': diseases_col,
                        'Признак': signs_col,
                        'Номер периода динамики': period_number_col,
                        'Длина периода динимики': period_length_col,
                        'Число моментов наблюдений в периоде динамики': number_observation_in_period_col})
df1.to_excel('task_2(1).xls')

history_disease_col1 = []
diseases_col1 = []
signs_col1 = []
observation_moment_number_col1 = []
observation_moment_value_col1 = []  # доделать

row_index1 = 0
history_disease_index1 = 0
disease_index1 = 0
signs_index1 = 0
observation_moment_index1 = 0
value_row_index = 0  # индекс строки значений для периода в первой таблице
index_left = 0  # индекс, указывающий на строку в лев таблице
time_observation = 0
nt = 0  # переменная чтобы запоминать номера моментов наблюдений
number_period_dynamic_index = 0  # индекс указывающий на число периодов динамики для каждого индекса

for history_disease_index1 in range(len(history_disease)):
    for signs_index1 in range(len(signs)):
        ttime = 1  # считать время

        for number_period_dynamic_index in range(number_period_dynamic[(history_disease_index1%2) * 6 + signs_index1]):
            moments_observation = random.sample(
                range(ttime, ttime + period_length_col[index_left]),
                number_observation_in_period_col[index_left])
            moments_observation.sort()
            # создаем значения в зависимости от признака
            for i in range(len(moments_observation)):
                history_disease_col1.append(history_disease[history_disease_index1])
                diseases_col1.append(diseases[history_disease_index1%2])
                signs_col1.append(signs[signs_index1])
                observation_moment_number_col1.append(moments_observation[i])
                # otmena
                if signs_index1 == 0 or signs_index1 == 1:  # бинарный признак
                    observation_moment_value_col1.append(values_for_periods[value_row_index])
                if signs_index1 == 2 or signs_index1 == 3:  # перечислимый
                    # выбираем случайное значение из списка
                    observation_moment_value_col1.append(random.choice(values_for_periods[value_row_index].split(',')))
                if signs_index1 == 4 or signs_index1 == 5:  # интервальный
                    pairNums = [int(i) for i in re.findall(r'\d+', values_for_periods[value_row_index])]
                    observation_moment_value_col1.append(random.randint(pairNums[0], pairNums[1]))


            ttime += period_length_col[index_left]
            index_left += 1
            value_row_index += 1
            if value_row_index == len(values_for_periods):
                value_row_index = 0

df2 = pandas.DataFrame({'История болезни': history_disease_col1,
                        'Заболевание': diseases_col1,
                        'Признак': signs_col1,
                        'Время момента наблюдения': observation_moment_number_col1,
                        'Значение момента наблюдения': observation_moment_value_col1, })
df2.to_excel('task_2(2).xls')
