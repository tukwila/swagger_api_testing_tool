#!/usr/bin/env python3
# encoding: utf-8
'''
generate testcases
Created on Aug 2, 2021
@author: Guangli.bao
'''
import sys
import copy
sys.path.append("..")
import re
import json
import random
import datetime
from auto_equivalence_partition_testcase_generator import generate_equivalence_partition
from api_testing_tool import utility
import strgen
from common_tools import utils

int32_minimum = -2147483648
int32_maximum = 2147483647
int64_minimum = -9223372036854775808
int64_maximum = 9223372036854775808
number_maximum = sys.float_info.max
number_minimum = sys.float_info.min
string_maxlength = 20
string_minlength = 1


def testcase_dict_template(valid_case, invalid_case):
    testcases = {
        "valid_partition": {'testcase': '', 'testdata': []},
        "invalid_partition": {'testcase': '', 'testdata': []}
    }
    testcases['valid_partition']['testcase'] = valid_case
    testcases['invalid_partition']['testcase'] = invalid_case
    return testcases


def generate_equivalence_testcase_for_integer_number(parameter_object):
    '''
    @summary: generate equivalence partition testcase for integer or number type parameter
    @param parameter_object: integer type parameter dict
    @return: testcase dict in api object
    '''
    parameter_name = parameter_object['name']
    if parameter_object.__contains__('format'):
        parameter_format = parameter_object['format']
    if parameter_object.__contains__('schema') and parameter_object['schema'].__contains__('format'):
        parameter_format = parameter_object['schema']['format']
    if 'int32' == parameter_format:
        maximum = int32_maximum
        minimum = int32_minimum
    elif 'int64' == parameter_format:
        maximum = int64_maximum
        minimum = int64_minimum
    elif 'float' == parameter_format or 'double' == parameter_format:
        maximum = number_maximum
        minimum = number_minimum
    else:
        pass
    if parameter_object.__contains__('maximum'):
        maximum = parameter_object['maximum']
    if parameter_object.__contains__('minimum'):
        minimum = parameter_object['minimum']
    if parameter_object.__contains__('exclusiveMaximum'):
        exclusiveMaximum = parameter_object['exclusiveMaximum']
    else:
        exclusiveMaximum = False
    if parameter_object.__contains__('exclusiveMinimum'):
        exclusiveMinimum = parameter_object['exclusiveMinimum']
    else:
        exclusiveMinimum = False
    if exclusiveMaximum and exclusiveMinimum:
        parameterRange = "(" + str(minimum) + ", " + str(maximum) + ")"
        valid_case = 'Parameter name {0} valid case: in parameter value range minimum {1} (not include) and maximum {2} (not include)'.format(
            parameter_name, minimum, maximum)
        invalid_case = 'Parameter name {0} invalid case: out of parameter valid range more than maximum (not include) {1} or small than minimum (not include) {2}'.format(
            parameter_name, maximum, minimum)
    elif not exclusiveMaximum and not exclusiveMinimum:
        parameterRange = "[" + str(minimum) + ", " + str(maximum) + "]"
        valid_case = 'Parameter name {0} valid case: in parameter value range minimum {1} (include) and maximum {2} (include)'.format(
            parameter_name, minimum, maximum)
        invalid_case = 'Parameter name {0} invalid case: out of parameter valid range more than maximum (not include) {1} or small than minimum (include) {2}'.format(
            parameter_name, maximum, minimum)
    elif not exclusiveMaximum and exclusiveMinimum:
        parameterRange = "[" + str(minimum) + ", " + str(maximum) + ")"
        valid_case = 'Parameter name {0} valid case: in parameter value range minimum {1} (not include) and maximum {2} (include)'.format(
            parameter_name, minimum, maximum)
        invalid_case = 'Parameter name {0} invalid case: out of parameter valid range more than maximum (include) {1} or small than minimum (not include) {2}'.format(
            parameter_name, maximum, minimum)
    elif exclusiveMaximum and not exclusiveMinimum:
        parameterRange = "(" + str(minimum) + ", " + str(maximum) + "]"
        valid_case = 'Parameter name {0} valid case: in parameter value range minimum {1} (include) and maximum {2} (not include)'.format(
            parameter_name, minimum, maximum)
        invalid_case = 'Parameter name {0} invalid case: out of parameter valid range more than maximum (include) {1} or small than minimum (include) {2}'.format(
            parameter_name, maximum, minimum)
    else:
        pass
    testcases = testcase_dict_template(valid_case, invalid_case)
    parameter_json = {
        "parameterName": parameter_name,
        "parameterType": "number",
        "parameterRange": parameterRange,
        "ifNull": parameter_object['required']
    }
    result_for_function, result_for_testcase = \
        generate_equivalence_partition.generate_number_equivalence_partition(parameter_json)
    testcases['valid_partition']['testdata'] = result_for_function[parameter_name]['valid_equivalence_partition']
    testcases['invalid_partition']['testdata'] = result_for_function[parameter_name]['invalid_equivalence_partition']
    return testcases


def generate_equivalence_testcase_for_date(parameter_object):
    '''
    @summary: generate equivalence partition testcase for date type parameter
    @param parameter_object: integer type parameter dict
    @return: testcase dict in api object
    '''
    parameter_name = parameter_object['name']
    valid_case = 'Parameter name {0} valid case: input one valid date'.format(parameter_name)
    invalid_case = 'Parameter name {0} invalid case: input one invalid date such as incorrect year or month or day'.format(
        parameter_name)
    testcases = testcase_dict_template(valid_case, invalid_case)
    parameter_json = {
        "parameterName": parameter_name,
        "parameterType": "date",
        "parameterRange": "[" + datetime.date.max.strftime("%Y-%m-%d") + ',' + datetime.date.min.strftime("%Y-%m-%d") + "]",
        "ifNull": parameter_object['required'],
        "validChar": ["yyyy-mm-dd"]
    }
    result_for_function, result_for_testcase = \
        generate_equivalence_partition.generate_date_equivalence_partition(parameter_json)
    testcases['valid_partition']['testdata'] = result_for_function[parameter_name]['valid_equivalence_partition']
    testcases['invalid_partition']['testdata'] = result_for_function[parameter_name]['invalid_equivalence_partition']
    return testcases


def generate_equivalence_testcase_for_datetime(parameter_object):
    '''
    @summary: generate equivalence partition testcase for datetime type parameter
    @param parameter_object: integer type parameter dict
    @return: testcase dict in api object
    '''
    parameter_name = parameter_object['name']
    valid_case = 'Parameter name {0} valid case: input valid dateTime with correct format'.format(parameter_name)
    invalid_case = 'Parameter name {0} invalid case: input invalid dateTime or incorrect format'.format(parameter_name)
    testcases = testcase_dict_template(valid_case, invalid_case)
    parameter_json = {
        "parameterName": parameter_name,
        "parameterType": "datetime",
        "parameterRange": "[" + datetime.datetime.max.strftime("%Y-%m-%d %H:%M:%S") + ',' +  \
                          datetime.datetime.min.strftime("%Y-%m-%d %H:%M:%S") + "]",
        "ifNull": parameter_object['required']
    }
    result_for_function, result_for_testcase = \
        generate_equivalence_partition.generate_datetime_equivalence_partition(parameter_json)
    testcases['valid_partition']['testdata'] = result_for_function[parameter_name]['valid_equivalence_partition']
    testcases['invalid_partition']['testdata'] = result_for_function[parameter_name]['invalid_equivalence_partition']
    return testcases


def generate_equivalence_testcase_for_boolean(parameter_object):
    '''
    @summary: generate equivalence partition testcase for boolean type parameter
    @param parameter_object: integer type parameter dict
    @return: testcase dict in api object
    '''
    parameter_name = parameter_object['name']
    valid_case = 'Parameter name {0} valid case: input valid boolean value: true or false'.format(parameter_name)
    invalid_case = 'Parameter name {0} invalid case: input non boolean value'.format(parameter_name)
    testcases = testcase_dict_template(valid_case, invalid_case)
    parameter_json = {
        "parameterName": parameter_name,
        "parameterType": "boolean",
        "parameterRange": [True, False],
        "ifNull": parameter_object['required']
    }
    result_for_function, result_for_testcase = \
        generate_equivalence_partition.generate_boolean_equivalence_partition(parameter_json)
    testcases['valid_partition']['testdata'] = result_for_function[parameter_name]['valid_equivalence_partition']
    testcases['invalid_partition']['testdata'] = result_for_function[parameter_name]['invalid_equivalence_partition']
    return testcases

def generate_equivalence_testcase_for_enum(parameter_object):
    parameter_name = parameter_object['name']
    valid_case = 'Parameter name {0} valid case: input one enum value in {1}'.format(parameter_name, parameter_object['enum'])
    invalid_case = 'Parameter name {0} invalid case: input value out of enum list {1}'.format(parameter_name, parameter_object['enum'])
    testcases = testcase_dict_template(valid_case, invalid_case)
    parameter_json = {
        "parameterName": parameter_name,
        "parameterRange": parameter_object['enum'],
        "ifNull": parameter_object['required'],
        "caseSensitive": False
    }
    result_for_function, result_for_testcase = \
        generate_equivalence_partition.generate_enum_equivalence_partition(parameter_json)
    testcases['valid_partition']['testdata'] = result_for_function[parameter_name]['valid_equivalence_partition']
    testcases['invalid_partition']['testdata'] = result_for_function[parameter_name]['invalid_equivalence_partition']
    return testcases

def compose_testing_data_for_embeded_object(object, model_definitions):
    model_name = object.split('/')[-1]
    model_properties = model_definitions['definitions'][model_name]['properties']
    valid_object_testing_data = {}
    invalid_object_testing_data = {}
    for k, v in model_properties.items():
        if v.__contains__('testcases'):
            valid_object_testing_data[k] = random.choice(v['testcases']['valid_partition']['testdata'])
            invalid_object_testing_data[k] = random.choice(v['testcases']['invalid_partition']['testdata'])
        elif v.__contains__('$ref'):
            compose_testing_data_for_embeded_object(v['$ref'], model_definitions)
        else:
            pass
    return valid_object_testing_data, invalid_object_testing_data

def compose_testing_data_for_array_object(object, model_definitions):
    valid_embeded_object_array = []
    invalid_embeded_object_array = []
    for i in range(1, random.randint(2, 4)):
        valid_embeded_object_dict, invalid_embeded_object_dict = \
            compose_testing_data_for_embeded_object(object, model_definitions)
        valid_embeded_object_array.append(valid_embeded_object_dict)
        invalid_embeded_object_array.append(invalid_embeded_object_dict)
    return valid_embeded_object_array, invalid_embeded_object_array


def generate_equivalence_testcase_for_object(parameter_object, isArray, model_definitions):
    def generate_testing_data_for_object(model_definitions):
        valid_object_testing_data = {}
        invalid_object_testing_data = {}
        for k, v in model_properties.items():
            if v.__contains__('testcases'):
                valid_object_testing_data[k] = random.choice(v['testcases']['valid_partition']['testdata'])
                invalid_object_testing_data[k] = random.choice(v['testcases']['invalid_partition']['testdata'])
            elif v.__contains__('$ref'):
                valid_object_testing_data[k], invalid_object_testing_data[k] = \
                    compose_testing_data_for_embeded_object(v['$ref'], model_definitions)
            elif v.__contains__('type') and 'array' in v['type']:
                if v['items'].__contains__('$ref'):
                    valid_object_testing_data[k], invalid_object_testing_data[k] = \
                        compose_testing_data_for_array_object(v['items']['$ref'], model_definitions)
            else:
                pass
        return valid_object_testing_data, invalid_object_testing_data
    if not isArray:
        valid_case = 'Parameter name {0} is object valid case: parameters in object body are valid'.format(
                                                                                                parameter_object['name'])
        invalid_case = 'Parameter name {0} is object invalid case: parameters in object body are invalid '.format(
                                                                                                 parameter_object['name'])
        testcases = testcase_dict_template(valid_case, invalid_case)
        model_name = parameter_object['schema']['$ref'].split('/')[-1]
        model_properties = model_definitions['definitions'][model_name]['properties']
        testcases['valid_partition']['testdata'], testcases['invalid_partition']['testdata'] = \
                                                    generate_testing_data_for_object(model_definitions)
    else:
        valid_case = 'Parameter name {0} is object array valid case: parameters in object body are valid'.format(
                                                                                                parameter_object['name'])
        invalid_case = 'Parameter name {0} is object array invalid case: parameters in object body are invalid '.format(
                                                                                                 parameter_object['name'])
        testcases = testcase_dict_template(valid_case, invalid_case)
        model_name = parameter_object['schema']['items']['$ref'].split('/')[-1]
        model_properties = model_definitions['definitions'][model_name]['properties']
        valid_array = []
        invalid_array = []
        for i in range(1, random.randint(2, 4)):
            valid_data, invalid_data = generate_testing_data_for_object(model_definitions)
            valid_array.append(valid_data)
            invalid_array.append(invalid_data)
        testcases['valid_partition']['testdata'] = valid_array
        testcases['invalid_partition']['testdata'] = invalid_array
    return testcases

def generate_equivalence_testcase_for_enum_array_2(parameter_object):
    '''
    @summary: openAPI2 generate equivalence partition testcase for array that values in array are enum
    @param parameter_object: array type parameter dict
    @return: testcase dict in api object
    '''
    valid_case = 'Parameter name {0} location in {1} collectionFormat == {2} valid case: input any ' \
                 'request data within enum range {3}'.format(parameter_object['name'],
                                                             parameter_object['in'],
                                                             parameter_object['collectionFormat'],
                                                             parameter_object['items']['enum'])
    invalid_case = 'Parameter name {0} location in {1} collectionFormat == {2} valid case: input any ' \
                   'request data without enum range {3}'.format(parameter_object['name'],
                                                                parameter_object['in'],
                                                                parameter_object['collectionFormat'],
                                                                parameter_object['items']['enum'])
    testcases = testcase_dict_template(valid_case, invalid_case)
    # genenrate testing data for enum_array
    testcases['valid_partition']['testdata'] = []
    testcases['invalid_partition']['testdata'] = []
    enum_list = parameter_object['items']['enum']
    if parameter_object.__contains__('collectionFormat') and 'multi' == parameter_object['collectionFormat']:
        testcases['valid_partition']['testdata'].append(parameter_object['name'] + '=' + random.choice(enum_list))
        all_enum_value = ''
        for i in enum_list:
            all_enum_value = (all_enum_value + '&' + parameter_object['name'] + '=' + i).strip('&')
        testcases['valid_partition']['testdata'].append(all_enum_value)
        testcases['invalid_partition']['testdata'].append(parameter_object['name'] + '=')
        more_enum_value1 = all_enum_value + '&' + parameter_object['name'] + '=' + random.choice(enum_list)
        more_enum_value2 = all_enum_value + '&' + parameter_object['name'] + '=' + random.choice(enum_list) + 'aa'
        testcases['invalid_partition']['testdata'].append(more_enum_value1)
        testcases['invalid_partition']['testdata'].append(more_enum_value2)
        testcases['invalid_partition']['testdata'].append(parameter_object['name'] + ':' + random.choice(enum_list)
                                                          + '&' + parameter_object['name'] + ':' + random.choice(
                                                                                                        enum_list))
    return testcases

def generate_equivalence_testcase_for_enum_array_3(parameter_object):
    '''
    @summary: openAPI3 generate equivalence partition testcase for array that values in array are enum
    @param parameter_object: array type parameter dict
    @return: testcase dict in api object
    '''
    valid_case = 'Parameter name {0} location in {1} style == {2} explode == {3} valid case: input any ' \
                 'request data within enum range {4}'.format(parameter_object['name'],
                                                             parameter_object['in'],
                                                             parameter_object['style'],
                                                             parameter_object['explode'],
                                                             parameter_object['schema']['enum'])
    invalid_case = 'Parameter name {0} location in {1} style == {2} explode == {3} valid case: input any ' \
                   'request data without enum range {4}'.format(parameter_object['name'],
                                                                parameter_object['in'],
                                                                parameter_object['style'],
                                                                parameter_object['explode'],
                                                                parameter_object['schema']['enum'])
    testcases = testcase_dict_template(valid_case, invalid_case)
    # genenrate testing data for enum_array
    testcases['valid_partition']['testdata'] = []
    testcases['invalid_partition']['testdata'] = []
    enum_list = parameter_object['schema']['enum']
    testcases['valid_partition']['testdata'].append(parameter_object['name'] + '=' + random.choice(enum_list))
    if parameter_object.__contains__('explode') and parameter_object['explode'] is True:
        all_enum_value = ''
        for i in enum_list:
            all_enum_value = (all_enum_value + '&' + parameter_object['name'] + '=' + i).strip('&')
        more_enum_value1 = all_enum_value + '&' + parameter_object['name'] + '=' + random.choice(enum_list)
        more_enum_value2 = all_enum_value + '&' + parameter_object['name'] + '=' + random.choice(enum_list) + 'aa'
        testcases['invalid_partition']['testdata'].append(parameter_object['name'] + ':' + random.choice(enum_list)
                                                          + '&' + parameter_object['name'] + ':' + random.choice(
                                                                                                        enum_list))
    if parameter_object.__contains__('explode') and parameter_object['explode'] is False:
        all_enum_value = ','.join(i for i in enum_list)
        more_enum_value1 = all_enum_value + ',' + random.choice(enum_list)
        more_enum_value2 = all_enum_value + ',' + random.choice(enum_list) + 'aa'
        testcases['invalid_partition']['testdata'].append(parameter_object['name'] + ':' + random.choice(enum_list))
    testcases['valid_partition']['testdata'].append(all_enum_value)
    testcases['invalid_partition']['testdata'].append(parameter_object['name'] + '=')
    testcases['invalid_partition']['testdata'].append(more_enum_value1)
    testcases['invalid_partition']['testdata'].append(more_enum_value2)
    return testcases


def generate_partition_testcase_for_primitive_data_type_2(item):
    item['testcases'] = None
    if 'integer' == item['type'] or 'number' == item['type']:
        item['testcases'] = generate_equivalence_testcase_for_integer_number(item)
    elif 'string' == item['type'] and not item.__contains__('format'):
        item['testcases'] = generate_equivalence_testcase_for_string(item)
    elif 'string' == item['type'] and 'date' == item['format']:
        item['testcases'] = generate_equivalence_testcase_for_date(item)
    elif 'string' == item['type'] and 'date-time' == item['format']:
        item['testcases'] = generate_equivalence_testcase_for_datetime(item)
    elif 'boolean' == item['type']:
        item['testcases'] = generate_equivalence_testcase_for_boolean(item)
    elif 'array' == item['type']:
        if 'string' == item['items']['type'] and item['items'].__contains__('enum'):
            item['testcases'] = generate_equivalence_testcase_for_enum_array_2(item)
    else:
        pass
    return item['testcases']

def generate_partition_testcase_for_primitive_data_type_3(item):
    item['testcases'] = None
    if item.__contains__('schema') and not item.__contains__('type'):
        if 'integer' == item['schema']['type'] or 'number' == item['schema']['type']:
            item['testcases'] = generate_equivalence_testcase_for_integer_number(item)
        elif 'string' == item['schema']['type'] and not item['schema'].__contains__('format') and not item['schema'].__contains__('enum'):
            item['testcases'] = generate_equivalence_testcase_for_string(item)
        elif 'string' == item['schema']['type'] and item['schema'].__contains__('format') and 'date' == item['schema']['format']:
            item['testcases'] = generate_equivalence_testcase_for_date(item)
        elif 'string' == item['schema']['type'] and item['schema'].__contains__('format') and 'date-time' == item['schema']['format']:
            item['testcases'] = generate_equivalence_testcase_for_datetime(item)
        elif item['schema'].__contains__('enum'):
            item['testcases'] = generate_equivalence_testcase_for_enum_array_3(item)
        elif 'boolean' == item['schema']['type']:
            item['testcases'] = generate_equivalence_testcase_for_boolean(item)
        elif 'array' == item['schema']['type']:
            if 'string' == item['schema']['items']['type'] and item['schema']['items'].__contains__('enum'):
                item['testcases'] = generate_equivalence_testcase_for_enum_array_3(item)
        else:
            pass
    if item.__contains__('type') and not item.__contains__('schema'):
        if 'integer' == item['type'] or 'number' == item['type']:
            item['testcases'] = generate_equivalence_testcase_for_integer_number(item)
        elif 'string' == item['type'] and not item.__contains__('format'):
            item['testcases'] = generate_equivalence_testcase_for_string(item)
        elif 'string' == item['type'] and 'date' == item['format']:
            item['testcases'] = generate_equivalence_testcase_for_date(item)
        elif 'string' == item['type'] and 'date-time' == item['format']:
            item['testcases'] = generate_equivalence_testcase_for_datetime(item)
        elif 'boolean' == item['type']:
            item['testcases'] = generate_equivalence_testcase_for_boolean(item)
        else:
            pass
    return item['testcases']

'''
def compose_object_parameter(parameter_object, model_definitions):
    new_parameter_list = []
    model_name = parameter_object.split('/')[-1]
    model_properties = model_definitions['definitions'][model_name]['properties']
    for k, v in model_properties.items():
        temp_para_object = {}
        temp_para_object['model_object'] = parameter_object
        if not v.__contains__('type'):
            temp_para_object['schema_$ref'] = v['$ref']
            new_parameter_list += compose_object_parameter(v['$ref'], model_definitions)
        else:
            temp_para_object['type'] = v['type']
        temp_para_object['name'] = k
        temp_para_object['in'] = 'body'
        if model_definitions['definitions'][model_name].__contains__('required') and k in \
                model_definitions['definitions'][model_name]['required']:
            temp_para_object['required'] = True
        else:
            temp_para_object['required'] = False
        if v.__contains__('format'):
            temp_para_object['format'] = v['format']
        elif v.__contains__('enum'):
            temp_para_object['format'] = 'enum'
            temp_para_object['enum'] = v['enum']
        else:
            pass
        generate_partition_testcase_for_primitive_data_type(temp_para_object)
        new_parameter_list.append(temp_para_object)
    return new_parameter_list
'''



def generate_parameter_equivalence_for_model_definition(model_definitions):
    '''
    @summary: analyze swagger api model definitions which is model objects to generate body testing data
    @param model_definitions: swagger api model definitions
    @return: None
    '''
    for k, v in model_definitions.items():
        for kk, vv in v.items():
            for model, value in vv['properties'].items():
                tmp_dict = copy.deepcopy(value)
                tmp_dict['name'] = model
                tmp_dict['required'] = False
                if vv.__contains__('required') and model in vv['required']:
                    tmp_dict['required'] = True
                if tmp_dict.__contains__('type'):
                    if 'integer' == tmp_dict['type'] or 'number' == tmp_dict['type']:
                        value['testcases'] = generate_equivalence_testcase_for_integer_number(tmp_dict)
                    elif 'string' == tmp_dict['type'] and not tmp_dict.__contains__('format') and not tmp_dict.__contains__('enum'):
                        value['testcases'] = generate_equivalence_testcase_for_string(tmp_dict)
                    elif 'string' == tmp_dict['type'] and tmp_dict.__contains__('enum'):
                        value['testcases'] = generate_equivalence_testcase_for_enum(tmp_dict)
                    elif 'string' == tmp_dict['type'] and 'date' == tmp_dict['format']:
                        value['testcases'] = generate_equivalence_testcase_for_date(tmp_dict)
                    elif 'string' == tmp_dict['type'] and 'date-time' == tmp_dict['format']:
                        value['testcases'] = generate_equivalence_testcase_for_datetime(tmp_dict)
                    elif 'boolean' == tmp_dict['type']:
                        value['testcases'] = generate_equivalence_testcase_for_boolean(tmp_dict)
                    elif 'array' == tmp_dict['type'] and tmp_dict.__contains__('items'):
                            if tmp_dict['items'].__contains__('type') and 'string' == tmp_dict['items']['type']:
                                value['testcases'] = generate_equivalence_testcase_for_array_string(tmp_dict)
                            else:
                                pass
                else:
                    pass

def generate_equivalence_testcase_for_array_string(parameter_object):
    valid_testdata_list = []
    invalid_testdata_list = []
    for i in range(1, random.randint(2, 5)):
        testcases = generate_equivalence_testcase_for_string(parameter_object)
        for j in testcases['valid_partition']['testdata']:
            valid_testdata_list.append(j)
        for j in testcases['invalid_partition']['testdata']:
            invalid_testdata_list.append(j)
    step = random.randint(1, len(valid_testdata_list)-1)
    valid_testdata_2dlist = []
    invalid_testdata_2dlist = []
    for i in range(0, len(valid_testdata_list), step):
        valid_testdata_2dlist.append(valid_testdata_list[i: i+step])
    for i in range(0, len(invalid_testdata_list), step):
        invalid_testdata_2dlist.append(invalid_testdata_list[i: i+step])
    testcases['valid_partition']['testdata'] = valid_testdata_2dlist
    testcases['invalid_partition']['testdata'] = invalid_testdata_2dlist
    return testcases

def generate_equivalence_testcase_based_on_pattern(parameter_object):
    pattern_str = parameter_object['pattern']
    try:
        valid_testing_data = strgen.StringGenerator(pattern_str).render()
    except Exception as e:
        raise 'Pattern string {0} is not correct: {1}'.format(pattern_str, e)
    invalid_testing_data = valid_testing_data[0: 2] + random.choice(' !@#$%^&*()') + valid_testing_data[4:]
    valid_case = 'Parameter name {0} with matched pattern: {} valid case'.format(parameter_object['name'], pattern_str)
    invalid_case = 'Parameter name {0} with not matched pattern: {} invalid case'.format(parameter_object['name'], pattern_str)
    testcases = testcase_dict_template(valid_case, invalid_case)
    testcases['valid_partition']['testdata'] = [valid_testing_data]
    testcases['invalid_partition']['testdata'] = [invalid_testing_data]
    if_null_list = ['None', '']
    for i in if_null_list:
        if parameter_object['ifNull'] is True:
            testcases['invalid_partition']['testdata'].append(i)
        else:
            testcases['valid_partition']['testdata'].append(i)
    return testcases


def generate_equivalence_testcase_for_string(parameter_object):
    '''
    @summary: generate equivalence partition testcase for integer or number type parameter
    @param parameter_object: integer type parameter dict
    @return: testcase
    '''
    parameter_name = parameter_object['name']
    if parameter_object.__contains__('maxLength'):
        maxLength = parameter_object['maxLength']
    else:
        maxLength = string_maxlength
    if parameter_object.__contains__('minLength'):
        minLength = parameter_object['minLength']
    else:
        minLength = string_minlength

    # if pattern is provided, pattern equivalence partition is higher than parameterRange/validChar/caseSensitive
    if parameter_object.__contains__('pattern') and parameter_object['pattern']:
        return generate_equivalence_testcase_based_on_pattern(parameter_object)
    # if no pattern in parameter attribute, testing data is generated based on parameterRange/validChar/caseSensitive
    valid_case = 'Parameter name {0} valid case: in string length range minimum {1} (include) and maximum {2} (include)'.format(
        parameter_name, minLength, maxLength)
    invalid_case = 'Parameter name {0} invalid case: out of string valid length range: shorter than minimum {1} or longer than maximum {2}'.format(
        parameter_name, minLength, maxLength)
    testcases = testcase_dict_template(valid_case, invalid_case)
    parameter_json = {
        "parameterName": parameter_name,
        "parameterType": "VARCHAR2",
        "parameterRange": [minLength, maxLength],
        "ifNull": parameter_object['required'],
        "validChar": [
            "uppercase",
            "lowercase",
            "."
        ],
        "caseSensitive": False
    }
    result_for_function, result_for_testcase = \
        generate_equivalence_partition.generate_varchar_equivalence_partition(parameter_json)
    # if parameter locate in header， utils.NONASCII testing data should be removed
    if parameter_object.__contains__('in') and parameter_object['in'] == 'header':
        for i in result_for_function[parameter_name]['invalid_equivalence_partition']:
            if utils.check_chinese_string(i):
                result_for_function[parameter_name]['invalid_equivalence_partition'].remove(i)
    testcases['valid_partition']['testdata'] = result_for_function[parameter_name]['valid_equivalence_partition']
    testcases['invalid_partition']['testdata'] = result_for_function[parameter_name]['invalid_equivalence_partition']
    return testcases

def generate_equivalence_testcase_2(api_objects, model_definitions, csv_case_file):
    '''
    @summary: generate equivalence partition testcase for every openAPI2 parameters
    @param api_objects: api definition
    @param model_definitions: object definition
    @return: None
    '''
    generate_parameter_equivalence_for_model_definition(model_definitions)
    with open('./TestResult/models_definitions.json', 'w', encoding='utf-8-sig') as fj:
        fj.write(json.dumps(model_definitions, indent=2))
    for k, v in api_objects.items():
        for kk, vv in v.items():
            for item in vv['parameters']:
                if item.__contains__('type') and item['type'] in ['string', 'integer','number', 'boolean','array']:
                    generate_partition_testcase_for_primitive_data_type_2(item)
                if item.__contains__('schema'):
                    if item['schema'].__contains__('$ref'):
                        item['testcases'] = generate_equivalence_testcase_for_object(item, False, model_definitions)
                    if item['schema'].__contains__('type') and 'array' == item['schema']['type']:
                        item['testcases'] = generate_equivalence_testcase_for_object(item, True, model_definitions)
    # compensate CaseID and no parameter API
    utility.append_CaseID_for_case(api_objects)
    # generate testcases and save to csv file
    utility.openAPI_csv_writer(csv_case_file, api_objects)
    with open('./TestResult/api_objects.json', 'w', encoding='utf-8-sig') as fj:
        fj.write(json.dumps(api_objects, indent=2))


def generate_equivalence_testcase_3(api_objects, model_definitions, csv_case_file, api_version):
    '''
    @summary: generate equivalence partition testcase for every openAPI3 parameters
    @param api_objects: api definition
    @param model_definitions: object definition
    @return: None
    '''
    generate_parameter_equivalence_for_model_definition(model_definitions)
    with open('./TestResult/models_definitions.json', 'w', encoding='utf-8-sig') as fj:
        fj.write(json.dumps(model_definitions, indent=2))
    for path_k, path_v in api_objects.items():
        for method_key, method_v in path_v.items():
            if method_v.__contains__('requestBody'):
                ref_object = ''
                for body_k, body_v in method_v['requestBody']['content'].items():
                    if body_v['schema'].__contains__('$ref'):
                        temp_dict = {'name': 'requestBody',
                                     'schema': {'$ref': '#/definitions/' + body_v['schema']['$ref'].split('/')[-1]}}
                        if body_v['schema']['$ref'] != ref_object:
                            body_v['schema']['testcases'] = generate_equivalence_testcase_for_object(temp_dict, False,
                                                                                                     model_definitions)
                            ref_object = body_v['schema']['$ref']
                    if body_v['schema'].__contains__('type') and 'array' == body_v['schema']['type']:
                        temp_dict = {'name': 'requestBody',
                                     'schema': {'type': 'array', 'items': {'$ref': '#/definitions/' + body_v['schema']['items']['$ref'].split('/')[-1]}}}
                        if body_v['schema']['items']['$ref'] != ref_object:
                            body_v['schema']['testcases'] = generate_equivalence_testcase_for_object(temp_dict, True,
                                                                                                     model_definitions)
                            ref_object = body_v['schema']['items']['$ref']
                    if body_v['schema'].__contains__('properties'):
                        if body_v['schema'].__contains__('required'):
                            body_v['schema']['required'].remove('file')
                        for k, v in body_v['schema']['properties'].items():
                            if v['type'] in ['string', 'integer', 'number', 'boolean', 'array']:
                                temp_dict = {'name': k, 'type': v['type']}
                                if body_v['schema'].__contains__('required') and k in body_v['schema']['required']:
                                    temp_dict['required'] = True
                                else:
                                    temp_dict['required'] = False
                                if v.__contains__('format'):
                                    temp_dict['format'] = v['format']
                                v['testcases'] = generate_partition_testcase_for_primitive_data_type_3(temp_dict)
            if method_v.__contains__('parameters'):
                for item in method_v['parameters']:
                    if item.__contains__('schema') and item['schema']['type'] in ['string', 'integer','number', 'boolean','array']:
                        generate_partition_testcase_for_primitive_data_type_3(item)
    # compensate CaseID and no parameter API
    # generate testcases and save to csv file
    #utility.openAPI_csv_writer(csv_case_file, api_objects)
    with open('./TestResult/api_objects.json', 'w', encoding='utf-8-sig') as fj:
        fj.write(json.dumps(api_objects, indent=2))


def generate_equivalence_testcase(api_objects, model_definitions, output_path, api_version):
    if api_version == 2:
        generate_equivalence_testcase_2(api_objects, model_definitions, output_path)
    if api_version == 3:
        generate_equivalence_testcase_3(api_objects, model_definitions, output_path, api_version)

def generate_orthogonal_testcase(api_objects):
    '''
    @summary: generate orthogonal array testcase for api that include more than 2 parameters(1 parameter cannot generate array)
    @param api_objects: all to be test api
    @return: testcases based on orthogonal array method
    '''
    # todo
