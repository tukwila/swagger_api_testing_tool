#!/usr/bin/env python3
# encoding: utf-8
'''
execute testcases and save result
Created on Aug 2, 2021
@author: Guangli.bao
'''
import csv
import requests
import json
import pytest_check as check
import os
import logging
from requests_toolbelt import MultipartEncoder
from urllib.request import quote

def execute_api_scripts(swagger_base_url, api_testcase_scripts, caselogger):
    '''
    @summary: do some preparation such as create directory and create new log instance
    @param swagger_base_url: swagger api url
    @param api_testcase_scripts: api test case scripts
    @param logger: log instance for every test case
    @return: None
    '''
    caselogger.info('------------Execute testcase ID: {0}, name: {1}, Execute-or-Not: {2}'.format(
            api_testcase_scripts[0]['CaseID'], api_testcase_scripts[0]['CaseName'], api_testcase_scripts[0]['Execute-or-Not']))
    if api_testcase_scripts[0]['Execute-or-Not']:
        caselogger.info('request method: {0}'.format(api_testcase_scripts[0]['Method']))
        default_headers = {
            'accept': 'application/json'
        }
        for case in api_testcase_scripts:
            caselogger.info('origin request url: {0}'.format(swagger_base_url + case['Path']))
            url = swagger_base_url + quote(case['Path'])
            caselogger.info('quote url: {0}'.format(url))
            caselogger.info('test step: {0}'.format(case['TestSteps']))
            if 'get' == api_testcase_scripts[0]['Method']:
                resp = requests.get(url)
            if 'post' == api_testcase_scripts[0]['Method']:
                data = eval(case['TestSteps'])
                caselogger.info('request data: {0}， type: {1}'.format(data, type(data)))
                resp = requests.post(url, json=data, headers=default_headers)
            if 'post:' in api_testcase_scripts[0]['Method']:
                headers = default_headers
                header_content_type = api_testcase_scripts[0]['Method'].split(':')[-1].strip()
                if 'multipart/form-data' == header_content_type:
                    data = eval(case['TestSteps'])
                    caselogger.info('request data: {0}， type: {1}'.format(data, type(data)))
                    m = MultipartEncoder(fields=data)
                    resp = requests.post(url, data=m, headers={'Content-Type': m.content_type})
                elif 'application/x-www-form-urlencoded' == header_content_type:
                    headers = default_headers
                    headers['Content-Type'] = header_content_type
                    data = eval(case['TestSteps'])
                    caselogger.info('request data: {0}， type: {1}'.format(data, type(data)))
                    caselogger.info('request headers: {0}'.format(headers))
                    resp = requests.post(url, params=data, headers=headers)
                    del(headers['Content-Type'])
            if 'put' == api_testcase_scripts[0]['Method']:
                data = eval(case['TestSteps'])
                caselogger.info('request data: {0}， type: {1}'.format(data, type(data)))
                resp = requests.put(url, json=data, headers=default_headers)
                caselogger.info('request headers: {0}'.format(default_headers))
            if 'delete' == api_testcase_scripts[0]['Method']:
                headers = default_headers
                if case['TestSteps']:
                    for k, v in eval(case['TestSteps']).items():
                        headers[k] = v
                caselogger.info('request headers: {0}'.format(headers))
                resp = requests.delete(url, headers=headers)
            if 'head' == api_testcase_scripts[0]['Method']:
                # todo
                pass
            if 'options' == api_testcase_scripts[0]['Method']:
                # todo
                pass
            if 'patch' == api_testcase_scripts[0]['Method']:
                # todo
                pass
            case['Actual-status-code'] = resp.status_code
            #if check.is_in(str(resp.status_code), case['Expected-status-code']):
            if str(resp.status_code) in case['Expected-status-code']:
                case['Execution-result'] = 'PASS'
            else:
                case['Execution-result'] = 'Fail'
            case['Response-content'] = json.dumps(resp.text)
            caselogger.info('expected status code: {0}'.format(case['Expected-status-code']))
            caselogger.info('actual response status code: {0}'.format(resp.status_code))
            caselogger.info('actual response content: {0}'.format(resp.text))
            caselogger.info('testing result: {0}'.format(case['Execution-result']))

def collect_testcases(test_scripts_path):
    all_case_file = []
   # for root, dirs, files in os.walk('./TestSuites'):
    for root, dirs, files in os.walk(test_scripts_path):
        for file in files:
            if file.endswith('csv'):
                all_case_file.append(os.path.join(root, file))
    return all_case_file

def create_case_log(case_file_name):
    caselogger = logging.getLogger('')
    if caselogger is not None:
        for handler in caselogger.handlers[:]:
            handler.stream.close()
            caselogger.removeHandler(handler)
    logfile_name = case_file_name.split('.csv')[0] + '.log'
    if os.path.exists(logfile_name):
        os.remove(logfile_name)
    logfile = logging.FileHandler(filename=logfile_name, mode='w')
    formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
    logfile.setFormatter(formatter)
    caselogger.addHandler(logfile)
    return caselogger

def execute_testcase(swagger_base_url, test_scripts_path):
    all_testcase_requests = {}
    all_case_file = collect_testcases(test_scripts_path)
    for case in all_case_file:
        case_requests = []
        csv.field_size_limit(500 * 1024 * 1024)
        with open(case, 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)
            for row in csv_reader:
                case_dict = {}
                case_dict['CaseID'] = row[0]
                case_dict['TestSuite'] = row[1]
                case_dict['CaseName'] = row[2]
                case_dict['TestSteps'] = row[3]
                case_dict['Path'] = row[4]
                case_dict['Method'] = row[5]
                case_dict['Execute-or-Not'] = row[6]
                case_dict['Expected-status-code'] = row[7]
                # case_dict['Actual-status-code'] = row[8]
                # case_dict['Execution-result'] = row[9]
                # case_dict['Response-content'] = row[10]
                case_requests.append(case_dict)
        all_testcase_requests[case] = case_requests
    # execute case scripts
    for key, value in all_testcase_requests.items():
        caselogger = create_case_log(key)
        execute_api_scripts(swagger_base_url, value, caselogger)
    # write execute result into csv
    with open('./TestResult/all_testcase_requests.json', 'w') as jf:
        jf.write(json.dumps(all_testcase_requests, indent=2))
    # write execution result to csv
    for case in all_case_file:
        new_case_name = case.split('.csv')[0] + '_new.csv'
        csv_headers = ['CaseID', 'TestSuite', 'CaseName', 'TestSteps', 'Path', 'Method', 'Execute-or-Not',
                       'Expected-status-code', 'Actual-status-code', 'Execution-result', 'Response-content']
        with open(new_case_name, 'w', encoding='utf-8-sig') as csvf:
            writer = csv.writer(csvf)
            writer.writerow(csv_headers)
            for data in all_testcase_requests[case]:
                writer.writerow([data['CaseID'],
                                 data['TestSuite'],
                                 data['CaseName'],
                                 data['TestSteps'],
                                 data['Path'],
                                 data['Method'],
                                 data['Execute-or-Not'],
                                 data['Expected-status-code'],
                                 data['Actual-status-code'],
                                 data['Execution-result'],
                                 data['Response-content']])
        os.remove(case)
        os.rename(new_case_name, case)
    return all_testcase_requests

