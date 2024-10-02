# from petrovich.main import Petrovich
# from petrovich.enums import Gender
import csv
from morphy import Morphy, RegimeLength, Case, case_convert, length_convert

m = Morphy()
counter = 0
with open('result.csv', 'w') as csv_file:
    writer = csv.writer(csv_file, delimiter=';')
    with open('DUAL.csv', 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            morth_dept_full = m.dept(row['NAME_FULL'], int(row['P_CASE']))
            morth_dept = m.dept(row['NAME'], int(row['P_CASE']))
            if morth_dept_full != row['RESULT_LONG'] or morth_dept != row['RESULT_SHORT']:
                # print(morth_name, ":::", row['RESULT'], ":::", row['P_CASE'])
                # print(row)
                writer.writerow([morth_dept, row['RESULT_SHORT'], morth_dept_full, row['RESULT_LONG'], row['P_CASE'], row['NAME'], row['NAME_FULL']])
                counter += 1
print(counter)

# print(m.fio_stub('Иванов', 'Иван', 'Иванович', Gender.MALE, Case.DATIVE, cut=False, reverse=False))
# print(m.fio_stub_full('Иванов Иван', Gender.MALE, Case.DATIVE, cut=False, reverse=True))