#!/usr/bin/env python3
# encoding: utf-8
'''
The tool to generate testcases based on swagger API 2.0 or 3.0 then execute these testcases
Created on Aug 2, 2021
@author: Guangli.bao
'''
import getopt
import parse_openAPI
from generate_api_testcase import *
from generate_testcase_script import *
from testcase_execution_engine import *
from generate_html_report import *
from utility import create_folder
from log import logger as logging
from datetime import datetime

def usage():
    '''
    @summary: usage info
    @param : None
    @return: None
    '''
    print("""
    The usage of this swagger api testing tool: to generate testcase based one swagger APi 2.0 or 3.0 then execute them
    -i input filepath e.g. -i /Users/user/test.json
    -s swagger api-docs url e.g. -s https://petstore.swagger.io/v2/swagger.json
    -o output testcase csv file((default: testcases.csv) e.g. -o /Users/user/test.csv
    -r do api testing and save test result report e.g. -e ./test.html
    -e only do api testing based on existed automation testcase scripts such as in TestSuites folder
    e.g. 
    1. to analyze local api json file and to generate testcase then save them into local file
    python3 main.py -i /Users/user/test.json -o /Users/user/test.csv
    2. to test swagger api then save testcases result the current path: ./test.html
    python3 main.py -s https://petstore.swagger.io/v2/swagger.json -o /Users/user/test.csv -r ./test.html
    3. only execute test scripts to test swagger api
    python3 main.py -s https://petstore.swagger.io/v2/swagger.json -e ./TestSuits -r ./test.html
    3.1. if no -r provided in only execution scenario, html report will default save to ./SwaggerAPI_testing_resport.html
    python3 main.py -s https://petstore.swagger.io/v2/swagger.json -e ./TestSuits
    3.2. if no -e value provided in only execution scenario, in current folder ./TestSuites will be scan for testing scripts
    python3 main.py -s https://petstore.swagger.io/v2/swagger.json -e
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
        opts, args = getopt.getopt(sys.argv[1:], 'hS:I:O:R:E:s:i:o:r:e')
        # -s and -f cannot exist together
        if opts.__contains__('-S') and opts.__contains__('-I') or opts.__contains__('-s') and opts.__contains__('-i'):
            logging.error("-s and -i cannot exist together; and -s swagger address is adopted")
        if (len(opts) < 2):
            print_help_exit()
        else:
            if not opts.__contains__('-O') or not opts.__contains__('-o'):
                rs['output_path'] = './TestResult/testcases.csv'
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
                        rs['output_path'] = './TestResult/testcases.csv'
                    else:
                        rs['output_path'] = value
                elif name in ("-r", "-R"):
                    if (value == "" or value == None):
                        logging.error("Please input testcase report result file path")
                    else:
                        rs['report'] = value
                elif name in ("-e", "-E"):
                    if (value == "" or value == None):
                        rs['execution'] = os.getcwd() + '/TestSuites'
                        logging.info("Only execute test suites in: {0}".format(rs['execution']))
                    else:
                        rs['execution'] = value
                else:
                    print_help_exit()
    except getopt.GetoptError:
        print_help_exit()
    return rs

def test_swagger_api(options):
    '''
    @summary: the main process of this tool
    @param options: python command arguments
    @return: None
    '''
    output_path = options['output_path']
    if options.__contains__('report'):
        report = options['report']
    else:
        report = None
    if options.__contains__('input_path'):
        input_path = options['input_path']
        logging.info('The input file is {0}, the output testcase csv file is {1}, the html report file is {2}'.format(
                                                                                    input_path, output_path, report))
        # todo: read json or yaml file to check 2.0 or 3.0 spec version then extract API object(path, parameters, response)
    if options.__contains__('swagger_path'):
        input_path = options['swagger_path']
        logging.info('The swagger api_docs url is {0}, the output testcase csv file is {1}, the html report file is '
                                                                        '{2}'.format(input_path, output_path, report))
        logging.info('request swagger url: {0} to get all api-docs content'.format(input_path))
        try:
            api_respnose = parse_openAPI.get_api_response(input_path)
        except Exception as e:
            logging.error('swagger url: {0} access fail, exception info: {1}'.format(input_path, repr(e)))
            raise e
        api_version = parse_openAPI.get_api_version(api_respnose)
        logging.info('swagger api version: {0}'.format(api_version))
        api_objects, model_definitions = parse_openAPI.extract_api_object(api_respnose, api_version)
        with open('api3_object.json', 'w') as jf:
            jf.write(json.dumps(api_objects, indent=2))
    if report is not None:
        logging.info('generate equivalence partition testcases based on api parameters in output testcase csv file {0}'.format(output_path))
        generate_equivalence_testcase(api_objects, model_definitions, output_path, api_version)
        swagger_base_url = parse_openAPI.get_swagger_url(api_respnose, api_version)
        logging.info('swagger api url: {0}'.format(swagger_base_url))
        logging.info('generate api testing scripts for testing report in folder: ./TestSuites')
        generate_auto_case_file(api_objects)
        logging.info('scan all test scripts in ./TestSuites then do testing swagger api with testing data')
        logging.info('generate testing result html report: {0}'.format(report))
        all_testcase_requests = execute_testcase(swagger_base_url, './TestSuites')
        generate_html(report, float(api_version), swagger_base_url, all_testcase_requests)

def execute_testing_suites(options):
    if options.__contains__('swagger_path'):
        input_path = options['swagger_path']
    else:
        logging.error('No swagger api url to be tested provided')
    if options.__contains__('report'):
        report = options['report']
    else:
        report = './TestResult/SwaggerAPI_testing_resport.html'
    test_scripts_path = options['execution']
    api_respnose = parse_openAPI.get_api_response(input_path)
    api_version = parse_openAPI.get_api_version(api_respnose)
    logging.info('swagger api version: {0}'.format(api_version))
    swagger_base_url = parse_openAPI.get_swagger_url(api_respnose)
    logging.info('generate testing result html report: {0}'.format(report))
    all_testcase_requests = execute_testcase(swagger_base_url, test_scripts_path)
    generate_html(report, float(api_version), swagger_base_url, all_testcase_requests)

if __name__ == '__main__':
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info('Execute Swagger API testing now: {}, please wait for a moment: '.format(start_time))
    print('Execute Swagger API testing now: {}, please wait for a moment: '.format(start_time))
    options = parse_options()
    if options.__contains__('execution'):
        execute_testing_suites(options)
    else:
        logging.info('prepare to create folder to save test scripts: ./TestSuites')
        create_folder(os.getcwd() + '/TestSuites')
        test_swagger_api(options)
    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info('Done: {}'.format(end_time))
    print('\nDone!')











