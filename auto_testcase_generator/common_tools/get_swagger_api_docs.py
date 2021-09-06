#!/usr/bin/env python3
# encoding: utf-8
'''
Get api parameters from swagger api_docs
Created on Jul 22, 2021
@author: Guangli.bao
'''
import requests
import json
import os
from log import logger as logging
import urllib3
import certifi
DEFAULT_VALUES = {}

# PARAMETER_BLACK_LIST is one list to exclude parameters that don't need testcases
PARAMETER_BLACK_LIST = ['token']

def get_api_response(url):
    '''
    @summary: get api response content from swagger url
    @param url: swagger api_docs url
    @return: api version
    '''
    #response = requests.get(url)
    # if response.status_code != 200:
    #     raise Exception("swagger url: {0} return {1}".format(url, response.status_code))
    # else:
    #     resp = json.loads(response.text)
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    response = http.request('GET', url)
    if response.status != 200:
        raise Exception("swagger url: {0} return {1}".format(url, response.status_code))
    else:
        resp = json.loads(response.data.decode('utf-8'))
    return resp

def getSwagger(response):
    '''
    @summary: get swagger parameters from swagger api_docs
    @param url: api_docs url
    @return: api parameters and model
    '''
    response_result_dict = response
    try:
        response_paths_dict = response_result_dict['paths']
        api_dict = {}
        for k, v in response_paths_dict.items():
            api_dict[k] = {}
            for kk, vv in v.items():
                if not vv.__contains__('deprecated') or vv.__contains__('deprecated') is False:
                    if vv.__contains__('parameters'):
                        api_dict[k][kk] = {'parameters': vv['parameters'], 'responses': vv['responses']}
                    if vv.__contains__('consumes'):
                        api_dict[k][kk]['consumes'] = vv['consumes']
    except Exception:
        logging.error('No paths that include parameters in swagger API definition')
    model_dict = {}
    if response_result_dict.__contains__('definitions'):
        model_dict = {'definitions': response_result_dict['definitions']}
    return api_dict, model_dict

def read_default_value_setting():
    '''
    @summary: get equivalence partition default condition value from json in the same directory
    @param params: None
    @return: values
    '''
    global DEFAULT_VALUES
    if os.path.dirname(__file__) == '':
        default_value_file = './default_value_setting.json'
    else:
        default_value_file = os.path.dirname(__file__) + '/default_value_setting.json'
    if os.path.exists(default_value_file):
        with open(default_value_file, 'r') as jf:
            DEFAULT_VALUES = json.load(jf)

def set_default_value(temp_dict, parameterType):
    '''
    @summary: fill into equivalence partition default values based on different type
    @param temp_dict: parameter dict
    @param parameterType: parameter type
    @return: new parameter dict
    '''
    temp_dict.update(DEFAULT_VALUES[parameterType])
    return temp_dict

def compose_dict(swagger_parameter, temp_dict):
    '''
    @summary: transform swagger api parameter to equivalence partition parameters format
    @param swagger_parameter: parameter
    @param temp_dict: origin parameter dict
    @return: new parameter dict
    '''
    if swagger_parameter.__contains__('type'):
        type = swagger_parameter['type']
    else:
        type = ''
    if swagger_parameter.__contains__('format'):
        format = swagger_parameter['format']
    else:
        format = ''
    if type == 'string':
        if swagger_parameter.__contains__('enum'):
            temp_dict['parameterType'] = 'enum'
            set_default_value(temp_dict, 'enum')
            temp_dict['parameterRange'] = swagger_parameter['enum']
        elif format.__contains__('date'):
            temp_dict['parameterType'] = 'date'
            set_default_value(temp_dict, 'date')
        else:
            temp_dict['parameterType'] = 'VARCHAR2'
            set_default_value(temp_dict, 'VARCHAR2')
    elif type == 'integer' or type == 'number':
        temp_dict['parameterType'] = 'number'
        set_default_value(temp_dict, 'number')
        if format.__contains__('float') or format.__contains__('double'):
            origin_range = temp_dict['parameterRange']
            temp_dict['parameterRange'] = '[' + str(float(origin_range.split(',')[0][-1])) + ', ' + \
                                          str(float(origin_range.split(',')[1].strip()[0])) + ']'
    elif type == 'file':
        temp_dict['parameterType'] = 'file'
        set_default_value(temp_dict, 'file')
    else:
        # array type
        temp_dict['parameterType'] = type
    if swagger_parameter.__contains__('required'):
        temp_dict['ifNull'] = swagger_parameter['required']
    return temp_dict

def get_schema(path, parameter_name, schema_value, model_dict, temp_request_parameter_list):
    '''
    @summary: if one parameter is object or object nested object, the parameter's schema should be analyse
    @param schema_value: parameter's schema, such as: {"schema":{"$ref":"#/definitions/FilterConditionValue"}}
    @param model_dict: swagger model
    @return temp_request_parameter_list: parameter list for equivalence partition
    '''
    model_name = schema_value.split('/')[-1]
    model_properties = model_dict['definitions'][model_name]['properties']
    model_properties_keys = model_properties.keys()
    for j in model_properties_keys:
        property_name = j
        temp_dict = {}
        if model_dict['definitions'][model_name]['properties'][j].__contains__('$ref'):
            get_schema(path, parameter_name, \
                                            model_dict['definitions'][model_name]['properties'][j]['$ref'], model_dict,
                                                temp_request_parameter_list)
        elif model_dict['definitions'][model_name]['properties'][j].__contains__('type'):
            temp_dict['parameterName'] = path + '_' + parameter_name + '_' + model_name + '_' + property_name
            temp_dict['path'] = path
            temp_dict = compose_dict(model_dict['definitions'][model_name]['properties'][j], temp_dict)
            temp_request_parameter_list.append(temp_dict)
        else:
            pass
    return temp_request_parameter_list

def transform2json(api_dict, model_dict):
    '''
    @summary: transform the whole swagger api parameters to equivalence partition parameters json
    @param api_dict: origin api parameters
    @param model_dict: origin model dict
    @return: equivalence partition parameters json
    '''
    request_parameter_list = []
    for k, v in api_dict.items():
        for kk, vv in v.items():
            if len(vv['parameters']) != 0:
                for i in vv['parameters']:
                    temp_dict = {}
                    path = k
                    parameter_name = i['name']
                    if i.__contains__('type'):
                        temp_dict['parameterName'] = path + '_' + parameter_name
                        temp_dict['path'] = path
                        temp_dict = compose_dict(i, temp_dict)
                        request_parameter_list.append(temp_dict)
                    if i.__contains__('schema'):
                        temp_request_parameter_list = []
                        if i['schema'].__contains__('$ref'):
                            temp_request_parameter_list = get_schema(path, parameter_name, i['schema']['$ref'], model_dict, \
                                                                 temp_request_parameter_list)
                            request_parameter_list += temp_request_parameter_list
                        else:
                            # array type is pending
                            pass
                    else:
                        pass
            else:
                pass
    logger.info('equivalence partition parameters json: {}'.format(json.dumps(request_parameter_list)))
    return request_parameter_list

def get_swagger_api_docs(swagger_url):
    '''
    @summary: function that get api parameters from swagger api_docs then transform them to equivalence partition json
    @param swagger_url: swagger api_docs url
    @return: equivalence partition parameters json
    '''
    api_response = get_api_response(swagger_url)
    api_dict, model_dict = getSwagger(api_response)
    read_default_value_setting()
    request_parameter_list = transform2json(api_dict, model_dict)
    return request_parameter_list

def get_schema_for_orthogonal(model_name, model_dict, model_parameters):
    '''
    @summary: if one parameter is object or object nested object, the parameter's schema should be analyse
    @param model_name: model name such as: Product object name
    @param model_dict: swagger model
    @param model_parameters: swagger model parameters empty list
    @return model_parameters: swagger model parameter list for orthogonal array
    '''
    model_properties = model_dict['definitions'][model_name]['properties']
    for j in model_properties.keys():
        if model_properties[j].__contains__('$ref'):
            get_schema_for_orthogonal(model_properties[j]['$ref'].split('/')[-1], \
                                      model_dict, model_parameters)
        elif model_properties[j].__contains__('type') and 'array' != model_properties[j]['type']:
            model_parameters.append(model_name + '_' + j)
        else:
            # array type is pending
            pass
    return model_parameters

def filter_parameters_for_orthogonal(api_dict, model_dict):
    '''
    @summary: filter the parameters to exclude parameter that's in black list; then store api with more than and equal
    to 2 parameters
    @param api_dict: origin api parameters
    @return: parameters to be orthogonal array, [{'SuiteName': '/TestSuites/addStudent', 'FactorLevel': {}}]
    '''
    orthogonal_parameter_list = []
    for k, v in api_dict.items():
        for kk, vv in v.items():
            temp_suite_dict = {}
            temp_suite_dict['SuiteName'] = k
            temp_suite_dict['FactorLevel'] = {}
            for i in vv['parameters']:
                # exclude black_list parameter
                if i['name'] not in PARAMETER_BLACK_LIST:
                    if i.__contains__('type'):
                        temp_suite_dict['FactorLevel'][i['name']] = []
                    if i.__contains__('schema'):
                        model_parameters = []
                        if i['schema'].__contains__('$ref'):
                            model_parameters = get_schema_for_orthogonal(i['schema']['$ref'].split('/')[-1],
                                                                     model_dict, model_parameters)
                        else:
                            # array type is pending
                            pass
                        for params in model_parameters:
                            temp_suite_dict['FactorLevel'][params] = []
            orthogonal_parameter_list.append(temp_suite_dict)

    # filter FactorLevel to remove less than 2 parameters
    new_orthogonal_parameter_list = []
    for param in orthogonal_parameter_list:
        if len(param['FactorLevel'].keys()) >= 2:
            new_orthogonal_parameter_list.append(param)
    return new_orthogonal_parameter_list

def set_orthogonal_array_default_value(parameters):
    '''
    @summary: fill into default value for orthogonal request parameters
    @param parameters: origin testsuite with parameters
    @return: testsuite with parameters and values
    '''
    for i in parameters:
        i['Mode'] = 0
        i['Num'] = 0
        i['Design'] = 1
        for key, value in i['FactorLevel'].items():
            i['FactorLevel'][key] = [None, '有效值', '无效值']
    return parameters

def compose_orthogonal_request_json_from_swagger(swagger_url):
    '''
    @summary: function that get api parameters from swagger api_docs then transform them to orthogonal arrays json
    Condition: one api is one test suite, and api parameters >=2
    @param swagger_url: swagger api_docs url
    @return: orthogonal arrays json
    '''
    api_response = get_api_response(swagger_url)
    api_dict, model_dict = getSwagger(api_response)
    orthogonal_parameters = filter_parameters_for_orthogonal(api_dict, model_dict)
    orthogonal_parameters = set_orthogonal_array_default_value(orthogonal_parameters)
    return orthogonal_parameters

'''
#for self debug
if __name__ == '__main__':
    swagger_url = 'http://127.0.0.1:8080/v2/api-docs'
    api_dict, model_dict = get_swagger_api_docs(swagger_url)
    read_default_value_setting()
    transform2json(api_dict, model_dict)
'''




