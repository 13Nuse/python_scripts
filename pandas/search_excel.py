#! Python3

import numpy
import pandas as pd



excel_file = 'pandas_workbook.xlsx'
df = pd.read_excel(excel_file)
print(df)

programmers = df['Name'].where(df['Occupation'] == 'Programmers')
print(programmers.dropna())


excel_files = ['pandas_workbook', 'pandas_workbook_2', 'pandas_workbook_3']

for individual_excel_file in excel_file:
    df: pd.read_excel(individual_excel_file)
    programmers = df['Name'].where(df['Occupation'] == 'Programmers').dropna()
    print("File Name" + individual_excel_file)
    print(programmers)
