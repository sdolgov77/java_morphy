from petrovich.main import Petrovich
from petrovich.enums import Gender
import csv
from morphy import Morphy, RegimeLength, Case, sex_convert, case_convert, length_convert

m = Morphy()

dept_name = 'ОЭИС'
print(m.dept(dept_name, 1))