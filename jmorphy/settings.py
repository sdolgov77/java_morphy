# Описание различных настроек и констант
from enum import Enum


class Respected:
    MALE = "Уважаемый"
    FEMALE = "Уважаемая"

class Gender(int, Enum):
    """Перечисление полов"""
    MALE = 0
    FEMALE = 1
    NEUTRAL = 2

class RegimeInit(str, Enum):
    """Режимы начала имени"""
    AS_IS = 'init_as_is'              # Выводить как есть
    LOWER = 'init_lower'              # Приводить первую букву к нижнему регистру
    UPPER = 'init_upper'              # Приводить первую букву к верхнему регистру

class RegimeLength(str, Enum):
  """Режимы длины имени"""
  SHORT           = 'short'           # Фамилия И.О.
  REVERSE_SHORT   = 'reverse_short'   # И.О. Фамилия
  LONG            = 'long'            # Фамилия Имя Отчество
  RESPECTED_LONG  = 'respected_long'  # Уважаемый Фамилия Имя Отчество
  RESPECTED_SHORT = 'respected_short' # Уважаемый Имя Отчество

class Case(int, Enum):
    """Перечисление падежей"""
    # Именительный
    NOMINATIVE = 1
    # Родительный
    GENITIVE = 2
    # Дательный
    DATIVE = 3
    # Винительный
    ACCUSATIVE = 4
    # Творительный
    INSTRUMENTAL = 5
    # Предложный
    PREPOSITIONAL = 6

class YearAdd(str, Enum):
   """Как дописывать год"""    
   SHORT = 'add_short_year'  # Дописывать " г." в конце даты
   LONG = 'add_long_year'   # Дописывать " года" в конце даты

class DayFormat(str, Enum):
   """Формат дня месяца"""
   SHORT = 'short'  # Опускать ведущий 0
   LONG = 'long'   # Выводить ведущий 0   

class PostFormat(str, Enum):
   """Формат вывода должности"""  
   AS_IS = 'post_as_is'  # Должность как есть
   SHORT = 'post'        # Сокращенный вариант должности
   DEPT = 'post_dept'    # Сокращенный вариант должности с кратким именем подразделения
   LONG = 'post_long'    # Сокращенный вариант должности с полным именем подразделения
   POSSIBLE = 'post_possible'  # Максимально возможную информацию на основе предоставленных данных

length_convert = {
   # cut, reverse
   RegimeLength.SHORT: (True, False),
   RegimeLength.REVERSE_SHORT: (True, True),
   RegimeLength.LONG: (False, False),
   RegimeLength.RESPECTED_LONG: (False, False),
   RegimeLength.RESPECTED_SHORT: (False, False)
}

l_convert = {
   # cut, reverse
 'short'          : (True, False),
 'reverse_short'  : (True, True),
 'long'           : (False, False),
 'respected_long' : (False, False),
 'respected_short': (False, False)
}

# Значения входных параметров по умолчанию
DFLT_POST      = PostFormat.POSSIBLE   # Режим вывода должности по умолчанию
DFLT_LENGTH    = RegimeLength.LONG     # Режим длины по умолчанию
DFLT_DATE      = YearAdd.SHORT         # Режим даты по умолчанию
DFLT_DAY       = DayFormat.SHORT       # Дописывать " года" в конце даты
DFLT_CURR_CODE = 'RUR'                 # Код валюты по умолчанию
DFLT_INIT_DEPT = RegimeInit.LOWER      # Режим вывода первой буквы подразделения по умолчанию

# Режимы вывода количества
class Count:
    """Режимы вывода количества"""
    DIGITAL = 'digital'  # Вывод количества числом
    TEXT = 'text'        # Вывод количества текстом

PTTRN_COUNT = '%s'                # Паттерн замены количества

EXCL_POST = [ 
   'цех',
   'центр',
   'филиал',
   'участок',
   'управление безопасности',
   'управление',
   'служба кадров',
   'служба',
   'отдел',
   'группа',
   'бригада',
]

EXCL_DEPT = [
   ' цеха',
   ' центра',
   'филиала',
   ' участка',
   ' управления безопасности',
   ' управления',
   ' службы кадров',
   ' службы',
   ' отдела',
   ' группы',
   ' бригады',
]