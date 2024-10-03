import csv
from jmorphy import Morphy, RegimeLength, Case, l_convert

m = Morphy()
counter = 0
with open('result.csv', 'w') as csv_file:
    writer = csv.writer(csv_file, delimiter=';')
    with open('AGNLIST.csv', 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            # is_cut, is_reverse = l_convert[row['R_LENGTH']]
            # if is_cut or is_reverse:
                # continue
            morth_name = m.fio(row['FIZ_FAMILY'], row['FIZ_NAME'], row['FIZ_OTCH'], int(row['FIZ_SEX']), \
                                    int(row['P_CASE']), row['R_LENGTH'])
            if morth_name != row['RESULT']:
                # print(morth_name, ":::", row['RESULT'], ":::", row['P_CASE'])
                # print(row)
                writer.writerow([morth_name, row['RESULT'], row['P_CASE'], row['FIZ_FAMILY'], row['FIZ_NAME'], row['FIZ_OTCH']])
                counter += 1
print(counter)

# print(m.fio_stub('Иванов', 'Иван', 'Иванович', Gender.MALE, Case.DATIVE, cut=False, reverse=False))
# print(m.fio_stub_full('Иванов Иван', Gender.MALE, Case.DATIVE, cut=False, reverse=True))