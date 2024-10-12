# -*- coding: utf-8 -*-
'''
femail_units=(('штука', 'штуки', 'штук'), 'f')
mail_units=(('рубль', 'рубля', 'рублей'), 'm')
num2text(num, femail_units)
'''

units = (
    'ноль',

    ('одна', 'один', 'одно'),
    ('две', 'два', 'два'),

    'три', 'четыре', 'пять',
    'шесть', 'семь', 'восемь', 'девять'
)

teens = (
    'десять', 'одиннадцать',
    'двенадцать', 'тринадцать',
    'четырнадцать', 'пятнадцать',
    'шестнадцать', 'семнадцать',
    'восемнадцать', 'девятнадцать'
)

tens = (
    teens,
    'двадцать', 'тридцать',
    'сорок', 'пятьдесят',
    'шестьдесят', 'семьдесят',
    'восемьдесят', 'девяносто'
)

hundreds = (
    'сто', 'двести',
    'триста', 'четыреста',
    'пятьсот', 'шестьсот',
    'семьсот', 'восемьсот',
    'девятьсот'
)

orders = (  # plural forms and gender
    # (('', '', ''), 'm'), # (('рубль', 'рубля', 'рублей'), 'm'), # (('копейка', 'копейки', 'копеек'), 'f')
    (('тысяча', 'тысячи', 'тысяч'), 0),
    (('миллион', 'миллиона', 'миллионов'), 1),
    (('миллиард', 'миллиарда', 'миллиардов'), 1),
)

minus = 'минус'


def thousand(rest, sex):
    """Converts numbers from 19 to 999"""
    prev = 0
    plural = 2
    name = []
    use_teens = rest % 100 >= 10 and rest % 100 <= 19
    if not use_teens:
        data = ((units, 10), (tens, 100), (hundreds, 1000))
    else:
        data = ((teens, 10), (hundreds, 1000))
    for names, x in data:
        cur = int(((rest - prev) % x) * 10 / x)
        prev = rest % x
        if x == 10 and use_teens:
            plural = 2
            name.append(teens[cur])
        elif cur == 0:
            continue
        elif x == 10:
            name_ = names[cur]
            if isinstance(name_, tuple):
                name_ = name_[sex]
            name.append(name_)
            if cur >= 2 and cur <= 4:
                plural = 1
            elif cur == 1:
                plural = 0
            else:
                plural = 2
        else:
            name.append(names[cur-1])
    return plural, name


def num2text(num, main_units=(('', '', ''), 1)):
    _orders = (main_units,) + orders
    if num == 0:
        return ' '.join((units[0], _orders[0][0][2])).strip()  # ноль

    rest = abs(num)
    ord = 0
    name = []
    while rest > 0:
        plural, nme = thousand(rest % 1000, _orders[ord][1])
        if nme or ord == 0:
            name.append(_orders[ord][0][plural])
        name += nme
        rest = int(rest / 1000)
        ord += 1
    if num < 0:
        name.append(minus)
    name.reverse()
    return ' '.join(name).strip()
