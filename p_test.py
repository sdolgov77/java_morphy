# from petrovich.enums import Case, Gender
# from petrovich.main import Petrovich
import os
from morphy import Morphy, RegimeLength, Case, case_convert, length_convert

# Текущая директория
CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))
# Путь до файла с правилами округления
DEFAULT_RULES_PATH = os.path.join(CURRENT_PATH, 'morphy','rules.json')


if __name__ == '__main__':
    rows = [
        # (u'Черных', u'Алексей', u'Давыдович'),
        # (u'Матвеев', u'Денис', u'Евгеньевич'),
        # (u'Алимова', u'Алия', u'Маратовна'),
        # (u'Шурша', u'Альфия', u'Александровна', Gender.FEMALE),
        (u'Ганцгорн', u'Зульфия', u'Милошев', 0),
        # (u'Коломиец', u'Данила', u'Олегович', Gender.MALE),
        # (u'Тарлюн', u'Данила', u'Борисович', Gender.MALE),
    ]

    m = Morphy()

    for segments in rows:
        gender = None

        if len(segments) == 4:
            fname, iname, oname, gender = segments
        elif len(segments) == 3:
            fname, iname, oname = segments
        else:
            raise ValueError

        for case in [1, 2, 3]:
            print(m.fio_stub(fname, iname, oname, gender, case, False, False))
                