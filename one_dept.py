import csv
from jmorphy import Morphy, RegimeLength, Case

m = Morphy()

dept_name = 'ОЭИС'
print(m.dept(dept_name, 1))