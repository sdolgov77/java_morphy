import os
import re
# from petrovich.main import Petrovich
# from petrovich.enums import Gender
# import pymorphy3
# from pyphrasy.inflect import PhraseInflector
from .settings import c_respected_male, c_respected_female, RegimeLength, Case, pm_case, RegimeInit
from jpype import startJVM, shutdownJVM,getDefaultJVMPath, JPackage, addClassPath

# Текущая директория
CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))
# Путь до файла с правилами округления
DEFAULT_RULES_PATH = os.path.join(CURRENT_PATH, 'rules.json')

class Morphy:
    def __init__(self):
        # self._p = Petrovich(DEFAULT_RULES_PATH)
        # self._morph = pymorphy3.MorphAnalyzer()
        # self._inflector = PhraseInflector(self._morph)
        startJVM(getDefaultJVMPath(), "-ea")
        addClassPath("padeg.jar")
        Padeg = JPackage('padeg.lib').Padeg
        self.p = Padeg()

    def __del__(self):
        shutdownJVM()

    def get_fio(self, last_name, first_name, middle_name, sex, phrase_case=Case.NOMINATIVE, cut=False, reverse=False):
        return self.fio(last_name, first_name, middle_name, sex, phrase_case)

    def fio_stub(self, last_name, first_name, middle_name, sex, phrase_case=0, cut=False, reverse=False):
        if cut:
            pass #return reverseCuttedFIO(Padeg.getCutFIOPadeg(lastName, firstName, middleName, (sex != 0), padeg), reverse);
        else:
          if reverse:
            pass #throw new IllegalArgumentException("Вывод полного ФИО в реверсном режиме (когда Фамилия выводится в конце) не реализован!");
          else:
            return self.p.getFIOPadeg(last_name, first_name, middle_name, (int(sex) != 0), phrase_case);


    # def fio_stub(self, last_name, first_name, middle_name, sex, phrase_case=Case.NOMINATIVE, cut=False, reverse=False):
        # if phrase_case == Case.NOMINATIVE:

        #     last_name_form = last_name.strip()
        # else:
        #     last_name_form = self._p.lastname(last_name.strip(), phrase_case, sex)

        # if cut:
        #     name_form = first_name[0] + '.' 
        #     if middle_name:
        #         name_form = name_form + middle_name[0] + '.'
        # else:
        #     if phrase_case == Case.NOMINATIVE:
        #         name_form = first_name.strip() 
        #         if middle_name:
        #             name_form = name_form + ' ' + middle_name.strip()
        #     else:
        #         name_form = self._p.firstname(first_name.strip(), phrase_case, sex)
        #         if middle_name:
        #             name_form = name_form + ' ' + self._p.middlename(middle_name.strip(), phrase_case, sex)

        # if reverse:
        #     return (name_form + ' ' + last_name_form).title()
        # else:
        #     return (last_name_form + ' ' + name_form).title()
        pass
    
    def fio_stub_full(self, full_name, sex, phrase_case=Case.NOMINATIVE, cut=False, reverse=False):
        full_name_row = re.split(r'\W+', full_name)
        if len(full_name_row) >= 3:
            last_name, first_name, middle_name = full_name_row[:3]
        elif len(full_name_row) == 2:
            last_name, first_name = full_name_row
            middle_name = ''
        else:
            raise Exception('Invalid full name: ' + full_name)
        return self.fio_stub(last_name, first_name, middle_name, sex, phrase_case, cut, reverse)
    
    def prefix_fio(self, sex, phrase_case, regime_length):
        return ""

    def fio(self, last_name, first_name, middle_name, sex, phrase_case=Case.NOMINATIVE, regime_length="short"):
        return self.prefix_fio(sex, phrase_case, regime_length) + last_name + ' ' + first_name + ' ' + middle_name
    
    def correct_case(self, phrase, init_phrase):
        '''Возврат регистра в каждом слове как было в первоначальной фразе
        так же возвращает назад аббревиатуры в первоначальном виде:
        если слово длиннее одной буквы и первая и последняя буквы - заглавные, то это аббревиатура
        '''
        # words = phrase.split()
        # tokens = init_phrase.split()
        # if len(words) == len(tokens):
        #     for i in range(len(words)):
        #         if len(tokens[i]) > 1 and tokens[i][0].upper() == tokens[i][0] and tokens[i][-1].upper() == tokens[i][-1]:
        #             words[i] = tokens[i]
        #         else:
        #             words[i] = pymorphy3.shapes.restore_capitalization(words[i], tokens[i])
        #     return ' '.join(words)
        # else:
        #     return phrase
        pass

    def phrase(self, phrase, phrase_case=Case.NOMINATIVE):
        '''Склонение фразы
        применяется так же для склонения должности appointment_padeg
        '''
        if phrase_case == 0:
            return phrase
        else:
            # return self.correct_case(self._inflector.inflect(phrase, pm_case[phrase_case]), phrase)
            return self.p.getOfficePadeg(phrase, int(phrase_case))
    
    def init_lower(self, word):
        '''Приведение первой буквы к нижнему регистру'''
        return word[0].lower() + word[1:]
    
    def init_upper(self, word):
        '''Приведение первой буквы к верхнему регистру'''
        return word[0].upper() + word[1:]

    def dept_init(self, dept_name, regime_init=RegimeInit.AS_IS):
        if regime_init == RegimeInit.AS_IS:
            return dept_name
        elif len(dept_name) < 2 \
           or 'цех электросвязи' in dept_name \
           or 'ЦЭС' in dept_name \
           or 'узел связи' in dept_name \
           or 'УС' in dept_name \
           or dept_name.upper().startswith('СВЯЗЬТРАНСНЕФТЬ') \
           or dept_name.upper().startswith('АО') \
           or dept_name.startswith('УС') \
           or dept_name.upper()[:2] == dept_name[:2] \
           or dept_name[0].upper() == dept_name[0] and dept_name[2].upper() == dept_name[2] \
           or (
            ' ПТУС' in dept_name
            or 'ПТУС ' in dept_name
           ) and dept_name.upper()[:6] != 'ФИЛИАЛ':
           return dept_name
        elif regime_init == RegimeInit.LOWER:
            return self.init_lower(dept_name)
        else:
            raise Exception('Неверно задан режим вывода первой буквы подразделения!')

    def dept_init_lower(self, dept_name):
        return self.dept_init(dept_name, RegimeInit.LOWER)

    def correct_dept_name(self, dept_name):
        return dept_name.replace('"-"', '" - "')
    
    def dept(self, dept_name, phrase_case=Case.NOMINATIVE, regime_init=RegimeInit.AS_IS):
        if phrase_case == 0 \
           or len(dept_name.strip()) == 0 \
           or phrase_case == 2 and (dept_name.startswith('УС ') or 'узел связи' in dept_name.lower()):
            return self.dept_init(dept_name, regime_init)
        return self.correct_dept_name(
            self.phrase(
                self.dept_init(dept_name, regime_init), 
                phrase_case)
            )

    def upper_word(self, word):
        '''Приведение слова к верхнему регистру, исключая аббревиатуры и разряды'''
        if re.match(r'[а-яёА-ЯЁa-zA-Z]*[А-ЯЁA-Z]+[а-яёА-ЯЁa-zA-Z]*[А-ЯЁA-Z]+[а-яёА-ЯЁa-zA-Z]*|[0-9]+[а-яёА-ЯЁa-zA-Z]+', word):
            return word
        return word.upper()
    
    def upper(self, text):
        '''Приведение предложения к верхнему регистру, исключая аббревиатуры и разряды'''
        return ' '.join([self.upper_word(word) for word in text.split()])
