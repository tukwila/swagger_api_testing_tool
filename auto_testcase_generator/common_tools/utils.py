#!/usr/bin/env python3
# encoding: utf-8
'''
Provide common utilities
Created on Jun 18, 2021
@author: Guangli.bao
'''
import os
import sys
import json
import csv
from datetime import date
from datetime import datetime
import sys
from dateutil.parser import parse
import requests

# uppercase = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
UPPERCASE = [chr(i) for i in range(65, 91)]

# lowercase = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
LOWERCASE = [chr(i) for i in range(97, 123)]

# number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
DIGITS = [chr(i) for i in range(48, 58)]

# otherMarkers = [' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']
# OTHERMARERS = [chr(i) for i in range(32, 127) if
#                i not in range(48, 58) and i not in range(65, 91) and i not in range(97, 123)]
OTHERMARERS = ['!','#', '$', '%', '&', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']

# non-ascii = ['¡', '¢', '£', '¤', '¥', '¦', '§', '¨', '©', 'ª', '«', '¬', '\xad', '®', '¯', '°', '±', '²', '³', '´', 'µ', '¶', '·', '¸', '¹', 'º', '»', '¼', '½', '¾', '¿', 'À', 'Á', 'Â', 'Ã', 'Ä', 'Å', 'Æ', 'Ç', 'È', 'É', 'Ê', 'Ë', 'Ì', 'Í', 'Î', 'Ï', 'Ð', 'Ñ', 'Ò', 'Ó', 'Ô', 'Õ', 'Ö', '×', 'Ø', 'Ù', 'Ú', 'Û', 'Ü', 'Ý', 'Þ', 'ß', 'à', 'á', 'â', 'ã', 'ä', 'å']
# NONASCII = [chr(i) for i in range(161, 230)]
NONASCII = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十']

def check_params(params):
    '''
    @summary: check if input parameter json is correct logically compare to equivalence partition conditions
    @param params: tested parameter
    @return: testcase in csv content
    '''
    check_result = 0  # 0: pass
    for i in params:
        para_keys = []
        for j in i.keys():
            para_keys.append(j)
        if i['parameterName'] == "" or i['parameterName'] == None:
            check_result = 1
            logger.error("Parameter {0} \'s name cannot be none".format(i['parameterName']))
        if i['parameterType'] not in ("VARCHAR2", "number", "enum", "date", "file"):
            check_result = 1
            logger.error(
                "Parameter {0} is not valid type, please use correct type: VARCHAR2/number/date/file/enum".format(
                    i['parameterName']))
        if i['parameterType'] == "VARCHAR2":
            if not set(["parameterRange", "ifNull", "validChar", "caseSensitive"]).issubset(para_keys):
                check_result = 1
                logger.error("Parameter {0} lacks equivalence partition condition".format(i['parameterName']))
            if len(i['parameterRange']) == 0 or i['ifNull'] == "" or len(i['validChar']) == 0 \
                    or i['caseSensitive'] == "":
                check_result = 1
                logger.error(
                    "Parameter {0} equivalence partition condition value cannot be empty".format(i['parameterName']))
        if i['parameterType'] is "number":
            if not set(["parameterRange", "ifNull"]).issubset(para_keys):
                check_result = 1
                logger.error("Parameter {0} lacks equivalence partition condition".format(i['parameterName']))
            if len(i['parameterRange']) == 0 or i['ifNull'] == "":
                check_result = 1
                logger.error(
                    "Parameter {0} equivalence partition condition value cannot be empty".format(i['parameterName']))
        if i['parameterType'] in ("file", "date"):
            if not set(["parameterRange", "ifNull", "validChar"]).issubset(para_keys):
                check_result = 1
                logger.error("Parameter {0} lacks equivalence partition condition".format(i['parameterName']))
            if len(i['parameterRange']) == 0 or i['ifNull'] == "" or len(i['validChar']) == 0:
                check_result = 1
                logger.error(
                    "Parameter {0} equivalence partition condition value cannot be empty".format(i['parameterName']))
        if i['parameterType'] == "enum":
            if not set(["parameterRange", "ifNull", "caseSensitive"]).issubset(para_keys):
                check_result = 1
                logger.error("Parameter {0} lacks equivalence partition condition".format(i['parameterName']))
            if len(i['parameterRange']) == 0 or i['ifNull'] == "" or i['caseSensitive'] == "":
                check_result = 1
                logger.error(
                    "Parameter {0} equivalence partition condition value cannot be empty".format(i['parameterName']))
    return check_result

def check_if_file_exists(path):
    '''
    @summary: check if input json file exists
    @param path: input json file path
    @return: tested parameters
    '''
    tested_parameters = {}
    if os.path.exists(path) or os.path.isfile(path):
        with open(path, 'r') as jf:
            tested_parameters = json.load(jf)

        # check if parameters valid
        if check_params(tested_parameters) != 0:
            msg = 'json parameters validate fail'
            logger.error(msg)
            raise RuntimeError(msg)
        return tested_parameters
    else:
        msg = "These is no json file in the path: ", path
        logger.error(msg)
        raise RuntimeError(msg)

def csv_writer(path, result):
    '''
    @summary: store equivalence partition result into csv file
    @param path: output json file path
    @param result: csv content
    @return: None
    '''
    csv_headers = ['Index', 'Title']
    rows = []
    count = 1
    msg = 'Equivalence partition result is not Dict, cannot write into csv'
    for k, v in result.items():
        if isinstance(v, dict):
            for name, value in v.items():
                if name == 'valid_part_csv_content':
                    testcase_content = (str(count), value)
                    rows.append(testcase_content)
                    count += 1
                if name == 'invalid_part_csv_content':
                    for j in value:
                        testcase_content = (str(count), j)
                        rows.append(testcase_content)
                        count += 1
        else:
            logger.error(msg)
            raise Exception(msg)
    with open(path, 'w', encoding='utf-8-sig') as csvf:
        writer = csv.writer(csvf)
        writer.writerow(csv_headers)
        for i in rows:
            writer.writerow(i)

def swagger_csv_writer(path, result):
    '''
    @summary: store swagger api equivalence partition result into csv file
    @param path: output json file path
    @param result: csv content
    @return: None
    '''
    csv_headers = ['Index', 'TestSuites', 'TestCases']
    rows = []
    count = 1
    msg = 'Equivalence partition result is not Dict, cannot write into csv'
    for k, v in result.items():
        if isinstance(v, dict):
            for name, value in v.items():
                swagger_api_path = v['path']
                if name == 'valid_part_csv_content':
                    testcase_content = (str(count), swagger_api_path, value)
                    rows.append(testcase_content)
                    count += 1
                if name == 'invalid_part_csv_content':
                    for j in value:
                        testcase_content = (str(count), swagger_api_path, j)
                        rows.append(testcase_content)
                        count += 1
        else:
            logger.error(msg)
            raise Exception(msg)
    with open(path, 'w', encoding='utf-8-sig') as csvf:
        writer = csv.writer(csvf)
        writer.writerow(csv_headers)
        for i in rows:
            writer.writerow(i)

def check_open_close_range(range_value):
    '''
    @summary: check if range_value is open range or close range based on number/date type;
              open range： parentheses: () ; close range: brackets: []
    @param range_value: tested parameter range value
    @return: equivalence partition dict include testing data
    '''
    open_parentheses = None
    close_parentheses = None
    open_brackets = None
    close_brackets = None

    # check open parentheses, close parentheses/open brackets close brackets
    try:
        if range_value.strip().startswith('('):
            open_parentheses = True
        if range_value.strip().startswith('['):
            open_brackets = True
        if range_value.strip().endswith(')'):
            close_parentheses = True
        if range_value.strip().endswith(']'):
            close_brackets = True
        return open_parentheses, open_brackets, close_parentheses, close_brackets
    except:
        logger.error('number/date parameterRange format is wrong')
        raise Exception('number/date parameterRange format is wrong')

def get_start_end_data(data_range):
    '''
    @summary: get start number and end number from one range that is number type or date type
    @param data_range: data range such as "[3, 20]" or "[20191031, 20191101]"
    @return: string: origin_start_number, origin_end_number; int: decimal_numbers
    '''

    # abstract start number/end number, decimal places
    comma_index = data_range.index(',')
    origin_start_number = data_range[1: comma_index]

    # check if origin_start_number is float or int
    if '.' in origin_start_number:
        start_number_decimal_num = len(origin_start_number.split('.')[-1])
    else:
        start_number_decimal_num = 0
    origin_end_number = data_range[comma_index + 1: -1]
    if '.' in origin_end_number:
        end_number_decimal_num = len(origin_end_number.split('.')[-1])
    else:
        end_number_decimal_num = 0
    if start_number_decimal_num == 0 and end_number_decimal_num == 0:
        decimal_numbers = 0
    else:
        decimal_numbers = max(start_number_decimal_num, end_number_decimal_num)
    return origin_start_number, origin_end_number, decimal_numbers

def is_valid_date(year, month, day):
    '''
    @summary: check if date is valid date
    @param year: year
    @param month: month
    @param day: day
    @return: 0: pass; 1: fail
    '''
    try:
        date(year, month, day)
    except:
        return False
    else:
        return True

def get_year_month_day_from_string(date_string_value):
    '''
    @summary: abstract year/month/day int value from date string value
    @param date_string_value: date string value, like: '20191231' or '2019-12-31' or '2019.12.31'
    @return: year/month/day int value
    '''
    return parse(date_string_value).year, parse(date_string_value).month, parse(date_string_value).day

def get_date_splitter(date_string_value):
    '''
    @summary: abstract splitter from date format such as: .,/,-,: and etc
    @param date_string_value: date string value, like: '20191231' or '2019-12-31' or '2019.12.31'
    @return: splitter
    '''
    date_splitter = date_string_value[4]  #assume date format is yearfirst: such as '2019-12-31' or '2019.12.31'
    if date_splitter in ['-', '/', ':', '.']:
        pass
    elif date_string_value.isdigit(): #'20191231'
        date_splitter = ''
    else:
        logger.error('date string format should be: \'20191231\' or \'2019-12-31\' or \'2019.12.31\'')
    return date_splitter

def check_leap_year(year, month):
    '''
    @summary: check solar manth/lunar month/leap year
            a solar month of 31 days/a lunar month of 30 days/Febrary in leap year
    @param year: year
    @param month: manth
    @return: days in month
    '''
    if month in [1, 3, 5, 7, 8, 10, 12]:
        days = 31
    if month in [4, 6, 9, 11]:
        days = 30
    if year % 4 == 0 & year % 100 != 0 & year % 400 == 0:
        days = 29
    else:
        days = 28
    return days

def date_to_string(date_string_format, date_value):
    '''
    @summary: transform date to string format
    @param date_string_format: date in string format, like: '20191231' or '2019-12-31' or '2019.12.31'
    @param date_value: date value
    @return: date in string format
    '''
    date_splitter = get_date_splitter(date_string_format)
    time_format = "%Y" + date_splitter + "%m" + date_splitter + "%d"
    date_in_string_format = date_value.strftime(time_format)
    return date_in_string_format

def check_if_date_range_correct(start_date, end_date):
    '''
    @summary: check if user input value date_range value is correct:
            a. start_date/end_date is correct according to month/day
            b. end_date is bigger than start_date
    @param date_range: tested parameter date range value
    @return: None
    '''

    # get year/month/day from start_date/end_date which are string
    start_year, start_month, start_day = get_year_month_day_from_string(start_date)
    end_year, end_month, end_day = get_year_month_day_from_string(end_date)

    # check if date value is valid date
    if not is_valid_date(start_year, start_month, start_day) or not is_valid_date(end_year, end_month, end_day):
        logger.error('These is wrong value in date')
        raise Exception('These is wrong value in date')

    # check if end_date is bigger than start_date
    if date(start_year, start_month, start_day) >= date(end_year, end_month, end_day):
        logger.error('start date should less than end date')
        raise Exception('start date should less than end date')

def check_chinese_string(string_data):
    '''
    @summary: check if the whole string is chinese
    @param string_data: chinese string
    @return: True, False
    '''
    result = True
    for w in string_data:
        if not '\u4e00' <= w <= '\u9fff':
            result = False
    return result

def read_orthogonal_array_file(orthogonal_array_file):
    '''
    @summary: read taguchi_designs.txt or ts723_Designs.txt file content to compose OrderedDict list
    @param orthogonal_array_file: taguchi_designs.txt or ts723_Designs.txt
    @return: OrderedDict list include orthogonal array
    '''
    data = {}

    # analyze taguchi_designs or ts723_Designs
    with open(orthogonal_array_file, 'r') as f:
        key = ''
        value = []
        pos = 0
        for i in f:
            i = i.strip()
            if 'n=' in i:
                if key and value:
                    data[key] = dict(pos=pos,
                                          n=int(key.split('n=')[1].strip()),
                                          mk=[[int(mk.split('^')[0]), int(mk.split('^')[1])] for mk in
                                              key.split('n=')[0].strip().split(' ')],
                                          data=value)
                key = ' '.join([k for k in i.split(' ') if k])
                value = []
                pos += 1
            elif i:
                value.append(i)

        data[key] = dict(pos=pos,
                         n=int(key.split('n=')[1].strip()),
                         mk=[[int(mk.split('^')[0]), int(mk.split('^')[1])] for mk in
                             key.split('n=')[0].strip().split(' ')],
                         data=value)
    data = sorted(data.items(), key=lambda j: j[1]['pos'])
    return data

def orthogonal_array_csv_writer(path, result):
    '''
    @summary: store equivalence partition result into csv file
    @param path: output json file path
    @param result: csv content
    @return: None
    '''
    csv_headers = ['Index', 'Title']
    rows = []
    count = 1
    for i in result:
        testcase_content = (str(count), i)
        rows.append(testcase_content)
        count += 1
    with open(path, 'w', encoding='utf-8-sig') as csvf:
        writer = csv.writer(csvf)
        writer.writerow(csv_headers)
        for i in rows:
            writer.writerow(i)

def swagger_orthogonal_array_csv_writer(path, result):
    '''
    @summary: store swagger api test cases based on orthogonal array into csv file
    @param path: output json file path
    @param result: csv content
    @return: None
    '''
    csv_headers = ['Index', 'TestSuites', 'TestCases']
    rows = []
    count = 1
    for i in result:
        testcase_content = (str(count), i[0], i[1])
        rows.append(testcase_content)
        count += 1
    with open(path, 'w', encoding='utf-8-sig') as csvf:
        writer = csv.writer(csvf)
        writer.writerow(csv_headers)
        for i in rows:
            writer.writerow(i)

def check_swagger_url(url):
    '''
    @summary: validate if swagger api_docs can access
    @param url: swagger url
    @return 0: pass; 1: fail
    '''
    response = requests.get(url)
    if response.status_code != 200:
        logger.error("Swagger api_docs url cannot access")
        return 1
    else:
        return 0