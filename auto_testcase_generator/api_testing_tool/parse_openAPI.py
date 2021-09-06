#!/usr/bin/env python3
# encoding: utf-8
'''
Provide common functions to parse swagger api
Created on Aug 2, 2021
@author: Guangli.bao
'''
import requests
import json
import sys
import random
sys.path.append("..")
from log import logger as logging
from common_tools.get_swagger_api_docs import *

def get_api_version(response):
    '''
    @summary: get api version from swagger api response content
    @param response: response content
    @return: api version
    '''
    if response.__contains__('swagger') and "2.0" in response['swagger']:
        api_version = 2
    elif response.__contains__('openapi') and "3.0" in response['openapi']:
        api_version = 3
    else:
        raise Exception("api version is not 2.0 or 3.0")
    return api_version

def get_swagger_url(response, api_version):
    '''
    @summary: get swagger host and basePath
    @param response: response content
    @return: swagger_base_url
    '''
    if api_version == 2:
        host = response['host']
        basePath = response['basePath']
        schemes = response['schemes']
        #swagger_base_url = random.sample(schemes, 1)[0] + '://' + host + basePath
        swagger_base_url = 'https://' + host + basePath
    if api_version == 3:
        swagger_base_url = response['servers'][0]['url']
    return swagger_base_url

def extract_api_object(response, api_version):
    '''
    @summary: compose api object: path, CRUD, parameters, response
    @param response: response content
    @param api_version: api version: 2 or 3
    @return: api object
    '''
    if api_version == 2:
        api_objects, model_definitions = getSwagger(response)
    else:
        api_objects, model_definitions = extract_api3_object(response)
    return api_objects, model_definitions

def extract_api3_object(response):
    '''
    @summary: get swagger parameters from swagger api_docs
    @param url: api_docs url
    @return: api parameters and schemas
    '''
    response_result_dict = response
    try:
        response_paths_dict = response_result_dict['paths']
        api_dict = {}
        for k, v in response_paths_dict.items():
            api_dict[k] = {}
            for kk, vv in v.items():
                if not vv.__contains__('deprecated') or vv.__contains__('deprecated') is False:
                    api_dict[k][kk] = {}
                    if vv.__contains__('parameters'):
                        api_dict[k][kk]['parameters'] = vv['parameters']
                    if vv.__contains__('requestBody'):
                        api_dict[k][kk]['requestBody'] = vv['requestBody']
                    if vv.__contains__('responses'):
                        api_dict[k][kk]['responses'] = vv['responses']
                    else:
                        pass
    except Exception:
        logging.error('No paths that include parameters in swagger API definition')
    model_dict = {}
    if response.__contains__('components'):
        model_dict = {'definitions': response_result_dict['components']['schemas']}
    return api_dict, model_dict

def check_api_file_format(file):
    '''
    @summary: check if api file is json or yaml format
    @param file: api file
    @return: file format: json, yaml
    '''
    #todo



