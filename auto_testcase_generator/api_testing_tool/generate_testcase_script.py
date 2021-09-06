#!/usr/bin/env python3
# encoding: utf-8
'''
generate testcase scripts
Created on Aug 5, 2021
@author: Guangli.bao
'''
import copy
import sys
import json
import random
import os
import csv
sys.path.append("..")
from utility import create_folder

def check_other_query_parameters(other_query_parameters, valid_part, TestSteps_tmp):
    query_str = ''
    Path = ''
    test_steps = {}
    for param in other_query_parameters:
        if 'query' == param['in']:
            if valid_part == 'valid':
                query_str = '&' + param['name'] + '=' + random.choice(param['testcases']['valid_partition']['testdata'])
            else:
                query_str = '&' + param['name'] + '=' + random.choice(param['testcases']['invalid_partition']['testdata'])
        if 'path' == param['in']:
            if valid_part == 'valid':
                Path = TestSteps_tmp.replace(param['name'], str(random.choice(param['testcases']['valid_partition']['testdata'])))
            else:
                Path = TestSteps_tmp.replace(param['name'], str(random.choice(param['testcases']['invalid_partition']['testdata'])))
        if 'header' == param['in']:
            if valid_part == 'valid':
                test_steps = {param['name']: random.choice(param['testcases']['valid_partition']['testdata'])}
            else:
                test_steps = {param['name']: random.choice(param['testcases']['invalid_partition']['testdata'])}
        if 'body' == param['in']:
            if isinstance(param['testcases']['valid_partition']['testdata'], list):
                if valid_part == 'valid':
                    test_steps = {param['name']: random.choice(param['testcases']['valid_partition']['testdata'])}
                else:
                    test_steps = {param['name']: random.choice(param['testcases']['invalid_partition']['testdata'])}
            if isinstance(param['testcases']['valid_partition']['testdata'], dict):
                if valid_part == 'valid':
                    test_steps = param['testcases']['valid_partition']['testdata']
                else:
                    test_steps = param['testcases']['invalid_partition']['testdata']
    return query_str, Path, test_steps

def combine_testcase_row_for_listdata(request_path, request_method, case_dict, other_query_parameters, responses, valid_part):
    TestSuite = request_path.replace('/', '_').strip('_')
    test_steps = ''
    Path = request_path
    Method = request_method
    execution_flag = True
    if '{' or "}" in request_path:
        TestSteps_tmp = request_path.replace('{', '').replace('}', '')
    rows = []
    if valid_part == 'valid':
        CaseID = case_dict['testcases']['valid_partition']['CaseID']
        CaseName = 'test' + '_' + case_dict['name'] + '_valid'
        Expected_status_code = '200'
        testdata = case_dict['testcases']['valid_partition']['testdata']
    else:
        CaseID = case_dict['testcases']['invalid_partition']['CaseID']
        CaseName = 'test' + '_' + case_dict['name'] + '_invalid'
        Expected_status_code = [','.join(str(k) for k, v in responses.items() if k not in [200, '200'])]
        testdata = case_dict['testcases']['invalid_partition']['testdata']
    query_str = ''
    if len(other_query_parameters) != 0:
        query_str, Path, test_steps = check_other_query_parameters(other_query_parameters, valid_part, TestSteps_tmp)
    for i in testdata:
        if 'path' == case_dict['in']:
            Path = TestSteps_tmp.replace(case_dict['name'], str(i))
        if 'query' == case_dict['in']:
            if 'array' == case_dict['type']:
                Path = request_path + '?' + i
            else:
                Path = request_path + '?' + case_dict['name'] + '=' + i + query_str
        if 'header' == case_dict['in']:
            test_steps = {case_dict['name']: i}
            test_steps = json.dumps(test_steps)
        if 0 == testdata.index(i):
            testcase_content = (CaseID, TestSuite, CaseName, test_steps, Path, Method, execution_flag, Expected_status_code, '', '', '')
            rows.append(testcase_content)
        else:
            testcase_content = ('', '', '', test_steps, Path, '', '', Expected_status_code, '', '', '', '')
            rows.append(testcase_content)
    if 'query' == case_dict['in'] and valid_part == 'valid':
        if case_dict.__contains__('allowEmptyValue') and case_dict['allowEmptyValue']:
            rows.append(('', '', '', test_steps, request_path + '?' + case_dict['name'] + query_str, '', '', Expected_status_code, '', '', '', ''))
    if 'query' == case_dict['in'] and valid_part == 'invalid':
        if not case_dict.__contains__('allowEmptyValue') or not case_dict['allowEmptyValue']:
            rows.append(('', '', '', test_steps, request_path + '?' + case_dict['name'] + query_str, '', '', Expected_status_code, '', '', '', ''))
    return rows

def combine_testcase_row_for_dictdata(request_path, request_method, case_dict, other_query_parameters, responses, valid_part):
    if '{' or "}" in request_path:
        TestSteps_tmp = request_path.replace('{', '').replace('}', '')
    rows = []
    if valid_part == 'valid':
        CaseName = 'test_' + case_dict['name'] + '_valid'
        Expected_status_code = '200'
        testdata = case_dict['testcases']['valid_partition']['testdata']
        CaseID = case_dict['testcases']['valid_partition']['CaseID']
    else:
        CaseName = 'test_' + case_dict['name'] + '_invalid'
        Expected_status_code = [','.join(str(k) for k, v in responses.items())]
        testdata = case_dict['testcases']['invalid_partition']['testdata']
        CaseID = case_dict['testcases']['invalid_partition']['CaseID']
    Path = request_path
    if len(other_query_parameters) != 0:
        query_str, Path, test_steps = check_other_query_parameters(other_query_parameters, valid_part, TestSteps_tmp)
    TestSuite = request_path.replace('/', '_').strip('_')
    test_steps = testdata
    Method = request_method
    execution_flag = True
    testcase_content = (CaseID, TestSuite, CaseName, test_steps, Path, Method, execution_flag, Expected_status_code, '', '', '')
    rows.append(testcase_content)
    return rows


def csv_writer(api_path_dir, case_file_name, csv_header, rows):
    if rows is not None:
        with open(api_path_dir + '/' + case_file_name, 'w', encoding='utf-8-sig') as csvf:
            writer = csv.writer(csvf)
            writer.writerow(csv_header)
            for i in rows:
                writer.writerow(i)

def compose_testing_data_for_post_formdata_valid(parameter_object, api_post_parameters, request_path, consumes=None):
    if '{' or "}" in request_path:
        path = request_path.replace('{', '').replace('}', '')
    TestSuite = request_path.replace('/', '_').strip('_')
    if consumes is not None:
        Method = 'post: ' + consumes[0]
    else:
        Method = 'post'
    execution_flag = True
    CaseID = parameter_object['testcases']['valid_partition']['CaseID']
    CaseName = 'test' + '_' + parameter_object['name'] + '_valid'
    Expected_status_code = '200'
    rows = []
    if 'path' == parameter_object['in']:
        test_steps = {}
        for j in api_post_parameters:
            if j['in'] == 'formData' and j.__contains__('testcases'):
                test_steps[j['name']] = random.choice(j['testcases']['valid_partition']['testdata'])
        for i in parameter_object['testcases']['valid_partition']['testdata']:
            Path = path.replace(parameter_object['name'], str(i))
            if 0 == parameter_object['testcases']['valid_partition']['testdata'].index(i):
                testcase_content = (
                CaseID, TestSuite, CaseName, test_steps, Path, Method, execution_flag, Expected_status_code, '', '', '')
                rows.append(testcase_content)
            else:
                testcase_content = ('', '', '', test_steps, Path, '', '', Expected_status_code, '', '', '', '')
                rows.append(testcase_content)
    if 'formData' == parameter_object['in'] and parameter_object.__contains__('testcases'):
        TestSteps_list = []
        for i in parameter_object['testcases']['valid_partition']['testdata']:
            test_steps = {}
            test_steps[parameter_object['name']] = i
            TestSteps_list.append(test_steps)
        temp_parameter_list = copy.deepcopy(api_post_parameters)
        temp_parameter_list.remove(parameter_object)
        for j in temp_parameter_list:
            if j['in'] == 'path':
                Path = path.replace(j['name'], str(j['testcases']['valid_partition']['testdata'][0]))
            if j['in'] == 'formData' and j.__contains__('testcases'):
                for k in TestSteps_list:
                    k[j['name']] = j['testcases']['valid_partition']['testdata'][1]
        for step in TestSteps_list:
            if 0 == TestSteps_list.index(step):
                testcase_content = (
                    CaseID, TestSuite, CaseName, step, Path, Method, execution_flag, Expected_status_code, '', '', '')
                rows.append(testcase_content)
            else:
                testcase_content = ('', '', '', step, Path, '', '', Expected_status_code, '', '', '', '')
                rows.append(testcase_content)
        for step in TestSteps_list:
            if step[parameter_object['name']] is None or step[parameter_object['name']] == '':
                break
            else:
                if not parameter_object.__contains__('allowEmptyValue') or not parameter_object['allowEmptyValue']:
                    test_step_tmp = TestSteps_list[0]
                    test_step_tmp[parameter_object['name']] = None
                    rows.append(('', '', '', test_step_tmp, Path, '', '', Expected_status_code, '', '', '', ''))
                    break
    return rows

def compose_testing_data_for_post_formdata_invalid(parameter_object, api_post_parameters, request_path, responses, consumes=None):
    if '{' or "}" in request_path:
        path = request_path.replace('{', '').replace('}', '')
    TestSuite = request_path.replace('/', '_').strip('_')
    if consumes is not None:
        Method = 'post: ' + consumes[0]
    else:
        Method = 'post'
    execution_flag = True
    CaseID = parameter_object['testcases']['invalid_partition']['CaseID']
    CaseName = 'test' + '_' + parameter_object['name'] + '_invalid'
    if '200' in responses.keys():
        del(responses['200'])
    if len(responses.keys()) == 0:
        Expected_status_code = 400
    else:
        Expected_status_code = ','.join(str(k) for k, v in responses.items())
    rows = []
    if 'path' == parameter_object['in']:
        test_steps = {}
        for j in api_post_parameters:
            if j['in'] == 'formData' and j.__contains__('testcases'):
                test_steps[j['name']] = random.choice(j['testcases']['invalid_partition']['testdata'])
        for i in parameter_object['testcases']['invalid_partition']['testdata']:
            if i is None or i == 'None' or i == 'Null' or i == '':
                Path = path.replace(parameter_object['name'], '')
            else:
                Path = path.replace(parameter_object['name'], str(i))
            if 0 == parameter_object['testcases']['invalid_partition']['testdata'].index(i):
                testcase_content = (
                CaseID, TestSuite, CaseName, test_steps, Path, Method, execution_flag, Expected_status_code, '', '', '')
                rows.append(testcase_content)
            else:
                testcase_content = ('', TestSuite, '', test_steps, Path, '', '', Expected_status_code, '', '', '', '')
                rows.append(testcase_content)
    if 'formData' == parameter_object['in'] and parameter_object.__contains__('testcases'):
        TestSteps_list = []
        for i in parameter_object['testcases']['invalid_partition']['testdata']:
            test_steps = {}
            test_steps[parameter_object['name']] = i
            TestSteps_list.append(test_steps)
        temp_parameter_list = copy.deepcopy(api_post_parameters)
        temp_parameter_list.remove(parameter_object)
        for j in temp_parameter_list:
            if j['in'] == 'path':
                Path = path.replace(j['name'], str(j['testcases']['valid_partition']['testdata'][0]))
            if j['in'] == 'formData' and j.__contains__('testcases'):
                for k in TestSteps_list:
                    k[j['name']] = j['testcases']['valid_partition']['testdata'][1]
        for step in TestSteps_list:
            if 0 == TestSteps_list.index(step):
                testcase_content = (
                    CaseID, TestSuite, CaseName, step, Path, Method, execution_flag, Expected_status_code, '', '', '')
                rows.append(testcase_content)
            else:
                testcase_content = ('', '', '', step, Path, '', '', Expected_status_code, '', '', '', '')
                rows.append(testcase_content)
        for step in TestSteps_list:
            if step[parameter_object['name']] is None or step[parameter_object['name']] == '':
                break
            else:
                if not parameter_object.__contains__('allowEmptyValue') or not parameter_object['allowEmptyValue']:
                    test_step_tmp = TestSteps_list[0]
                    test_step_tmp[parameter_object['name']] = None
                    rows.append(('', '', '', test_step_tmp, Path, '', '', Expected_status_code, '', '', '', ''))
                    break
    return rows


def compose_testing_data_for_post_formdata(parameter_object, api_post_parameters, request_path, responses, consumes = None):
    valid_rows = compose_testing_data_for_post_formdata_valid(parameter_object, api_post_parameters, request_path, consumes)
    invalid_rows = compose_testing_data_for_post_formdata_invalid(parameter_object, api_post_parameters, request_path, responses, consumes)
    return valid_rows, invalid_rows

def compose_testcase_for_no_parameter_api(request_path, request_method, request_object):
    rows = []
    CaseID = request_object['testcases']['valid_partition']['CaseID']
    execution_flag = True
    TestSuite = request_path.replace('/', '_').strip('_')
    CaseName = 'test' + '_' + TestSuite + '_valid'
    Expected_status_code = '200'
    test_steps = ''
    path = request_path
    method = request_method
    rows.append((CaseID, TestSuite, CaseName, test_steps, path, method, execution_flag, Expected_status_code, '', '', '', ''))
    return rows

def generate_auto_case_file(api_objects):
    '''
    @summary: generate api scripts for testing execution in folder: ./TestSuites
    @param api_objects: api definition
    @return: None
    '''
    case_location = os.path.dirname(os.path.realpath(__file__)) + '/TestSuites/'
    create_folder(case_location)
    csv_header = ['CaseID', 'TestSuite', 'CaseName', 'TestSteps', 'Path', 'Method', 'Execute-or-Not',
                   'Expected-status-code', 'Actual-status-code', 'Execution-result', 'Response-content']
    for k, v in api_objects.items():
        if len(v.keys()) != 0:
            api_path_dir = case_location + k.replace('/', '_').strip('_')
            create_folder(api_path_dir)
            for kk, vv in v.items():
                if len(vv['parameters']) != 0:
                    for item in vv['parameters']:
                        if item.__contains__('testcases'):
                            api_path = k.replace('/', '_').strip('_')
                            valid_case_file_name = str(item['testcases']['valid_partition']['CaseID']) + '_' + api_path + '.csv'
                            invalid_case_file_name = str(item['testcases']['invalid_partition']['CaseID']) + '_' + api_path + '.csv'
                            valid_rows = None
                            invalid_rows = None
                            # check if more than one parameters locate in query
                            other_query_parameters = []
                            if len(vv['parameters']) > 1:
                                for para in vv['parameters']:
                                    if para != item and \
                                            (para['in'] == 'query' or para['in'] == 'body' or
                                             para['in'] == 'path' or para['in'] == 'header'):
                                        other_query_parameters.append(para)
                            if ('path' == item['in'] or 'query' == item['in'] or 'header' == item['in']) \
                                            and ('get' == kk or 'delete' == kk or 'put' == kk):
                                valid_rows = combine_testcase_row_for_listdata(k, kk, item, other_query_parameters, vv['responses'], 'valid')
                                invalid_rows = combine_testcase_row_for_listdata(k, kk, item, other_query_parameters, vv['responses'], 'invalid')
                            if 'body' == item['in'] and ('post' == kk or 'put' == kk):
                                valid_rows = combine_testcase_row_for_dictdata(k, kk, item, other_query_parameters, vv['responses'], 'valid')
                                invalid_rows = combine_testcase_row_for_dictdata(k, kk, item, other_query_parameters, vv['responses'], 'invalid')
                            if ('path' == item['in'] or 'formData' == item['in']) and 'post' == kk:
                                # when post parameter locate in path, other parameters locate in formdata
                                if vv.__contains__('consumes') and ('application/x-www-form-urlencoded'
                                                                    in vv['consumes'] or 'multipart/form-data' in vv['consumes']):
                                    valid_rows, invalid_rows = compose_testing_data_for_post_formdata(item, vv['parameters'], k, vv['responses'], vv['consumes'])
                                else:
                                    valid_rows, invalid_rows = compose_testing_data_for_post_formdata(item,
                                                                                   vv['parameters'],k, vv['responses'])
                            csv_writer(api_path_dir, valid_case_file_name, csv_header, valid_rows)
                            csv_writer(api_path_dir, invalid_case_file_name, csv_header, invalid_rows)
                else:
                    api_path = k.replace('/', '_').strip('_')
                    valid_case_file_name = str(vv['testcases']['valid_partition']['CaseID']) + '_' + api_path + '.csv'
                    valid_row = compose_testcase_for_no_parameter_api(k, kk, vv)
                    csv_writer(api_path_dir, valid_case_file_name, csv_header, valid_row)




















