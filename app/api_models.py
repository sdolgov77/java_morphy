from flask_restx import reqparse, inputs

from .extensions import api
from jmorphy.settings import RegimeLength, Case, RegimeInit, PostFormat, YearAdd, DayFormat

case_choices = [v.value for v in Case]
regime_length_choices = [v.value for v in RegimeLength]
regime_init_choices = [v.value for v in RegimeInit]
post_format_choices = [v.value for v in PostFormat]
year_add_choices = [v.value for v in YearAdd]
day_format_choices = [v.value for v in DayFormat]

fio_parser = reqparse.RequestParser()
fio_parser.add_argument("last_name", type=str, required=True,
                        help="Example - [Иванов]", location="args")
fio_parser.add_argument("first_name", type=str, required=True,
                        help="Example - [Иван]", location="args")
fio_parser.add_argument("middle_name", type=str, required=False,
                        help="Example - [Иванович]", location="args")
fio_parser.add_argument("sex", type=int, required=False,
                        help="Example - [0, 1]", location="args")
fio_parser.add_argument("phrase_case", type=int, choices=case_choices,
                        required=False, help="Example - [1]", location="args")
fio_parser.add_argument("regime_length", type=str, required=False,
                        choices=regime_length_choices, help="Example - ['short', 'long']", location="args")

full_fio_parser = reqparse.RequestParser()
full_fio_parser.add_argument("full_name", type=str, required=True,
                             help="Example - [Иванов Иван Иванович]", location="args")
full_fio_parser.add_argument(
    "sex", type=int, required=False, help="Example - [0, 1]", location="args")
full_fio_parser.add_argument("phrase_case", type=int, choices=case_choices,
                             required=False, help="Example - [1]", location="args")
full_fio_parser.add_argument("regime_length", type=str, required=False,
                             choices=regime_length_choices, help="Example - ['short', 'long']", location="args")

dept_parser = reqparse.RequestParser()
dept_parser.add_argument("dept_name", type=str, required=False,
                         help="Example - [Служба экологической безопасности]", location="args")
dept_parser.add_argument("phrase_case", type=int, choices=case_choices,
                         required=False, help="Example - [1]", location="args")
dept_parser.add_argument("regime_init", type=str, required=False, choices=[
                         'init_as_is', 'init_lower'], help="Example - ['init_as_is', 'init_lower']", location="args")

dept_init_parser = dept_parser.copy()
dept_init_parser.remove_argument("phrase_case")

dept_init_lower_parser = dept_init_parser.copy()
dept_init_lower_parser.remove_argument("regime_init")

init_parser = reqparse.RequestParser()
init_parser.add_argument("word", type=str, required=False,
                         help="Example - [Служба экологической безопасности]", location="args")


post_parser = reqparse.RequestParser()
post_parser.add_argument("post_name", type=str, required=False,
                         help="Example - [Ведущий специалист]", location="args")
post_parser.add_argument("post_suffix", type=str,
                         required=False, help="Example - []", location="args")
post_parser.add_argument("dept_long_name", type=str, required=False,
                         help="Example - [Служба экологической безопасности]", location="args")
post_parser.add_argument("dept_name", type=str, required=False,
                         help="Example - [СЭБиРП]", location="args")
post_parser.add_argument("phrase_case", type=int, choices=case_choices,
                         required=False, help="Example - [1]", location="args")
post_parser.add_argument("regime_post", type=str, required=False,
                         choices=post_format_choices, help="Example - ['short', 'long']", location="args")
post_parser.add_argument("regime_init_dept", type=str, required=False, choices=['init_as_is', 'init_lower'], help="Example - ['init_as_is', 'init_lower']",
                         location="args")

date_parser = reqparse.RequestParser()
date_parser.add_argument('p_date', type=inputs.date, required=False,
                         help="Example - [2024-12-01]", location="args")
date_parser.add_argument('regime', type=str, required=True, choices=year_add_choices,
                         help="Example - ['add_short_year', 'add_long_year']", location="args")
date_parser.add_argument('regime_day', type=str, required=True,
                         choices=day_format_choices, help="Example - ['short', 'long']", location="args")

phrase_parser = reqparse.RequestParser()
phrase_parser.add_argument('phrase', type=str, required=True,
                           help="Example - ['Просто какая-то фраза']", location="args")
phrase_parser.add_argument('phrase_case', type=int, choices=case_choices,
                           required=False, help="Example - [1]", location="args")

count_parser = reqparse.RequestParser()
count_parser.add_argument('p_cnt', type=int, required=True,
                          help="Example - [123]", location="args")
count_parser.add_argument('sex', type=int, choices=[
                          0, 1, 2], required=True, help="Example - [0, 1]", location="args")


count_pattern_parser = reqparse.RequestParser()
count_pattern_parser.add_argument('p_cnt', type=int, required=True,
                                  help="Example - [123]", location="args")
count_pattern_parser.add_argument(
    'pttrn_one', type=str, required=True, help="Example - ['%s файл']", location="args")
count_pattern_parser.add_argument(
    'pttrn_two', type=str, required=True, help="Example - ['%s файла']", location="args")
count_pattern_parser.add_argument(
    'pttrn_five', type=str, required=True, help="Example - ['%s файлов']", location="args")
count_pattern_parser.add_argument(
    'pttrn_null', type=str, required=False, help="Example - ['ошибка получения']", location="args")
count_pattern_parser.add_argument(
    'pttrn_only_zero', type=str, required=False, help="Example - ['%s файлов']", location="args")
count_pattern_parser.add_argument(
    'pttrn_only_one', type=str, required=False, help="Example - ['%s файл']", location="args")
count_pattern_parser.add_argument('sex', type=int, choices=[
    0, 1, 2], required=False, help="Example - [0, 1, 2]", location="args")
count_pattern_parser.add_argument("regime_init", type=str, required=False, choices=[
    'init_as_is', 'init_lower', 'init_upper'], help="Example - ['init_as_is', 'init_lower', 'init_upper']", location="args")

sum_parser = reqparse.RequestParser()
sum_parser.add_argument('p_sum', type=int, required=True,
                        help="Example - [123]", location="args")
sum_parser.add_argument('currency_code', type=str, required=False,
                        help="Example - [RUB]", location="args")
sum_parser.add_argument('regime_init', type=str, required=False, choices=[
                        'init_as_is', 'init_lower', 'init_upper'], help="Example - ['init_as_is', 'init_lower', 'init_upper']", location="args")

upper_parser = reqparse.RequestParser()
upper_parser.add_argument("text", type=str, required=False,
                          help="Example - [Просто какой-то текст]", location="args")

case_check_parser = reqparse.RequestParser()
case_check_parser.add_argument('phrase_case', type=int,
                               required=False, help="Example - [1]", location="args")

regime_check_parser = reqparse.RequestParser()
regime_check_parser.add_argument('regime', type=int,
                                 required=False, help="Example - [1]", location="args")

cut_post_parser = reqparse.RequestParser()
cut_post_parser.add_argument('post_name', type=str, required=True,
                             help="Example - [Ведущий специалист]", location="args")
cut_post_parser.add_argument('dept_long_name', type=str, required=False,
                             help="Example - [Служба экологической безопасности]", location="args")
