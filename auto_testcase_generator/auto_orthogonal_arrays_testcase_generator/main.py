#!/usr/bin/env python3
# encoding: utf-8
'''
The tool to auto-generate orthogonal arrays testcases
Created on Jul 13, 2021
@author: Guangli.bao
'''
import json
import getopt
import sys
import time
from log import logging as logging
from orthogonal_arrays import *
from common_tools.utils import orthogonal_array_csv_writer
from common_tools.utils import swagger_orthogonal_array_csv_writer
from common_tools.get_swagger_api_docs import compose_orthogonal_request_json_from_swagger

def usage():
    '''
    @summary: usage info
    @param : None
    @return: None
    '''
    print("""
    The usage this orthogonal array testcase automotive generation tool:
    -i input filepath e.g. -i /Users/user/test.json
    -s swagger url e.g. -s http://127.0.0.1:8080/v2/api-docs
    -o output testcase file: csv format  e.g. -o /Users/user/test.csv
    e.g.
    python3 main.py -i /Users/user/test.json -o /Users/user/test.csv
    or
    python3 main.py -s http://127.0.0.1:8080/v2/api-docs -o /Users/user/test.csv
    """)

def print_help_exit():
    '''
    @summary: print help info and exit
    @param : None
    @return: None
    '''
    usage()
    sys.exit(-1)

def parse_options():
    '''
    @summary: get the external afferent parameters
    @param : None
    @return: None
    '''
    rs = {}
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hI:S:O:i:s:o:')

        # -s and -i cannot both exist
        attributes = []
        for opt in opts:
            attributes.append(opt[0])
        if '-s' in attributes and '-i' in attributes:
            logging.error("-s or -i these two options should exist one")
            print_help_exit()

        if (len(opts) < 2):
            print_help_exit()
        else:
            for name, value in opts:
                if name in ("-h"):
                    print_help_exit()
                elif name in ("-i", "-I") or name in ("-S", "-s"):
                    if (value == "" or value == None):
                        logging.error("Please input json file or swagger path")
                    else:
                        if name in ("-i", "-I"):
                            rs['input_path'] = value
                        if name in ("-S", "-s"):
                            rs["swagger_path"] = value
                elif name in ("-O", "-o"):
                    if (value == "" or value == None):
                        logging.error("Please input output testcase file path")
                    else:
                        rs['output_path'] = value
                else:
                    print_help_exit()
    except getopt.GetoptError:
        print_help_exit()
    return rs

def check_json(suite_dict):
    '''
    @summary: set suite json value to default if no key or correct value in suite_dict
    @param suite_dict: parameter under test in json file
    @return: suite_name, mode, num, design, suite
    '''
    default_suite_name = 'DemoSuite' + str(round(time.time()))
    default_mode = 0
    default_num = 1
    default_design = 1
    default_factor_level = {
        "K1": [0, 1],
        "K2": [0, 1],
        "K3": [0, 1]
    }
    if suite_dict.__contains__('SuiteName') or suite_dict['SuiteName'] is not None or suite_dict['SuiteName'] != '':
        suite_name = suite_dict['SuiteName']
    else:
        suite_name = default_suite_name
    if suite_dict.__contains__('Mode') or suite_dict['Mode'] is not None or suite_dict['Mode'] not in [0, 1]:
        mode = suite_dict['Mode']
    else:
        mode = default_mode
    if suite_dict.__contains__('Num') or suite_dict['Num'] is not None or suite_dict['Num'] not in [0, 1]:
        num = suite_dict['Num']
    else:
        num = default_num
    if suite_dict.__contains__('Design') or suite_dict['Design'] is not None or suite_dict['Design'] not in [0, 1]:
        design = suite_dict['Design']
    else:
        design = default_design
    if suite_dict.__contains__('FactorLevel') or suite_dict['FactorLevel'] is not None or suite_dict['FactorLevel'] != {}:
        suite = suite_dict['FactorLevel']
    else:
        suite = default_factor_level
    return suite_name, mode, num, design, suite

if __name__ == '__main__':
    options = parse_options()
    output_path = options['output_path']
    if options.__contains__('input_path'):
        input_path = options['input_path']
        logging.info('The input file is {0}, The output file is {1}'.format(input_path, output_path))
        with open(input_path, 'r') as json_file:
            test_json_body = json.load(json_file)

    if options.__contains__('swagger_path'):
        input_path = options['swagger_path']
        logging.info('The swagger api_docs url is {0}, The output file is {1}'.format(input_path, output_path))
        test_json_body = compose_orthogonal_request_json_from_swagger(input_path)

    oa_test = OrthogonalArrayTest()
    whole_csv_result = []
    for i in test_json_body:
        suite_name, mode, num, design, suite = check_json(i)
        oa_test.orthogonal_array_file = design
        result = oa_test.genSets(suite, design, mode, num)
        logging.info('orthogonal array result for function: {0}'.format(result))
        for j in result:
            whole_csv_result.append([suite_name, json.dumps(j, ensure_ascii=False)])
    # save result into output_path
    swagger_orthogonal_array_csv_writer(output_path, whole_csv_result)
