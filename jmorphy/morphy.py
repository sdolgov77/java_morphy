import datetime
import locale
# import os
import re
from .settings import *
from jpype import startJVM, shutdownJVM, getDefaultJVMPath, JPackage, addClassPath
from num2text import num2text

# Текущая директория
# CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))
# Путь до файла с правилами округления
# DEFAULT_RULES_PATH = os.path.join(CURRENT_PATH, 'rules.json')
case_choices = [v.value for v in Case]
regime_length_choices = [v.value for v in RegimeLength]
regime_init_choices = [v.value for v in RegimeInit]
post_format_choices = [v.value for v in PostFormat]
year_add_choices = [v.value for v in YearAdd]
day_format_choices = [v.value for v in DayFormat]


class Morphy:
    def __init__(self):
        startJVM(getDefaultJVMPath(), "-ea")
        addClassPath("padeg.jar")
        Padeg = JPackage('padeg.lib').Padeg
        self.p = Padeg()

    def __del__(self):
        shutdownJVM()

    @staticmethod
    def check_phrase_case(phrase_case):
        '''Проверка правильности задания падежа'''
        if phrase_case == None:
            raise Exception('Не задан падеж!')
        if phrase_case not in case_choices:  # Case:
            raise Exception('Неверно задан падеж!')

    @staticmethod
    def check_regime_init(regime):
        '''Корректность режима вывода первой буквы'''
        if regime == None:
            raise Exception('Не задан режим вывода первой буквы!')
        if regime not in regime_init_choices:  # RegimeInit:
            raise Exception('Неверно задан режим вывода первой буквы!')

    @staticmethod
    def check_regime_init_dept(regime):
        '''Корректность режима вывода первой буквы подразделения'''
        if regime == None:
            raise Exception(
                'Не задан режим вывода первой буквы подразделения!')
        if regime not in (RegimeInit.AS_IS, RegimeInit.LOWER):
            raise Exception(
                'Неверно задан режим вывода первой буквы подразделения!')

    @staticmethod
    def check_regime_length(regime):
        '''Корректность режима длины имени'''
        if regime == None:
            raise Exception('Не задан режим вывода имени!')
        if regime not in regime_length_choices:  # RegimeLength:
            raise Exception('Неверно задан режим вывода имени!')

    @staticmethod
    def check_regime_post(regime):
        '''Корректность режима вывода должности'''
        if regime == None:
            raise Exception('Не задан режим вывода должности!')
        if regime not in post_format_choices:  # PostFormat:
            raise Exception('Неверно задан режим вывода должности!')

    @staticmethod
    def check_regime_respected(regime):
        '''Корректность режима вывода вежливого обращения'''
        if regime == None:
            raise Exception('Не задан режим вывода вежливого обращения!')
        if regime not in (0, 1):
            raise Exception('Неверно задан режим вывода вежливого обращения!')

    @staticmethod
    def get_cut(regime_length):
        '''Возвращает признак обрезания имени'''
        Morphy.check_regime_length(regime_length)
        return length_convert[regime_length][0]

    @staticmethod
    def get_reverse(regime_length):
        '''Возвращает признак обрезания имени'''
        Morphy.check_regime_length(regime_length)
        return length_convert[regime_length][1]

    @staticmethod
    def check_sex(sex):
        '''Проверка правильности задания пола'''
        if sex not in (Gender.MALE, Gender.FEMALE, None):
            raise Exception('Неверно задан пол!')

    def phrase(self, phrase, phrase_case=Case.NOMINATIVE):
        '''Склонение фразы
        применяется так же для склонения должности appointment_padeg
        '''
        if phrase_case == Case.NOMINATIVE or phrase_case == None:
            return phrase
        else:
            return self.get_appointment(phrase, phrase_case)

    def prefix_fio(self, sex, phrase_case, regime_length):
        '''Обращение перед ФИО'''
        if regime_length in (RegimeLength.RESPECTED_SHORT, RegimeLength.RESPECTED_LONG):
            if sex == Gender.FEMALE:
                return self.phrase(Respected.FEMALE, phrase_case) + ' '
            elif sex == Gender.MALE:
                return self.phrase(Respected.MALE, phrase_case) + ' '
        return ''

    def fio(self, last_name, first_name, middle_name, sex, phrase_case=Case.NOMINATIVE, regime_length=DFLT_LENGTH):
        '''Склонение ФИО, ф и о по отдельности'''
        # Если пусто ставлю значения по умолчанию, веб всегда передает все аргументы
        phrase_case = Case.NOMINATIVE if phrase_case is None else phrase_case
        regime_length = DFLT_LENGTH if regime_length is None else regime_length
        Morphy.check_sex(sex)
        if sex == None:
            sex = int()
        Morphy.check_phrase_case(phrase_case)
        return self.prefix_fio(sex, phrase_case, regime_length) + \
            str(self.get_fio(last_name if regime_length != RegimeLength.RESPECTED_SHORT else '',
                             first_name, middle_name, sex, phrase_case,
                             self.get_cut(regime_length),
                             self.get_reverse(regime_length))).lstrip()

    def fio_full(self, full_name, sex, phrase_case=Case.NOMINATIVE, regime_length=DFLT_LENGTH):
        '''Склонение ФИО, ф и о одной строкой'''
        # Если пусто ставлю значения по умолчанию, веб всегда передает все аргументы
        phrase_case = Case.NOMINATIVE if phrase_case is None else phrase_case
        regime_length = DFLT_LENGTH if regime_length is None else regime_length
        Morphy.check_sex(sex)
        Morphy.check_phrase_case(phrase_case)

        if not regime_length.strip():
            regime_length = RegimeLength.SHORT

        if regime_length == RegimeLength.RESPECTED_SHORT:
            full_name_row = re.split(r'\W+', full_name)
            if len(full_name_row) < 3:
                # если нет отчества, добавить пустую строку
                full_name_row.append('')
            if phrase_case == Case.NOMINATIVE:
                return self.prefix_fio(sex, phrase_case, regime_length) + \
                    full_name_row[1] + ' ' + full_name_row[2]
            else:
                return self.fio(full_name_row[0], full_name_row[1], full_name_row[2], sex, phrase_case, regime_length)
        elif phrase_case == Case.NOMINATIVE and regime_length in (RegimeLength.RESPECTED_LONG, RegimeLength.LONG) \
                or full_name.strip() is None:
            return self.prefix_fio(sex, phrase_case, regime_length) + full_name
        else:
            return self.prefix_fio(sex, phrase_case, regime_length) + \
                self.get_fio_p(full_name, sex, phrase_case,
                               self.get_cut(regime_length),
                               self.get_reverse(regime_length))

    def cutted_post(self, post_name):
        '''Может ли наименование должности сокращено'''
        post_name = post_name.strip()
        if post_name:
            for post in EXCL_POST:
                if post in post_name:
                    return True
        else:
            return False

    def cut_post(self, post_name, dept_long_name=None):
        '''Сокращение должности'''
        dept_name = dept_long_name.strip().lower()
        post_name = post_name.strip()
        if len(post_name) == 0 or len(dept_name) == 0:
            return post_name
        for dept, post in zip(EXCL_DEPT, EXCL_POST):
            if dept in dept_name or post in post_name:
                dept_name = dept_name.replace(dept, '')
                post_name = post_name.replace(post, '')
            if post_name.strip() == '' or dept_name.strip() == '':
                return post_name.strip()
        return post_name

    @staticmethod
    def reverse_cutted_fio(fullname, reverse):
        '''Вывод сокращенного ФИО в реверсном режиме'''
        if reverse:
            arr = fullname.split(" ")
            retval = []
            if len(arr) > 1:
                retval.append(arr[1])
            if len(arr) > 0:
                retval.append(arr[0])
                return " ".join(retval)
            else:
                return ""
        else:
            return fullname

    def get_fio_p(self, fio, sex, padeg, cut, reverse):
        if cut:
            if sex is None:
                return Morphy.reverse_cutted_fio(str(self.p.getCutFIOPadegFS(self.p.get_fio_padeg_fs_as(fio, padeg), True, 1)), reverse)
            else:
                return Morphy.reverse_cutted_fio(str(self.p.getCutFIOPadegFS(fio, sex, padeg)), reverse)
        else:
            if reverse:
                raise ValueError(
                    "Вывод полного ФИО в реверсном режиме (когда Фамилия выводится в конце) не реализован!")
            else:
                if sex is None:
                    return str(self.p.getFIOPadegFSAS(fio, padeg))
                else:
                    return str(self.p.getFIOPadegFS(fio, sex, padeg))

    def get_fio(self, last_name, first_name, middle_name, sex, padeg, cut, reverse):
        '''Склонение ФИО'''
        if cut:
            return Morphy.reverse_cutted_fio(str(self.p.getCutFIOPadeg(last_name, first_name, middle_name, sex, padeg)), reverse)
        else:
            if reverse:
                raise ValueError(
                    "Вывод полного ФИО в реверсном режиме (когда Фамилия выводится в конце) не реализован!")
            else:
                return str(self.p.getFIOPadeg(last_name, first_name, middle_name, sex, padeg))

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
            raise Exception(
                'Неверно задан режим вывода первой буквы подразделения!')

    def dept_init_lower(self, dept_name):
        return self.dept_init(dept_name, RegimeInit.LOWER)

    def correct_dept_name(self, dept_name):
        return dept_name.replace('"-"', '" - "')

    def dept(self, dept_name, phrase_case=Case.NOMINATIVE, regime_init=RegimeInit.AS_IS):
        '''Склонение подразделения'''
        # Если пусто ставлю значения по умолчанию, веб всегда передает все аргументы
        phrase_case = Case.NOMINATIVE if phrase_case is None else phrase_case
        regime_init = RegimeInit.AS_IS if regime_init is None else regime_init
        Morphy.check_phrase_case(phrase_case)
        if len(dept_name.strip()) == 0:
            return ''
        if phrase_case == Case.NOMINATIVE \
           or len(dept_name.strip()) == 0 \
           or phrase_case == Case.GENITIVE and (dept_name.startswith('УС ') or 'узел связи' in dept_name.lower()):
            return self.dept_init(self.correct_dept_name(dept_name), regime_init)
        return self.correct_dept_name(
            self.get_office(
                self.dept_init(dept_name, regime_init),
                phrase_case)
        )

    def get_appointment(self, post, padeg):
        '''Склонение должности'''
        m_post = post.replace("о-", "о&")
        delimiter = " - "
        if delimiter not in m_post:
            delimiter = "-"
            if delimiter not in m_post:
                return str(self.p.getAppointmentPadeg(post, padeg))
        sub_str = m_post.split(delimiter)
        return delimiter.join([str(self.p.getAppointmentPadeg(sub.replace("о&", "о-"), padeg)) for sub in sub_str])

    def get_office(self, dept, padeg):
        return str(self.p.getOfficePadeg(dept, padeg))

    @staticmethod
    def upper_word(word):
        '''Приведение слова к верхнему регистру, исключая аббревиатуры и разряды'''
        if re.match(r'[а-яёА-ЯЁa-zA-Z]*[А-ЯЁA-Z]+[а-яёА-ЯЁa-zA-Z]*[А-ЯЁA-Z]+[а-яёА-ЯЁa-zA-Z]*|[0-9]+[а-яёА-ЯЁa-zA-Z]+', word):
            return word
        return word.upper()

    @staticmethod
    def upper(text):
        '''Приведение предложения к верхнему регистру, исключая аббревиатуры и разряды'''
        if text.isspace() or len(text) == 0:
            return text
        return ' '.join([Morphy.upper_word(word) for word in text.split()])

    def post(self, post_name, post_suffix='', dept_long_name='', dept_name='', phrase_case=Case.NOMINATIVE,
             regime_post=DFLT_POST, regime_init_dept=DFLT_INIT_DEPT):
        '''Склонение должности в подразделении'''
        # Если пусто ставлю значения по умолчанию, веб всегда передает все аргументы
        phrase_case = Case.NOMINATIVE if phrase_case is None else phrase_case
        regime_post = DFLT_POST if regime_post is None else regime_post
        regime_init_dept = DFLT_INIT_DEPT if regime_init_dept is None else regime_init_dept
        post_name = '' if post_name is None else post_name
        post_suffix = '' if post_suffix is None else post_suffix
        dept_long_name = '' if dept_long_name is None else dept_long_name
        dept_name = '' if dept_name is None else dept_name

        Morphy.check_regime_post(regime_post)
        Morphy.check_phrase_case(phrase_case)

        l_post = post_name.strip()
        l_suffix = post_suffix.strip()
        l_dept_long = dept_long_name.strip()
        l_dept = dept_name.strip()

        l_no_dept = l_post.lower() == l_dept_long.lower() \
            or l_dept_long != '' and (
            (' ' + l_dept_long.lower()) in l_post.lower()
            or (l_dept_long.lower() + ' ') in l_post.lower()) \
            or 'доверенности' in l_post.lower() \
            or ('АО' + chr(160) + 'Связьтранснефть') in l_post

        if l_post == '' or regime_post == PostFormat.AS_IS and phrase_case == Case.NOMINATIVE:
            return post_name

        if regime_post in (PostFormat.POSSIBLE, PostFormat.SHORT, PostFormat.DEPT, PostFormat.LONG):
            if self.cutted_post(post_name) and not l_no_dept:
                if l_dept_long == '' and regime_post != PostFormat.POSSIBLE:
                    raise Exception(
                        'Для сокращения наименования должности не хватает полного наименования подразделения!')
                elif l_dept_long != '':
                    post_name = self.cut_post(l_post, l_dept_long)

        if dept_name != '':
            if (' ' + dept_name) in l_post:
                l_post = post_name.replace(' ' + dept_name, '')

        if regime_post in (PostFormat.POSSIBLE, PostFormat.DEPT):
            if l_dept == '' and regime_post == PostFormat.DEPT:
                raise Exception(
                    'Для выбранного режима отображения должности не хватает краткого наименования подразделения!')
        l_dept = self.dept(dept_name if dept_name != '' else self.dept_init(
            l_dept_long, regime_init_dept), Case.GENITIVE)

        if regime_post in (PostFormat.POSSIBLE, PostFormat.LONG) and l_dept == '':
            if l_dept_long == '':
                if regime_post == PostFormat.LONG:
                    raise Exception(
                        'Для выбранного режима отображения должности не хватает полного наименования подразделения!')
            else:
                l_dept = self.dept(self.dept_init(
                    l_dept_long, regime_init_dept), Case.GENITIVE)

        if phrase_case != Case.NOMINATIVE:
            l_post = self.get_appointment(l_post, phrase_case)
        l_post = ' '.join([l_post, l_suffix])

        if l_no_dept:
            return l_post.replace('  ', ' ')
        else:
            return (' '.join([l_post, l_dept])).replace('  ', ' ')

    def print_date(self, p_date=None, regime=DFLT_DATE, regime_day=DFLT_DAY):
        '''Печать даты'''
        locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

        def print_day():
            if regime_day == DayFormat.SHORT:
                return p_date.strftime('%-d')
            elif regime_day == DayFormat.LONG:
                return p_date.strftime('%d')
            else:
                raise Exception('Неверно задан режим вывода дня месяца!')

        def print_month():
            return p_date.strftime('%B')

        def print_year():
            if regime == None:
                raise Exception('Не задан режим вывода даты!')
            if regime == YearAdd.SHORT:
                return p_date.strftime('%Y') + ' г.'
            if regime == YearAdd.LONG:
                return p_date.strftime('%Y') + ' года'
            else:
                raise Exception('Неверно задан режим вывода даты!')

        if p_date == None:
            p_date = datetime.datetime.now()
            return '"____"___________20___' + print_year()
        return print_day() + ' ' + print_month() + ' ' + print_year()

    def print_count(self, p_cnt, sex):
        '''Печать количества прописью'''
        if sex == None:
            raise Exception('Не задан пол единицы измерения!')
        if sex not in [0, 1, 2]:  # Gender:
            raise Exception('Неверно задан пол единицы измерения!')
        if int(p_cnt) != p_cnt:
            raise Exception(
                'Вывод дробного количества в текстовом режиме не реализован!')
        if sex == Gender.MALE:
            units = (('', '', ''), 0)
        elif sex == Gender.FEMALE:
            units = (('', '', ''), 1)
        else:
            units = (('', '', ''), 2)
        return num2text(int(p_cnt), units)

    def print_count_pattern(self, p_cnt, pttrn_one, pttrn_two, pttrn_five, pttrn_null=None,
                            pttrn_only_zero=None, pttrn_only_one=None, sex=None, regime_init=None):
        '''Печать количества прописью с шаблоном
        p_cnt: количество

        pttrn_* - шаблоны
        pttrn_one: Шаблон количества, заканчивающегося на 1, исключая 11 (пр. '%s файл' - именительный падеж, ед.ч.)
        pttrn_two: Шаблон количества, заканчивающегося на 2..4, исключая 12..14 (пр. '%s файла' - родительный падеж, ед.ч)
        pttrn_five: Шаблон количества, заканчивающегося на 0, 5..9, 11..14, (пр. '%s файлов' - родительный падеж, мн.ч.)
        pttrn_null: Шаблон неопределенного количества (пр. 'ошибка получения') - если содержит %s в этом месте будет 0
        pttrn_only_zero: Шаблон для нулевого количества (пр. '%s файлов' - именительный падеж, ед.ч.) - если не заполнить, будет выведена пустая строка
        pttrn_only_one: Шаблон единичного количества (пр. '%s файл' - именительный падеж, ед.ч.) - если не заполнить, будет pttrn_one

        sex: пол единицы измерения
        regime_init: режим вывода первой буквы
        '''
        if pttrn_one is None or PTTRN_COUNT not in pttrn_one \
                or pttrn_two is None or PTTRN_COUNT not in pttrn_two \
                or pttrn_five is None or PTTRN_COUNT not in pttrn_five:
            raise Exception(
                f'В шаблоне не указан паттерн количества "{PTTRN_COUNT}"!')
        if p_cnt is None:
            if sex is None:
                l_cnt = '0'
            else:
                l_cnt = self.print_count(0, sex)
            retval = pttrn_null.replace(PTTRN_COUNT, l_cnt)
        else:
            if sex is None:
                l_cnt = str(p_cnt)
            else:
                l_cnt = self.print_count(p_cnt, sex)

            if p_cnt == 0:
                retval = pttrn_only_zero.replace(PTTRN_COUNT, l_cnt)
            else:
                if p_cnt == 1:
                    if pttrn_only_one is None:
                        retval = pttrn_one.replace(PTTRN_COUNT, l_cnt)
                    else:
                        retval = pttrn_only_one.replace(PTTRN_COUNT, l_cnt)
                elif int(p_cnt) == p_cnt:
                    str_p_cnt = str(int(p_cnt))
                    l_decade = str_p_cnt[-2]
                    l_unit = str_p_cnt[-1]
                    if l_decade == '1' or l_unit in ('0', '5', '6', '7', '8', '9'):
                        retval = pttrn_five.replace(PTTRN_COUNT, l_cnt)
                    elif l_unit == '1':
                        retval = pttrn_one.replace(PTTRN_COUNT, l_cnt)
                    else:
                        retval = pttrn_two.replace(PTTRN_COUNT, l_cnt)
                else:
                    if sex is None:
                        return pttrn_two.replace(PTTRN_COUNT, str(p_cnt))
                    else:
                        return pttrn_two.replace(PTTRN_COUNT, l_cnt)

        if regime_init is None or regime_init == RegimeInit.AS_IS:
            return retval
        elif regime_init == RegimeInit.LOWER:
            return self.init_lower(retval)
        elif regime_init == RegimeInit.UPPER:
            return self.init_upper(retval)
        else:
            raise Exception('Неверно задан режим вывода первой буквы числа!')

    def print_sum(self, p_sum, currency_code=DFLT_CURR_CODE, regime_init=RegimeInit.AS_IS):
        '''Печать денежной суммы с названием валюты'''
        if currency_code is None or currency_code not in CURRENCY:
            raise Exception('Неверно задан код валюты!')
        retval = self.print_count_pattern(
            int(p_sum),
            PTTRN_COUNT + ' ' + CURRENCY[currency_code].base_nominative,
            PTTRN_COUNT + ' ' + CURRENCY[currency_code].base_genitive,
            PTTRN_COUNT + ' ' + CURRENCY[currency_code].base_genitive_plural,
            '__________________________________________________________________________________________________________ ______',
            CURRENCY[currency_code].base_sex,
            regime_init
        )

        penny = (' ___' if p_sum is None else str(int((p_sum - int(p_sum))
                 * 100)).zfill(2)) + ' ' + CURRENCY[currency_code].penny_short

        if not retval:
            return penny.strip()

        return retval + penny

    def get_fio_padeg_fs(self, fio, sex, padeg):
        return str(self.p.getFIOPadegFS(fio, sex, padeg))

    def get_fio_padeg_fsas(self, fio, padeg):
        return str(self.p.getFIOPadegFSAS(fio, padeg))

    def get_appointment_padeg(self, post, padeg):
        return str(self.p.getAppointmentPadeg(post, padeg))

    def get_office_padeg(self, dept, padeg):
        return str(self.p.getOfficePadeg(dept, padeg))

    def get_full_appointment_padeg(self, appointment, office, padeg):
        return str(self.p.getFullAppointmentPadeg(appointment, office, padeg))
