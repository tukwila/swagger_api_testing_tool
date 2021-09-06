#!/usr/bin/env python3
# encoding: utf-8
'''
Provide common utilities for openAPI testing tool
Created on Aug 9, 2021
@author: Guangli.bao
'''
import csv
import os
from log import logger as logging

def openAPI_csv_writer(path, result):
    '''
    @summary: store openAPI api equivalence partition result into csv file
    @param path: output csv file path
    @param result: csv content
    @return: None
    '''
    csv_headers = ['Index', 'TestSuite', 'TestCase', 'TestData']
    rows = []
    for k, v in result.items():
        if isinstance(v, dict):
            for name, value in v.items():
                TestSuite = name + ' ' + k
                if len(value['parameters']) != 0:
                    for para in value['parameters']:
                        # for file parameter, there is no testcases now [20210902]
                        if not para.__contains__('testcases'):
                            continue
                        if para['testcases'].__contains__('valid_partition'):
                            TestCase = para['testcases']['valid_partition']['testcase']
                            if isinstance(para['testcases']['valid_partition']['testdata'], list):
                                TestData = [str(i) + ' ' for i in para['testcases']['valid_partition']['testdata']]
                            if isinstance(para['testcases']['valid_partition']['testdata'], dict):
                                TestData = para['testcases']['valid_partition']['testdata']
                            testcase_content = (para['testcases']['valid_partition']['CaseID'], TestSuite, TestCase, TestData)
                            rows.append(testcase_content)
                        if para['testcases'].__contains__('invalid_partition'):
                            TestCase = para['testcases']['invalid_partition']['testcase']
                            if isinstance(para['testcases']['invalid_partition']['testdata'], list):
                                TestData = [str(i) + ' ' for i in para['testcases']['invalid_partition']['testdata']]
                            if isinstance(para['testcases']['invalid_partition']['testdata'], dict):
                                TestData = para['testcases']['invalid_partition']['testdata']
                            testcase_content = (para['testcases']['invalid_partition']['CaseID'], TestSuite, TestCase, TestData)
                            rows.append(testcase_content)
                else:
                    rows.append((value['testcases']['valid_partition']['CaseID'], TestSuite,
                                                        value['testcases']['valid_partition']['testcase'],
                                                         value['testcases']['valid_partition']['testdata']))
        else:
            msg = 'Equivalence partition result is not Dict, cannot write into csv'
            logging.error(msg)
            raise Exception(msg)
    with open(path, 'w', encoding='utf-8-sig') as csvf:
        writer = csv.writer(csvf)
        writer.writerow(csv_headers)
        for i in rows:
            writer.writerow(i)
    logging.info('testcases write into csv: {}'.format(path))

def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        del_list = os.listdir(path)
        if len(del_list) != 0:
            for i in del_list:
                if os.path.isfile(path + '/' + i):
                    os.system('rm ' + path + '/' + i)
                if os.path.isdir(path + '/' + i):
                    os.system('rm -rf ' + path + '/' + i)

def append_CaseID_for_case(api_objects):
    count = 1
    for k, v in api_objects.items():
        for name, value in v.items():
            if len(value['parameters']) != 0:
                for para in value['parameters']:
                    if not para.__contains__('testcases'):
                        continue
                    para['testcases']['valid_partition']['CaseID'] = count
                    count += 1
                    para['testcases']['invalid_partition']['CaseID'] = count
                    count += 1
            else:
                if 'get' == name:
                    value['testcases'] = {'valid_partition': {}}
                    value['testcases']['valid_partition']['CaseID'] = count
                    value['testcases']['valid_partition']['testcase'] = 'For no parameter API, just request api itself'
                    value['testcases']['valid_partition']['testdata'] = ''
                    count += 1


