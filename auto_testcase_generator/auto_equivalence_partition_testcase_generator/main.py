#!/usr/bin/env python3
# encoding: utf-8
'''
Provide the function for auto-generate testcase according to equivalence partition method
Created on Jun 18, 2021
@author: Guangli.bao
@change: on Jul 22, 2021 Guangli.bao: add swagger api_docs function
'''
import getopt
import sys
import json
sys.path.append("..")
from common_tools import utils
from log import logging as logging
import generate_equivalence_partition
from common_tools.get_swagger_api_docs import get_swagger_api_docs

def usage():
    '''
    @summary: usage info
    @param : None
    @return: None
    '''
    print("""
    The usage this equivalence partition testcase automotive generation tool:
    -i input filepath e.g. -i /Users/user/test.json
    -s swagger url e.g. -s http://127.0.0.1:8080/v2/api-docs
    -o output testcase file: csv format  e.g. -o /Users/user/test.csv
    Note: -i or -s should choose one from these two options
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

def generate_tc(tested_parameters):
    # whole_result_for_function is for API
    whole_result_for_function = {}

    # csv_content is for csv testcase Title
    whole_csv_content = {}
    # run the equivalence partition tc generator
    for para in tested_parameters:
        if not para.__contains__('parameterType'):
            logging.error("No parameterType in parameter: {}".format(json.dumps(para)))
            raise RuntimeError("No parameterType in parameter: {}".format(json.dumps(para)))
        elif para['parameterType'] == 'VARCHAR2':
            result_for_function, result_for_testcase \
                = generate_equivalence_partition.generate_varchar_equivalence_partition(para)
        elif para['parameterType'] == 'number':
            result_for_function, result_for_testcase \
                = generate_equivalence_partition.generate_number_equivalence_partition(para)
        elif para['parameterType'] == 'date':
            result_for_function, result_for_testcase \
                = generate_equivalence_partition.generate_date_equivalence_partition(para)
        elif para['parameterType'] == 'enum':
            result_for_function, result_for_testcase \
                = generate_equivalence_partition.generate_enum_equivalence_partition(para)
        elif para['parameterType'] == 'file':
            result_for_function, result_for_testcase \
                = generate_equivalence_partition.generate_file_equivalence_partition(para)
        else:
            pass
        if para.__contains__('path'):
            for k, v in result_for_testcase.items():
                result_for_testcase[k]['path'] = para['path']
        whole_result_for_function.update(result_for_function)
        whole_csv_content.update(result_for_testcase)
    logging.info('testcases for function: ')
    logging.info(json.dumps(whole_result_for_function, indent=2, ensure_ascii=False))
    logging.info('testcases for csv file: ')
    logging.info(json.dumps(whole_csv_content, indent=2, ensure_ascii=False))
    return whole_result_for_function, whole_csv_content

if __name__ == '__main__':
    options = parse_options()
    output_path = options['output_path']
    if options.__contains__('input_path'):
        input_path = options['input_path']
        logging.info('The input file is {0}, The output file is {1}'.format(input_path, output_path))

        # check file exist and file content correctness
        tested_parameters = utils.check_if_file_exists(input_path)
        whole_result_for_function, whole_csv_content = generate_tc(tested_parameters)
        utils.csv_writer(output_path, whole_csv_content)
    if options.__contains__('swagger_path'):
        input_path = options['swagger_path']
        logging.info('The swagger api_docs url is {0}, The output file is {1}'.format(input_path, output_path))

        # check swagger url is accessed and get swagger api parameters to be tested; swagger path is included
        if utils.check_swagger_url(input_path) == 0:
            tested_parameters = get_swagger_api_docs(input_path)
            whole_result_for_function, whole_csv_content = generate_tc(tested_parameters)
            utils.swagger_csv_writer(output_path, whole_csv_content)

