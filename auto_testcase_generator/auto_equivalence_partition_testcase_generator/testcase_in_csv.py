#!/usr/bin/env python3
# encoding: utf-8
'''
Generate testcases content based on equivalence partition result and equivalence partition conditions
Created on Jun 29, 2021
@author: Guangli.bao
'''
from common_tools import utils
import copy


def if_null_content_template(If_null, parameter, equivalence_partition_basic):
    valid_if_null_content = ''
    invalid_if_null_content = ''
    if If_null is True:
        invalid_if_null_content = parameter['parameterName'] + '必填时的非法测试数据，如' + \
                                  ','.join(equivalence_partition_basic[parameter['parameterName']][
                                               'invalid_equivalence_partition']['ifNull'])
    else:
        valid_if_null_content = parameter['parameterName'] + '非必填时的合法测试数据，如' + \
                                ','.join(equivalence_partition_basic[parameter['parameterName']][
                                             'valid_equivalence_partition']['ifNull'])
    return valid_if_null_content, invalid_if_null_content

def testcase_varchar_content(parameter, varchar2_equivalence_partition_basic):
    '''
    @summary: generate equivalence partition testcase for csv based on varchar2 type
    @param parameter: tested parameter of varchar2 type
    @param varchar2_equivalence_partition_basic: varchar2's equivalence partition dict
    @return: testcase in csv content
    '''
    parameter_range_min = parameter['parameterRange'][0]
    parameter_range_max = parameter['parameterRange'][1]
    If_null = parameter['ifNull']
    valid_char = parameter['validChar']
    case_sense = parameter['caseSensitive']
    csv_content = {
        parameter['parameterName']: {
            'valid_part_csv_content': '',
            'invalid_part_csv_content': []
        }
    }
    valid_content_template_basic = parameter['parameterName'] + '为长度在' + str(parameter_range_min) + '(含)到' + \
                                   str(parameter_range_max) + '(含)以内'
    valid_test_data_in_content = '的合法字符, 如' + \
                                 ','.join(varchar2_equivalence_partition_basic[parameter['parameterName']][
                                              'valid_equivalence_partition']['parameterRange_validChar'])
    if varchar2_equivalence_partition_basic[parameter['parameterName']]['valid_equivalence_partition']['caseSensitive']:
        valid_test_data_in_content += ','.join(
        varchar2_equivalence_partition_basic[parameter['parameterName']]['valid_equivalence_partition']['caseSensitive'])

    valid_if_null_content, invalid_if_null_content = if_null_content_template(If_null, parameter, varchar2_equivalence_partition_basic)
    if case_sense is True:
        valid_case_sense_content = '且大小写字母敏感'
        invalid_case_sense_content = parameter['parameterName'] + '为大小写字母敏感的非法字符,如：' + \
                                     ','.join(varchar2_equivalence_partition_basic[parameter['parameterName']][
                                                  'valid_equivalence_partition']['caseSensitive'])
    else:
        valid_case_sense_content = ''
        invalid_case_sense_content = parameter['parameterName'] + '为大小写字母不敏感的非法字符,如：' + \
                                     ','.join(varchar2_equivalence_partition_basic[parameter['parameterName']][
                                                  'invalid_equivalence_partition']['caseSensitive'])
    if len(valid_char) != 0:
        valid_validChar_content_basic = '且包含'
        valid_char_copy = copy.deepcopy(valid_char)
        valid_validChar_content = ''
        if 'uppercase' in valid_char_copy:
            valid_validChar_content = valid_validChar_content + '大写字母/'
            valid_char_copy.remove('uppercase')
        if 'lowercase' in valid_char_copy:
            valid_validChar_content = valid_validChar_content + '小写字母/'
            valid_char_copy.remove('lowercase')
        if 'digits' in valid_char_copy:
            valid_validChar_content = valid_validChar_content + '数字/'
            valid_char_copy.remove('digits')
        if set(valid_char_copy).issubset(utils.OTHERMARERS):
            valid_validChar_content = valid_validChar_content + '/'.join(valid_char_copy)
    else:
        valid_validChar_content = ''

    # compose valid testcase title
    valid_validChar_content = valid_validChar_content_basic + valid_validChar_content
    if valid_if_null_content == '':
        valid_content_template = valid_content_template_basic + valid_case_sense_content + \
                                 valid_validChar_content + valid_test_data_in_content
    else:
        valid_content_template = valid_content_template_basic + valid_case_sense_content + \
                                 valid_validChar_content + valid_test_data_in_content + ', ' + valid_if_null_content
    csv_content[parameter['parameterName']]['valid_part_csv_content'] = valid_content_template

    # compose valid testcase title list
    if invalid_if_null_content == '':
        invalid_content_list = [invalid_case_sense_content]
    else:
        invalid_content_list = [invalid_if_null_content, invalid_case_sense_content]
    invalid_range_validChar_content = parameter['parameterName'] + '为长度小于' + str(parameter_range_min) + \
                                      '(不含)或者大于' + str(parameter_range_max) + '(不含)的非法字符, 如' + \
                                      ', '.join(varchar2_equivalence_partition_basic[parameter['parameterName']][
                                                   'invalid_equivalence_partition']['parameterRange_validChar'])
    invalid_content_list.append(invalid_range_validChar_content)
    csv_content[parameter['parameterName']]['invalid_part_csv_content'] = invalid_content_list
    return csv_content

def testcase_common_template(parameter, equivalence_partition_basic):
    '''
    @summary: common function for number and date type to compose testcase content
    @param parameter: tested parameter such as number or date types
    @param equivalence_partition_basic: equivalence partition dict
    @return: testcase in csv content
    '''
    If_null = parameter['ifNull']
    csv_content = {
        parameter['parameterName']: {
            'valid_part_csv_content': '',
            'invalid_part_csv_content': []
        }
    }

    # get open/close range
    open_parentheses, open_brackets, close_parentheses, close_brackets = \
        utils.check_open_close_range(parameter['parameterRange'])
    origin_start_number, origin_end_number, decimal_numbers = utils.get_start_end_data(parameter['parameterRange'])
    valid_test_data_in_content = '的合法数值, 如' + \
                                 ','.join([str(i) for i in equivalence_partition_basic[parameter['parameterName']][
                                     'valid_equivalence_partition']['parameterRange']])
    invalid_test_data_in_content = '的非法数值, 如' + ','.join(
        [str(i) for i in equivalence_partition_basic[parameter['parameterName']][
            'invalid_equivalence_partition']['parameterRange']])

    # for []
    if open_brackets and close_brackets:
        valid_content_template_basic = parameter['parameterName'] + '为数值在' + origin_start_number + '(含)到' + \
                                       origin_end_number + '(含)以内' + valid_test_data_in_content
        invalid_content_template_basic = parameter['parameterName'] + '为数值小于' + origin_start_number + '(不含)或者数值大于' + \
                                         origin_end_number + '(不含)' + invalid_test_data_in_content

    # for [):
    if open_brackets and close_parentheses:
        valid_content_template_basic = parameter['parameterName'] + '为数值在' + origin_start_number + '(含)到' + \
                                       origin_end_number + '(不含)以内' + valid_test_data_in_content
        invalid_content_template_basic = parameter['parameterName'] + '为数值小于' + origin_start_number + '(不含)或者数值大于' + \
                                         origin_end_number + '(含)' + invalid_test_data_in_content

    # for (]:
    if open_parentheses and close_brackets:
        valid_content_template_basic = parameter['parameterName'] + '为数值在' + origin_start_number + '(不含)到' + \
                                       origin_end_number + '(含)以内' + valid_test_data_in_content
        invalid_content_template_basic = parameter['parameterName'] + '为数值小于' + origin_start_number + '(含)或者数值大于' + \
                                         origin_end_number + '(不含)' + invalid_test_data_in_content

    # for ():
    if open_parentheses and close_parentheses:
        valid_content_template_basic = parameter['parameterName'] + '为数值在' + origin_start_number + '(不含)到' + \
                                       origin_end_number + '(不含)以内' + valid_test_data_in_content
        invalid_content_template_basic = parameter['parameterName'] + '为数值小于' + origin_start_number + '(含)或者数值大于' + \
                                         origin_end_number + '(含)' + invalid_test_data_in_content
    valid_if_null_content, invalid_if_null_content = if_null_content_template(If_null, parameter, equivalence_partition_basic)
    if valid_if_null_content == '':
        csv_content[parameter['parameterName']]['valid_part_csv_content'] = valid_content_template_basic
    else:
        csv_content[parameter['parameterName']]['valid_part_csv_content'] = valid_content_template_basic + \
                                                                        '，' + valid_if_null_content
    if invalid_if_null_content != '':
        csv_content[parameter['parameterName']]['invalid_part_csv_content'].append(invalid_if_null_content)
    csv_content[parameter['parameterName']]['invalid_part_csv_content'].append(invalid_content_template_basic)
    return csv_content

def testcase_number_content(parameter, number_equivalence_partition_basic):
    '''
    @summary: generate equivalence partition testcase for csv based on number type
    @param parameter: tested parameter of number type
    @param number_equivalence_partition_basic: number's equivalence partition dict
    @return: testcase in csv content
    '''
    csv_content = testcase_common_template(parameter, number_equivalence_partition_basic)
    return csv_content

def testcase_date_content(parameter, date_equivalence_partition_basic):
    '''
    @summary: generate equivalence partition testcase for csv based on date type
    @param parameter: tested parameter of date type
    @param date_equivalence_partition_basic: date's equivalence partition dict
    @return: testcase in csv content
    '''
    csv_content = testcase_common_template(parameter, date_equivalence_partition_basic)
    return csv_content

def testcase_datetime_content(parameter, datetime_equivalence_partition_basic):
    '''
    @summary: generate equivalence partition testcase for csv based on dateTime type
    @param parameter: tested parameter of date type
    @param datetime_equivalence_partition_basic: date's equivalence partition dict
    @return: testcase in csv content
    '''
    csv_content = testcase_common_template(parameter, datetime_equivalence_partition_basic)
    return csv_content

def testcase_enum_content(parameter, enum_equivalence_partition_basic):
    '''
    @summary: generate equivalence partition testcase for csv based on enum type
    @param parameter: tested parameter of date type
    @param enum_equivalence_partition_basic: enum's equivalence partition dict
    @return: testcase in csv content
    '''
    If_null = parameter['ifNull']
    csv_content = {
        parameter['parameterName']: {
            'valid_part_csv_content': '',
            'invalid_part_csv_content': []
        }
    }
    valid_if_null_content, invalid_if_null_content = if_null_content_template(If_null, parameter,
                                                                              enum_equivalence_partition_basic)
    valid_content_template_basic = parameter['parameterName'] + '的合法取值为: ' + ','.join([str(i) for i in \
        enum_equivalence_partition_basic[parameter['parameterName']]['valid_equivalence_partition']['parameterRange']])

    invalid_content_template_basic = parameter['parameterName'] + '的非法取值为: ' + ','.join([str(i) for i in \
        enum_equivalence_partition_basic[parameter['parameterName']]['invalid_equivalence_partition']['parameterRange']])

    if enum_equivalence_partition_basic[parameter['parameterName']]['invalid_equivalence_partition'].__contains__('caseSensitive') and \
        enum_equivalence_partition_basic[parameter['parameterName']]['invalid_equivalence_partition']['caseSensitive']:
        invalid_content_for_caseSense = parameter['parameterName'] + '是英文时且大小写字母敏感时的非法取值，如' + ','.join([i for i in \
            enum_equivalence_partition_basic[parameter['parameterName']]['invalid_equivalence_partition']['caseSensitive']])
        csv_content[parameter['parameterName']]['invalid_part_csv_content'].append(invalid_content_for_caseSense)
    if valid_if_null_content == '':
        csv_content[parameter['parameterName']]['valid_part_csv_content'] = valid_content_template_basic
    else:
        csv_content[parameter['parameterName']][
            'valid_part_csv_content'] = valid_content_template_basic + ', ' + valid_if_null_content
    csv_content[parameter['parameterName']]['invalid_part_csv_content'].append(invalid_content_template_basic)
    if invalid_if_null_content != '':
        csv_content[parameter['parameterName']]['invalid_part_csv_content'].append(invalid_if_null_content)
    return csv_content

def testcase_file_content(parameter, file_equivalence_partition_basic):
    '''
    @summary: generate equivalence partition testcase for csv based on file type
    @param parameter: tested parameter of file type
    @param file_equivalence_partition_basic: file's equivalence partition dict
    @return: testcase in csv content
    '''
    parameter_range_min = parameter['parameterRange'][0]
    parameter_range_max = parameter['parameterRange'][1]
    valid_char = copy.deepcopy(parameter['validChar'])
    If_null = parameter['ifNull']
    csv_content = {
        parameter['parameterName']: {
            'valid_part_csv_content': '',
            'invalid_part_csv_content': []
        }
    }
    valid_content_template_basic = parameter['parameterName'] + '为size在' + str(parameter_range_min) + 'M(含)到' + \
                                   str(parameter_range_max) + 'M(含)以内的文件且后缀名为' + ','.join([i for i in valid_char])
    valid_if_null_content, invalid_if_null_content = if_null_content_template(If_null, parameter,
                                                                              file_equivalence_partition_basic)
    invalid_content_template_basic = parameter['parameterName'] + '为size小于' + str(parameter_range_min) + \
                                     'M(不含)或者大于' + str(parameter_range_max) + 'M(不含)的非法文件size且文件后缀名为' + \
                                     ','.join([i for i in file_equivalence_partition_basic[parameter['parameterName']][
                                         'invalid_equivalence_partition']['parameterRange']])
    if valid_if_null_content == '':
        csv_content[parameter['parameterName']]['valid_part_csv_content'] = valid_content_template_basic
    else:
        csv_content[parameter['parameterName']]['valid_part_csv_content'] = valid_content_template_basic + \
                                                                        ', ' + valid_if_null_content
    if invalid_if_null_content != '':
        csv_content[parameter['parameterName']]['invalid_part_csv_content'].append(invalid_if_null_content)
    csv_content[parameter['parameterName']]['invalid_part_csv_content'].append(invalid_content_template_basic)
    return csv_content
