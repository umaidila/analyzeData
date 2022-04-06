import pandas
import xlwings

classes = ['Заболевание 1','Заболевание 2']
signs = ['Признак 1','Признак 2','Признак 3','Признак 4','Признак 5','Признак 6']

history_disease_col = []
diseases_col = []
signs_col = []
period_number_col = []
period_length_col = []
number_observation_in_period_col = []

row_num = 1
bottom_line = []
upper_line = []
number_period_dynamic = []

file = pandas.ExcelFile('input.xls')
data_excel = file.parse('1. МБЗ')
print(data_excel['Unnamed: 15'][:12])

