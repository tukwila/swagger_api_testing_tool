#!/usr/bin/env python3
# encoding: utf-8
'''
According to equivalence partition method, generate valid and invalid testing data based on and different parameter type: VARCHAR2,
number,date,file,enum
Created on Jun 23, 2021
@author: Guangli.bao
'''
import datetime
import time
from common_tools import utils
from log import logger as logging
import random
import copy
from datetime import date
from datetime import timedelta

def get_char_pools(valid_char):
    '''
    @summary: generate different kinds of characters pools
    @param valid_char: valid characters in user input
    @return: valid_char_pool, invalid_char_pool, valid_ascii_pool, invalid_ascii_pool
    '''
    valid_char_pool = []
    invalid_char_pool = []
    if 'lowercase' in valid_char:
        valid_char_pool += utils.LOWERCASE
        valid_char.remove('lowercase')
    else:
        invalid_char_pool += utils.LOWERCASE
    if 'uppercase' in valid_char:
        valid_char_pool += utils.UPPERCASE
        valid_char.remove('uppercase')
    else:
        invalid_char_pool += utils.UPPERCASE
    if 'digits' in valid_char:
        valid_char_pool += utils.DIGITS
        valid_char.remove('digits')
    else:
        invalid_char_pool += utils.DIGITS
    valid_ascii_pool = []
    invalid_ascii_pool = []
    markers = copy.deepcopy(utils.OTHERMARERS)
    if len(valid_char) != 0:
        for i in valid_char:
            if i in utils.OTHERMARERS:
                valid_ascii_pool.append(i)
                markers.remove(i)
    for j in markers:
        invalid_ascii_pool.append(j)
        invalid_char_pool.append(j)
    return valid_char_pool, invalid_char_pool, valid_ascii_pool, invalid_ascii_pool

def generate_valid_length_string(valid_char_pool, valid_ascii_pool, parameter_range_min, parameter_range_max):
    '''
    @summary: generate valid string in correct length
    @param valid_char_pool: valid characters
    @param valid_ascii_pool: valid ascii characters
    @param parameter_range_min: minimum length string
    @param parameter_range_max: maximum length string
    @return: one valid length string
    '''
    random_length_str = ''
    if len(valid_ascii_pool) == 0:
        random_length_str = ''.join(
            random.sample(valid_char_pool, random.randrange(parameter_range_min, parameter_range_max, 1)))
    if len(valid_ascii_pool) == 1:
        random_list = random.sample(valid_char_pool, random.choice(range(parameter_range_min, parameter_range_max - 1)))
        random_list += valid_ascii_pool
        random.shuffle(random_list)
        random_length_str = ''.join(random_list)
    if len(valid_ascii_pool) > 1:
        random_length = random.choice(range(1, len(valid_ascii_pool)))
        random_valid_ascii_pool = random.sample(valid_char_pool, random_length)
        random_list = random.sample(valid_char_pool, random.choice(range(parameter_range_min, parameter_range_max -
                                                                         random_length)))
        random_list += random_valid_ascii_pool
        random.shuffle(random_list)
        random_length_str = ''.join(random_list)
    return random_length_str

def generate_invalid_length_string(invalid_char_pool, invalid_ascii_pool, parameter_range_min, parameter_range_max):
    '''
    @summary: generate invalid string in incorrect length
    @param invalid_char_pool: invalid characters
    @param invalid_ascii_pool: invalid ascii characters
    @param parameter_range_min: minimum length string
    @param parameter_range_max: maximum length string
    @return: one invalid length string
    '''
    if len(invalid_ascii_pool) == 0:
        invalid_random_length_str = ''.join(
            random.sample(invalid_char_pool, random.randrange(parameter_range_min, parameter_range_max, 1)))
    if len(invalid_ascii_pool) == 1:
        invalid_random_list = random.sample(invalid_char_pool, random.choice(range(parameter_range_min,
                                                                                   parameter_range_max - 1)))
        invalid_random_list += invalid_ascii_pool
        random.shuffle(invalid_random_list)
        invalid_random_length_str = ''.join(invalid_random_list)
    if len(invalid_ascii_pool) > 1:
        random_length = random.choice(range(parameter_range_min, min(len(invalid_char_pool), parameter_range_max)))
        random_Invalid_str = random.sample(invalid_char_pool, random_length)
        random.shuffle(random_Invalid_str)
        invalid_random_length_str = ''.join(random_Invalid_str)
    return invalid_random_length_str

def generate_varchar_testing_data(parameter, varchar2_equivalence_partition_basic):
    '''
    @summary: generate equivalence partition and testing data based on varchar2 type
    @param parameter: tested parameter
    @param varchar2_equivalence_partition_basic: basic dict
    @return: equivalence partition dict include testing data
    '''
    temp_dict = {parameter['parameterName']: {}}
    valid_equivalence_partition_list = []
    invalid_equivalence_partition_list = []
    parameter_range_min = parameter['parameterRange'][0]
    parameter_range_max = parameter['parameterRange'][1]
    if_null = parameter['ifNull']
    valid_char = copy.deepcopy(parameter['validChar'])
    case_sense = parameter['caseSensitive']
    valid_char_pool, invalid_char_pool, valid_ascii_pool, invalid_ascii_pool = get_char_pools(valid_char)

    # valid: generate the shortest/longest_str string based on range
    shortest_str = ''.join(random.sample(valid_char_pool, parameter_range_min))
    longest_str = ''.join(random.sample(valid_char_pool, parameter_range_max))

    # valid: random length string include other ascii markers
    random_length_str = generate_valid_length_string(valid_char_pool, valid_ascii_pool, parameter_range_min,
                                                     parameter_range_max)
    # valid or invalid based on if_null
    if_null_list = ['None']
    if if_null is True:
        invalid_equivalence_partition_list += if_null_list
        varchar2_equivalence_partition_basic[parameter['parameterName']]['invalid_equivalence_partition']['ifNull'] = \
            if_null_list
    else:
        valid_equivalence_partition_list += if_null_list
        varchar2_equivalence_partition_basic[parameter['parameterName']]['valid_equivalence_partition']['ifNull'] = \
            if_null_list
    # valid: generate string based on case_sense
    origin_case_sense_str = ''.join(
        random.sample(valid_char_pool, random.randrange(parameter_range_min, parameter_range_max, 1)))
    reverse_case_sense_str = origin_case_sense_str.swapcase()
    if case_sense is True:
        varchar2_equivalence_partition_basic[parameter['parameterName']]['valid_equivalence_partition']['caseSensitive'] \
            = [origin_case_sense_str, reverse_case_sense_str]
        varchar2_equivalence_partition_basic[parameter['parameterName']]['invalid_equivalence_partition'][
            'caseSensitive'] \
            = [origin_case_sense_str, origin_case_sense_str]
    else:
        varchar2_equivalence_partition_basic[parameter['parameterName']]['invalid_equivalence_partition'][
            'caseSensitive'] \
            = [origin_case_sense_str, origin_case_sense_str]

    # invalid: generate the less than shortest/more than longest_str string based on range
    less_than_shortest_str = ''.join(random.sample(valid_char_pool, parameter_range_min - 1))
    more_than_longest_str = ''.join(random.sample(valid_char_pool, parameter_range_max + 1))

    # invalid: random length string include other invalid range ascii markers
    invalid_random_length_str = generate_invalid_length_string(invalid_char_pool, invalid_ascii_pool,
                                                               parameter_range_min, parameter_range_max)

    # not ascii chars
    non_ascii_str = ''.join(
        random.sample(utils.NONASCII, random.randrange(parameter_range_min, 5, 1)))

    valid_equivalence_partition_list += [shortest_str, longest_str, random_length_str, origin_case_sense_str,
                                         reverse_case_sense_str]
    invalid_equivalence_partition_list += [less_than_shortest_str, more_than_longest_str, invalid_random_length_str,
                                           non_ascii_str]
    temp_dict[parameter['parameterName']]['valid_equivalence_partition'] = valid_equivalence_partition_list
    temp_dict[parameter['parameterName']]['invalid_equivalence_partition'] = invalid_equivalence_partition_list
    varchar2_equivalence_partition_basic[parameter['parameterName']]['valid_equivalence_partition'][
        'parameterRange_validChar'] = \
        [shortest_str, longest_str, random_length_str]
    varchar2_equivalence_partition_basic[parameter['parameterName']]['invalid_equivalence_partition'][
        'parameterRange_validChar'] = \
        [less_than_shortest_str, more_than_longest_str, invalid_random_length_str, non_ascii_str]
    return varchar2_equivalence_partition_basic, temp_dict

def generate_number_edge_value(smallest_value, biggest_value, decimal_numbers):
    '''
    @summary: generate boundary value as testing data based on number type
    @param smallest_value: the smallest value in parameterRange
    @param biggest_value: the biggest_value value in parameterRange
    @param decimal_numbers: the decimal places in float
    @return: boundary value
    '''
    if decimal_numbers != 0:
        inner_left_value = smallest_value + 1 / 10 ** decimal_numbers  # valid value
        outer_left_value = smallest_value - 1 / 10 ** decimal_numbers  # invalid value
        inner_right_value = biggest_value - 1 / 10 ** decimal_numbers  # valid value
        outer_right_value = biggest_value + 1 / 10 ** decimal_numbers  # invalid value

        inner_left_value = round(inner_left_value, decimal_numbers)
        outer_left_value = round(outer_left_value, decimal_numbers)
        inner_right_value = round(inner_right_value, decimal_numbers)
        outer_right_value = round(outer_right_value, decimal_numbers)
    else:
        inner_left_value = smallest_value + 1  # valid value
        if not smallest_value == 0:
            outer_left_value = smallest_value - 1  # invalid value
        else:
            outer_left_value = smallest_value
        inner_right_value = biggest_value - 1  # valid value
        outer_right_value = biggest_value + 1  # invalid value
    return inner_left_value, outer_left_value, inner_right_value, outer_right_value

def generate_number_testing_data(parameter, number_equivalence_partition_basic):
    '''
    @summary: generate equivalence partition and testing data based on number type
    @param parameter: tested parameter
    @param number_equivalence_partition_basic: basic dict
    @return: equivalence partition dict include testing data
    '''
    temp_dict = {parameter['parameterName']: {}}
    valid_equivalence_partition_list = []
    invalid_equivalence_partition_list = []
    if_null = parameter['ifNull']

    # valid or invalid based on if_null
    if_null_list = ['None']
    if if_null is True:
        invalid_equivalence_partition_list += if_null_list
        number_equivalence_partition_basic[parameter['parameterName']]['invalid_equivalence_partition']['ifNull'] = \
            if_null_list
    else:
        valid_equivalence_partition_list += if_null_list
        number_equivalence_partition_basic[parameter['parameterName']]['valid_equivalence_partition']['ifNull'] = \
            if_null_list

    # get open/close range
    open_parentheses, open_brackets, close_parentheses, close_brackets = \
        utils.check_open_close_range(parameter['parameterRange'])

    # abstract start number/end number, decimal places
    origin_start_number, origin_end_number, decimal_numbers = utils.get_start_end_data(parameter['parameterRange'])

    # check (str)origin_start_number/(str)origin_end_number is int or float
    if '.' not in origin_start_number:
        start_number = int(origin_start_number)
    else:
        start_number = float(origin_start_number)
    if '.' not in origin_end_number:
        end_number = int(origin_end_number)
    else:
        end_number = float(origin_end_number)

    # check if end_number less than start_number
    if end_number <= start_number:
        raise RuntimeError('In parameterRange, the second digit should less than the first one!')
    smallest_value = 0
    biggest_value = 0

    # for []
    if open_brackets and close_brackets:
        smallest_value = start_number
        biggest_value = end_number

    # for [):
    if open_brackets and close_parentheses:
        smallest_value = start_number
        if decimal_numbers != 0:
            biggest_value = end_number - 1 / 10 ** decimal_numbers
        else:
            biggest_value = end_number - 1

    # for (]:
    if open_parentheses and close_brackets:
        if decimal_numbers != 0:
            smallest_value = start_number + 1 / 10 ** decimal_numbers
        else:
            smallest_value = start_number + 1
        biggest_value = end_number

    # for ():
    if open_parentheses and close_parentheses:
        if decimal_numbers != 0:
            smallest_value = start_number + 1 / 10 ** decimal_numbers
            biggest_value = end_number - 1 / 10 ** decimal_numbers
        else:
            smallest_value = start_number + 1
            biggest_value = end_number - 1

    # random value
    if decimal_numbers == 0:
        random_value = random.randint(start_number, end_number)
    else:
        random_value = random.uniform(start_number, end_number)
    if isinstance(biggest_value, float):
        biggest_value = round(biggest_value, decimal_numbers)
    if isinstance(smallest_value, float):
        smallest_value = round(smallest_value, decimal_numbers)
    if isinstance(random_value, float):
        random_value = round(random_value, decimal_numbers)
    inner_left_value, outer_left_value, inner_right_value, outer_right_value = generate_number_edge_value(
        smallest_value, biggest_value, decimal_numbers)
    valid_equivalence_partition_list += [smallest_value, biggest_value, inner_left_value, inner_right_value,
                                         random_value]
    invalid_equivalence_partition_list += [outer_left_value, outer_right_value]
    temp_dict[parameter['parameterName']]['valid_equivalence_partition'] = valid_equivalence_partition_list
    temp_dict[parameter['parameterName']]['invalid_equivalence_partition'] = invalid_equivalence_partition_list
    number_equivalence_partition_basic[parameter['parameterName']]['valid_equivalence_partition']['parameterRange'] = \
        [smallest_value, biggest_value, inner_left_value, inner_right_value, random_value]
    number_equivalence_partition_basic[parameter['parameterName']]['invalid_equivalence_partition']['parameterRange'] = \
        [outer_left_value, outer_right_value]
    return number_equivalence_partition_basic, temp_dict

def generate_date_edge_value(start_date, end_date):
    '''
    @summary: generate boundary value as testing data based on date type
    @param start_date: the earliest date
    @param end_date: the latest date
    @return: boundary value
    '''
    tmp_date = utils.get_year_month_day_from_string(start_date)
    tmp_inner_left_date = date(tmp_date[0], tmp_date[1], tmp_date[2]) - timedelta(days=1)
    inner_left_date = utils.date_to_string(start_date, tmp_inner_left_date)
    tmp_outer_left_date = date(tmp_date[0], tmp_date[1], tmp_date[2]) + timedelta(days=1)
    outer_left_date = utils.date_to_string(start_date, tmp_outer_left_date)
    tmp_date = utils.get_year_month_day_from_string(end_date)
    tmp_inner_right_date = date(tmp_date[0], tmp_date[1], tmp_date[2]) - timedelta(days=1)
    inner_right_date = utils.date_to_string(start_date, tmp_inner_right_date)
    tmp_outer_right_date = date(tmp_date[0], tmp_date[1], tmp_date[2]) + timedelta(days=1)
    outer_right_date = utils.date_to_string(start_date, tmp_outer_right_date)
    return inner_left_date, outer_left_date, inner_right_date, outer_right_date

def get_smallest_biggest_date(open_parentheses, open_brackets, close_parentheses, close_brackets, origin_start_date,
                              origin_end_date):
    '''
    @summary: generate smallest and biggest date based on date type in open or close range
    @param open_parentheses: (
    @param close_parentheses: )
    @param open_brackets: [
    @param close_brackets: ]
    @param origin_start_date: original start date from user input
    @param origin_end_date: original end date from user input
    @return: biggest date/smallest date based on open or close range
    '''
    smallest_date = ''
    biggest_date = ''

    # for []
    if open_brackets and close_brackets:
        smallest_date = origin_start_date
        biggest_date = origin_end_date

    # for [):
    if open_brackets and close_parentheses:
        smallest_date = origin_start_date

        # open biggest_date is earlier 1 day than origin_end_date
        year, month, day = utils.get_year_month_day_from_string(origin_end_date)
        tmp_biggest_date = date(year, month, day) - timedelta(days=1)

        # transform tmp_biggest_date which is date format to string format
        biggest_date = utils.date_to_string(origin_end_date, tmp_biggest_date)

    # for (]:
    if open_parentheses and close_brackets:
        # open smallest_date is later 1 day than origin_start_date
        year, month, day = utils.get_year_month_day_from_string(origin_start_date)
        tmp_smallest_date = date(year, month, day) + timedelta(days=1)
        smallest_date = utils.date_to_string(origin_end_date, tmp_smallest_date)
        biggest_date = origin_end_date

    # for ():
    if open_parentheses and close_parentheses:
        start_year, start_month, start_day = utils.get_year_month_day_from_string(origin_start_date)
        end_year, end_month, end_day = utils.get_year_month_day_from_string(origin_end_date)
        tmp_smallest_date = date(start_year, start_month, start_day) + timedelta(days=1)
        smallest_date = utils.date_to_string(origin_end_date, tmp_smallest_date)
        tmp_biggest_date = date(end_year, end_month, end_day) - timedelta(days=1)
        biggest_date = utils.date_to_string(origin_end_date, tmp_biggest_date)

    return smallest_date, biggest_date

def compose_digits_string_for_date(digits_places):
    '''
    @summary: generate digits string to compose yyyymmdd
    @param digits_places: digits places
    @return: digits string
    '''
    return ''.join(str(i) for i in random.sample(range(0, 9), digits_places))

def millennium_bug_year(date_mark):
    '''
    @summary: millennium bug years
    @param date_mark: date splitter such as: -, :, .,
    @return: millennium bug year list
    '''
    millennium_bug_year_list = ['0000' + date_mark + '00' + date_mark + '00',
                                      '1999' + date_mark + '12' + date_mark + '31',
                                      '2000' + date_mark + '01' + date_mark + '01',
                                      '2038' + date_mark + '01' + date_mark + '19']
    return millennium_bug_year_list

def generate_valid_date_in_range(smallest_date, biggest_date):
    '''
    @summary: generate valid date in range between smallest date and biggest date
    @param smallest_date: start date
    @param biggest_date: end date
    @return: one valid range date
    '''
    biggest_date_tuple = utils.get_year_month_day_from_string(biggest_date)
    smallest_date_tuple = utils.get_year_month_day_from_string(smallest_date)
    delta_days = (date(biggest_date_tuple[0], biggest_date_tuple[1], biggest_date_tuple[2]) -
                  date(smallest_date_tuple[0], smallest_date_tuple[1], smallest_date_tuple[2])).days
    random_date_gap = random.randint(0, delta_days)
    random_date_in_data_format = date(smallest_date_tuple[0], smallest_date_tuple[1],
                                      smallest_date_tuple[2]) + timedelta(days=random_date_gap)
    valid_random_date = utils.date_to_string(biggest_date, random_date_in_data_format)
    return valid_random_date

def generate_date_testing_data(parameter, date_equivalence_partition_basic):
    '''
    @summary: generate equivalence partition and testing data based on date type
    @param parameter: tested parameter
    @param date_equivalence_partition_basic: basic dict
    @return: equivalence partition dict include testing data
    '''
    temp_dict = {parameter['parameterName']: {}}
    valid_equivalence_partition_list = []
    invalid_equivalence_partition_list = []
    if_null = parameter['ifNull']

    # get open/close range
    open_parentheses, open_brackets, close_parentheses, close_brackets = utils.check_open_close_range(
        parameter['parameterRange'])

    # abstract start date/end date
    origin_start_date, origin_end_date, decimal_numbers = utils.get_start_end_data(parameter['parameterRange'])

    # check if user input date value is correct
    utils.check_if_date_range_correct(origin_start_date, origin_end_date)

    # generate valid equivalence partition and testing data
    smallest_date, biggest_date = get_smallest_biggest_date(open_parentheses, open_brackets, close_parentheses,
                                                            close_brackets, origin_start_date, origin_end_date)

    # valid or invalid based on if_null
    if_null_list = ['None']
    if if_null is True:
        invalid_equivalence_partition_list += if_null_list
        date_equivalence_partition_basic[parameter['parameterName']]['invalid_equivalence_partition']['ifNull'] = \
            if_null_list
    else:
        valid_equivalence_partition_list += if_null_list
        date_equivalence_partition_basic[parameter['parameterName']]['valid_equivalence_partition']['ifNull'] = \
            if_null_list

    # generate invalid equivalence partition and testing data
    # year is out of the range [1900, 3000]
    invalid_year_1 = utils.date_to_string(origin_end_date, date(1899, 12, 31))
    invalid_year_2 = utils.date_to_string(origin_end_date, date(3001, 1, 1))

    # abstract mark in date format
    date_mark = utils.get_date_splitter(origin_end_date)

    # generate random date in valid range
    valid_random_date = generate_valid_date_in_range(smallest_date, smallest_date)

    # month is out of the range [0,12]
    tmp_year, tmp_month, tmp_day = utils.get_year_month_day_from_string(valid_random_date)
    invalid_month_date_1 = str(tmp_year) + date_mark + str(0) + date_mark + str(tmp_day)
    invalid_month_date_2 = str(tmp_year) + date_mark + str(13) + date_mark + str(tmp_day)

    # day is out of the valid range [0, days of current month]
    invalid_day_date_1 = str(tmp_year) + date_mark + str(tmp_month) + date_mark + str(0)
    invalid_day_date_2 = str(tmp_year) + date_mark + str(tmp_month) + date_mark + \
                                                                str(utils.check_leap_year(tmp_year, tmp_month) + 1)
    inner_left_date, outer_left_date, inner_right_date, outer_right_date = generate_date_edge_value(smallest_date,
                                                                                                    biggest_date)

    # not date type testing data
    invalid_not_date_type_1 = ''.join(random.sample(utils.NONASCII, 8))

    # invalid format date, such as: yyy-mm-dd, yyyy-m-dd, yyyy-mm-d
    yyyy = compose_digits_string_for_date(4)
    mm = compose_digits_string_for_date(2)
    dd = compose_digits_string_for_date(2)
    invalid_date_1 = yyyy[0:2] + date_mark + mm + date_mark + dd
    invalid_date_2 = yyyy + date_mark + mm[0] + date_mark + dd
    invalid_date_3 = yyyy + date_mark + mm + date_mark + dd[0]
    valid_equivalence_partition_list += [smallest_date, biggest_date, inner_left_date, inner_right_date,
                                         valid_random_date]
    invalid_equivalence_partition_list += [invalid_year_1, invalid_year_2, invalid_month_date_1, invalid_month_date_2,
                                           invalid_day_date_1, invalid_day_date_2,
                                           invalid_not_date_type_1, invalid_date_1, invalid_date_2, invalid_date_3,
                                           outer_left_date, outer_right_date] + millennium_bug_year(date_mark)
    temp_dict[parameter['parameterName']]['valid_equivalence_partition'] = valid_equivalence_partition_list
    temp_dict[parameter['parameterName']]['invalid_equivalence_partition'] = invalid_equivalence_partition_list
    date_equivalence_partition_basic[parameter['parameterName']]['valid_equivalence_partition']['parameterRange'] = \
        [smallest_date, biggest_date, inner_left_date, inner_right_date, valid_random_date]
    date_equivalence_partition_basic[parameter['parameterName']]['invalid_equivalence_partition']['parameterRange'] = \
        [invalid_year_1, invalid_year_2, invalid_month_date_1, invalid_month_date_2, invalid_day_date_1,
         invalid_day_date_2,
         invalid_not_date_type_1, invalid_date_1, invalid_date_2, invalid_date_3, outer_left_date, outer_right_date] \
                                                                    + millennium_bug_year(date_mark)
    return date_equivalence_partition_basic, temp_dict

def generate_random_datetime(start_datetime, end_datetime):
    start_datetime_tuple = tuple(start_datetime.timetuple()[0:9])
    end_datetime_tuple = tuple(end_datetime.timetuple()[0:9])
    start_datetime_timestamp = time.mktime(start_datetime_tuple)
    end_datetime_timestamp = time.mktime(end_datetime_tuple)
    t = random.randint(start_datetime_timestamp, end_datetime_timestamp)
    datetime_tuple = time.localtime(t)
    random_datetime = time.strftime("%Y-%m-%dT%H:%M:%S", datetime_tuple)
    return random_datetime

def generate_datetime_testing_data(parameter, datetime_equivalence_partition_basic):
    '''
    @summary: generate equivalence partition and testing data based on dateTime type
    @param parameter: tested parameter
    @param datetime_equivalence_partition_basic: basic dict
    @return: equivalence partition dict include testing data
    '''
    temp_dict = {parameter['parameterName']: {}}
    valid_equivalence_partition_list = []
    invalid_equivalence_partition_list = []
    if_null = parameter['ifNull']
    # valid or invalid based on if_null
    if_null_list = ['None']
    if if_null is True:
        invalid_equivalence_partition_list += if_null_list
        datetime_equivalence_partition_basic[parameter['parameterName']]['invalid_equivalence_partition']['ifNull'] = \
            if_null_list
    else:
        valid_equivalence_partition_list += if_null_list
        datetime_equivalence_partition_basic[parameter['parameterName']]['valid_equivalence_partition']['ifNull'] = \
            if_null_list

    # generate valid testing data：datetime between now and 3 minutes before
    valid_random_datetime_basic = generate_random_datetime(datetime.datetime.now() + datetime.timedelta(minutes=-3), \
                                                           datetime.datetime.now())
    valid_equivalence_partition_list.append(valid_random_datetime_basic + 'Z')
    valid_equivalence_partition_list.append(valid_random_datetime_basic + '+08:00')
    valid_equivalence_partition_list.append(valid_random_datetime_basic + '-08:00')
    # leap year/second
    valid_equivalence_partition_list.append('2000-02-29')
    valid_equivalence_partition_list.append('2015-06-30T23:59:60')
    # invalid: full year is just 2 digits
    invalid_equivalence_partition_list.append(valid_random_datetime_basic.split('-')[0][2:] + '-' + '-'.join(valid_random_datetime_basic.split('-')[1:]))
    # invalid: month is 3 digits
    invalid_equivalence_partition_list.append(valid_random_datetime_basic.split('-')[0] + '-' + \
                                                valid_random_datetime_basic.split('-')[1]+'1' + '-' + \
                                                    '-'.join(valid_random_datetime_basic.split('-')[2:]))
    # invalid: month is not 01~12
    invalid_equivalence_partition_list.append(valid_random_datetime_basic.split('-')[0] + \
                                                                '-' + str(13) + '-' + \
                                                                '-'.join(valid_random_datetime_basic.split('-')[2:]))
    # invalid: day is 3 digits
    invalid_equivalence_partition_list.append(valid_random_datetime_basic.split('T')[0]+'1'+ \
                                              'T'+valid_random_datetime_basic.split('T')[-1])
    # invalid: day is 00
    invalid_equivalence_partition_list.append('-'.join(valid_random_datetime_basic.split('T')[0].split('-')[0:-1]) + \
                                              '-00' + 'T' + valid_random_datetime_basic.split('T')[-1])
    # invalid: hour is not in 00~23
    invalid_equivalence_partition_list.append(valid_random_datetime_basic.split('T')[0] + 'T24:' + \
                                            ':'.join(valid_random_datetime_basic.split('T')[-1].split(':')[1:]))
    # invalid: minute is not in 00~59
    invalid_equivalence_partition_list.append(valid_random_datetime_basic.split('T')[0]+'T'\
                                   +valid_random_datetime_basic.split('T')[-1].split(':')[0] +\
                                   ':60:' + valid_random_datetime_basic.split('T')[-1].split(':')[-1])
    # invalid: second is not in 00~60
    invalid_equivalence_partition_list.append(valid_random_datetime_basic.split('T')[0] + 'T' + \
                                   ':'.join(valid_random_datetime_basic.split('T')[-1].split(':')[0:-1]) + ':61')
    # invalid: time-numoffset
    invalid_equivalence_partition_list.append(valid_random_datetime_basic + '+08+00')
    # invalid: both Z and numoffset
    invalid_equivalence_partition_list.append(valid_random_datetime_basic + '+08:00Z')
    # invalid: 2021=08=23T09:50:07
    invalid_equivalence_partition_list.append('='.join(valid_random_datetime_basic.split('-')))
    # invalid: 2021-08-23T09;50;07
    invalid_equivalence_partition_list.append(';'.join(valid_random_datetime_basic.split(':')))
    # invalid: 2021-08-23T09:50:07,09
    invalid_equivalence_partition_list.append(valid_random_datetime_basic + ',09')
    # invalid: 2021-08-23I09:50:07
    invalid_equivalence_partition_list.append('I'.join(valid_random_datetime_basic.split('T')))
    # invalid: not date type
    invalid_equivalence_partition_list.append('0123456789')
    # invalid：0000-00-00
    invalid_equivalence_partition_list.append('0000-00-00')
    temp_dict[parameter['parameterName']]['valid_equivalence_partition'] = valid_equivalence_partition_list
    temp_dict[parameter['parameterName']]['invalid_equivalence_partition'] = invalid_equivalence_partition_list
    datetime_equivalence_partition_basic[parameter['parameterName']]['valid_equivalence_partition']['parameterRange'] \
                                                            = valid_equivalence_partition_list
    datetime_equivalence_partition_basic[parameter['parameterName']]['invalid_equivalence_partition'][
                                                            'parameterRange'] = invalid_equivalence_partition_list
    return datetime_equivalence_partition_basic, temp_dict

def generate_file_testing_data(parameter, file_equivalence_partition_basic):
    '''
    @summary: generate equivalence partition and testing data based on file type
    @param parameter: tested parameter
    @param file_equivalence_partition_basic: basic dict
    @return: equivalence partition dict include testing data
    '''
    temp_dict = {parameter['parameterName']: {}}
    valid_equivalence_partition_list = []
    invalid_equivalence_partition_list = []
    if_null = parameter['ifNull']
    valid_char = copy.deepcopy(parameter['validChar'])

    # valid or invalid based on if_null
    if_null_list = ["''",'None']
    if if_null is True:
        invalid_equivalence_partition_list += if_null_list
        file_equivalence_partition_basic[parameter['parameterName']]['invalid_equivalence_partition']['ifNull'] = \
            if_null_list
    else:
        valid_equivalence_partition_list += if_null_list
        file_equivalence_partition_basic[parameter['parameterName']]['valid_equivalence_partition']['ifNull'] = \
            if_null_list

    # valid file format
    invalid_file_format = []
    for i in valid_char:
        invalid_file_format.append(i + 'a')
    file_equivalence_partition_basic[parameter['parameterName']]['valid_equivalence_partition'][
        'parameterRange'] = valid_char
    file_equivalence_partition_basic[parameter['parameterName']]['invalid_equivalence_partition']['parameterRange'] = \
        invalid_file_format
    valid_equivalence_partition_list += valid_char
    invalid_equivalence_partition_list += invalid_file_format
    temp_dict[parameter['parameterName']]['valid_equivalence_partition'] = valid_equivalence_partition_list
    temp_dict[parameter['parameterName']]['invalid_equivalence_partition'] = invalid_equivalence_partition_list
    return file_equivalence_partition_basic, temp_dict

def generate_enum_testing_data(parameter, enum_equivalence_partition_basic):
    '''
    @summary: generate equivalence partition and testing data based on enum type
    @param parameter: tested parameter
    @param enum_equivalence_partition_basic: basic dict
    @return: equivalence partition dict include testing data
    '''
    temp_dict = {parameter['parameterName']: {}}
    valid_equivalence_partition_list = []
    invalid_equivalence_partition_list = []
    if_null = parameter['ifNull']
    case_sense = parameter['caseSensitive']

    # valid: generate the valid partition string based on range
    for i in parameter['parameterRange']:
        valid_equivalence_partition_list.append(i)

    # valid or invalid based on if_null
    if_null_list = ["''", 'None']
    if if_null is True:
        invalid_equivalence_partition_list += if_null_list
        enum_equivalence_partition_basic[parameter['parameterName']]['invalid_equivalence_partition']['ifNull'] = \
            if_null_list
    else:
        valid_equivalence_partition_list += if_null_list
        enum_equivalence_partition_basic[parameter['parameterName']]['valid_equivalence_partition']['ifNull'] = \
            if_null_list

    # check if enum values is chinese characters; if yes, case_sense is no any effect to equivalence partition
    parameterRange_is_english_flag = True
    for i in parameter['parameterRange']:
        if utils.check_chinese_string(i):
            parameterRange_is_english_flag = False
            break

    # check if enum values are all english characters; if yes, reverse case
    case_reverse_list = []
    for i in parameter['parameterRange']:
        if i.isalpha() is False:
            parameterRange_is_english_flag = False
            msg = 'Enum parameterRange english string values include non-english character: {1}'.format(i)
            logging.error(msg)
            raise RuntimeError(msg)
        else:
            case_reverse_list.append(i.swapcase())
    if case_sense is True and parameterRange_is_english_flag is True:
        enum_equivalence_partition_basic[parameter['parameterName']]['invalid_equivalence_partition']['caseSensitive'] = \
            case_reverse_list
        for i in case_reverse_list:
            invalid_equivalence_partition_list.append(i)
    elif not case_sense and parameterRange_is_english_flag:
        for i in case_reverse_list:
            valid_equivalence_partition_list.append(i)
    else:
        pass

    # invalid: any string out of enum range is valid testing data
    out_of_enum_range_values = []
    if parameterRange_is_english_flag:
        english_choices = ['roaddb', 'testcase', 'auto', 'generator', 'equivalence']
        out_of_enum_range_values.append(random.choice(english_choices))
    else:
        # generate chinese word if enum value is chinese
        chinese_choices = ['路图', '测试用例', '自动化', '生成器', '等价类']
        out_of_enum_range_values.append(random.choice(chinese_choices))
    invalid_equivalence_partition_list += out_of_enum_range_values
    enum_equivalence_partition_basic[parameter['parameterName']]['valid_equivalence_partition']['parameterRange'] = \
        parameter['parameterRange']
    enum_equivalence_partition_basic[parameter['parameterName']]['invalid_equivalence_partition']['parameterRange'] = \
        out_of_enum_range_values

    # generate english word if enum value is english
    temp_dict[parameter['parameterName']]['valid_equivalence_partition'] = valid_equivalence_partition_list
    temp_dict[parameter['parameterName']]['invalid_equivalence_partition'] = invalid_equivalence_partition_list
    return enum_equivalence_partition_basic, temp_dict

def generate_boolean_testing_data(parameter, boolean_equivalence_partition_basic):
    '''
    @summary: generate equivalence partition and testing data based on boolean type
    @param parameter: tested parameter
    @param enum_equivalence_partition_basic: basic dict
    @return: equivalence partition dict include testing data
    '''
    temp_dict = {parameter['parameterName']: {}}
    valid_equivalence_partition_list = []
    invalid_equivalence_partition_list = []
    If_null = parameter['ifNull']
    # valid testing data: True/False
    valid_equivalence_partition_list = [str(i) for i in parameter['parameterRange']]
    # valid or invalid based on if_null
    if_null_list = ["''", 'Null', 'None']
    if If_null is True:
        invalid_equivalence_partition_list += if_null_list
        boolean_equivalence_partition_basic[parameter['parameterName']]['invalid_equivalence_partition']['ifNull'] = \
            if_null_list
    else:
        valid_equivalence_partition_list += if_null_list
        boolean_equivalence_partition_basic[parameter['parameterName']]['valid_equivalence_partition']['ifNull'] = \
            if_null_list
    # non boolean value as invalid testing data: 0/1, yes/no
    invalid_equivalence_partition_list = [0, 1, 'yes', 'no']
    boolean_equivalence_partition_basic[parameter['parameterName']]['valid_equivalence_partition']['parameterRange'] = \
        valid_equivalence_partition_list
    boolean_equivalence_partition_basic[parameter['parameterName']]['invalid_equivalence_partition']['parameterRange'] = \
        invalid_equivalence_partition_list

    # generate english word if enum value is english
    temp_dict[parameter['parameterName']]['valid_equivalence_partition'] = valid_equivalence_partition_list
    temp_dict[parameter['parameterName']]['invalid_equivalence_partition'] = invalid_equivalence_partition_list
    return boolean_equivalence_partition_basic, temp_dict