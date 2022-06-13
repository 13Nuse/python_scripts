import pandas as pd

# first and last combined issues or multiple data in one cell issue
# enter workbook name below
excel_workbook = ""
# reading the workbook using pandas library
sheet1 = pd.read_excel(excel_workbook, sheet_name="Sheet1")
print(sheet1.head(10))

# empty list where it would store split data
first_name_list = []
last_name_list = []

excel_names = sheet1["First Name, Last Name"]
print(excel_names)

# general for loop could be variables could be named anything
for names in excel_names:
    first_name, last_name = names.split("", 1)
    first_name_list.append(first_name)
    last_name_list.append(last_name)

# reinserting data back into the workbook
sheet1.insert(0, "First Name", first_name_list)
sheet1.insert(1, "Last Name", last_name_list)
