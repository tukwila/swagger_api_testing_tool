#!/usr/bin/env python3
# encoding: utf-8
'''
Generate equivalence partition: valid part/invalid part
Created on Jul 01, 2021
@author: Guangli.bao
'''
from auto_equivalence_partition_testcase_generator import equivalence_partition_testing_data, testcase_in_csv
from log import logging as logging

def generate_varchar_equivalence_partition(parameter):
    '''
    @summary: generate equivalence partition dict based on varchar2 type
    @param parameter: tested varchar2 parameter
    @return: equivalence partition dict
    '''
    varchar2_equivalence_partition_basic = {
        parameter['parameterName']: {
            'valid_equivalence_partition': {'parameterRange_validChar': None, 'ifNull': None, 'caseSensitive': None},
            'invalid_equivalence_partition': {'parameterRange_validChar': None, 'ifNull': None, 'caseSensitive': None}
        }
    }
    varchar2_equivalence_partition_testing_data_for_function = {}
    varchar2_equivalence_partition_testing_data_for_testcase = {}
    if len(parameter['parameterRange']) != 0 and parameter['ifNull'] is not None and parameter['ifNull'] != '' \
            and len(parameter['validChar']) != 0 and parameter['caseSensitive'] is not None \
            and parameter['caseSensitive'] != '':
        varchar2_equivalence_partition_basic, varchar2_equivalence_partition_testing_data_for_function = \
            equivalence_partition_testing_data.generate_varchar_testing_data(parameter,
                                                                             varchar2_equivalence_partition_basic)
    else:
        logging.error("Tested parameter json value is not correct")
        raise Exception('Tested parameter json value is not correct')
    varchar2_equivalence_partition_testing_data_for_testcase = \
        testcase_in_csv.testcase_varchar_content(parameter, varchar2_equivalence_partition_basic)
    return varchar2_equivalence_partition_testing_data_for_function, varchar2_equivalence_partition_testing_data_for_testcase

def generate_number_equivalence_partition(parameter):
    '''
    @summary: generate equivalence partition dict based on number type
    @param parameter: tested number parameter
    @return: equivalence partition dict
    '''
    number_equivalence_partition_basic = {
        parameter['parameterName']: {
            'valid_equivalence_partition': {'parameterRange': None, 'ifNull': None},
            'invalid_equivalence_partition': {'parameterRange': None, 'ifNull': None}
        }
    }
    number_equivalence_partition_testing_data_for_function = {}
    number_equivalence_partition_testing_data_for_testcase = {}
    if len(parameter['parameterRange']) != 0 and parameter['ifNull'] is not None and parameter['ifNull'] != '':
        number_equivalence_partition_basic, number_equivalence_partition_testing_data_for_function = \
            equivalence_partition_testing_data.generate_number_testing_data(parameter,
                                                                            number_equivalence_partition_basic)
    else:
        logging.error("Tested parameter json value is not correct")
        raise Exception('Tested parameter json value is not correct')
    number_equivalence_partition_testing_data_for_testcase = \
        testcase_in_csv.testcase_number_content(parameter, number_equivalence_partition_basic)
    return number_equivalence_partition_testing_data_for_function, number_equivalence_partition_testing_data_for_testcase

def generate_date_equivalence_partition(parameter):
    '''
    @summary: generate equivalence partition dict based on date type
    @param parameter: tested number parameter
    @return: equivalence partition dict
    '''
    date_equivalence_partition_basic = {
        parameter['parameterName']: {
            'valid_equivalence_partition': {'parameterRange': None, 'ifNull': None},
            'invalid_equivalence_partition': {'parameterRange': None, 'ifNull': None}
        }
    }
    date_equivalence_partition_testing_data_for_function = {}
    date_equivalence_partition_testing_data_for_testcase = {}
    if len(parameter['parameterRange']) != 0 and parameter['ifNull'] is not None and parameter['ifNull'] != '':
        date_equivalence_partition_basic, date_equivalence_partition_testing_data_for_function = \
            equivalence_partition_testing_data.generate_date_testing_data(parameter,
                                                                          date_equivalence_partition_basic)
    else:
        logging.error('Tested parameter json value is not correct')
        raise Exception('Tested parameter json value is not correct')
    date_equivalence_partition_testing_data_for_testcase = \
        testcase_in_csv.testcase_date_content(parameter, date_equivalence_partition_basic)
    return date_equivalence_partition_testing_data_for_function, date_equivalence_partition_testing_data_for_testcase

def generate_datetime_equivalence_partition(parameter):
    '''
    @summary: generate equivalence partition dict based on dateTime type
    @param parameter: tested number parameter
    @return: equivalence partition dict
    '''
    datetime_equivalence_partition_basic = {
        parameter['parameterName']: {
            'valid_equivalence_partition': {'parameterRange': None, 'ifNull': None},
            'invalid_equivalence_partition': {'parameterRange': None, 'ifNull': None}
        }
    }
    datetime_equivalence_partition_testing_data_for_function = {}
    datetime_equivalence_partition_testing_data_for_testcase = {}
    if parameter['ifNull'] is not None and parameter['ifNull'] != '':
        datetime_equivalence_partition_basic, datetime_equivalence_partition_testing_data_for_function = \
            equivalence_partition_testing_data.generate_datetime_testing_data(parameter,
                                                                          datetime_equivalence_partition_basic)
    date_equivalence_partition_testing_data_for_testcase = \
        testcase_in_csv.testcase_datetime_content(parameter, datetime_equivalence_partition_basic)
    return datetime_equivalence_partition_testing_data_for_function, datetime_equivalence_partition_testing_data_for_testcase

def generate_enum_equivalence_partition(parameter):
    '''
    @summary: generate equivalence partition dict based on enum type
    @param parameter: tested number parameter
    @return: equivalence partition dict
    '''
    enum_equivalence_partition_basic = {
        parameter['parameterName']: {
            'valid_equivalence_partition': {'parameterRange': None, 'ifNull': None},
            'invalid_equivalence_partition': {'parameterRange': None, 'ifNull': None, 'caseSensitive': None}
        }
    }
    date_equivalence_partition_testing_data_for_function = {}
    date_equivalence_partition_testing_data_for_testcase = {}
    if len(parameter['parameterRange']) != 0 and parameter['ifNull'] is not None and parameter['ifNull'] != '' and \
            parameter['caseSensitive'] is not None and parameter['caseSensitive'] != '':
        enum_equivalence_partition_basic, enum_equivalence_partition_testing_data_for_function = \
            equivalence_partition_testing_data.generate_enum_testing_data(parameter,
                                                                          enum_equivalence_partition_basic)
    else:
        logging.error('Tested parameter json value is not correct')
        raise Exception('Tested parameter json value is not correct')
    enum_equivalence_partition_testing_data_for_testcase = \
        testcase_in_csv.testcase_enum_content(parameter, enum_equivalence_partition_basic)
    return enum_equivalence_partition_testing_data_for_function, enum_equivalence_partition_testing_data_for_testcase

def generate_file_equivalence_partition(parameter):
    '''
    @summary: generate equivalence partition dict based on file type
    @param parameter: tested number parameter
    @return: equivalence partition dict
    '''
    file_equivalence_partition_basic = {
        parameter['parameterName']: {
            'valid_equivalence_partition': {'parameterRange': None, 'ifNull': None},
            'invalid_equivalence_partition': {'parameterRange': None, 'ifNull': None}
        }
    }
    file_equivalence_partition_testing_data_for_function = {}
    file_equivalence_partition_testing_data_for_testcase = {}
    if len(parameter['parameterRange']) != 0 and parameter['ifNull'] is not None and parameter['ifNull'] != '':
        file_equivalence_partition_basic, file_equivalence_partition_testing_data_for_function = \
            equivalence_partition_testing_data.generate_file_testing_data(parameter,
                                                                          file_equivalence_partition_basic)
    else:
        logging.error('Tested parameter json value is not correct')
        raise Exception('Tested parameter json value is not correct')
    file_equivalence_partition_testing_data_for_testcase = \
        testcase_in_csv.testcase_file_content(parameter, file_equivalence_partition_basic)
    return file_equivalence_partition_testing_data_for_function, file_equivalence_partition_testing_data_for_testcase

def generate_boolean_equivalence_partition(parameter):
    '''
    @summary: generate equivalence partition dict based on file type
    @param parameter: tested number parameter
    @return: equivalence partition dict
    '''
    boolean_equivalence_partition_basic = {
        parameter['parameterName']: {
            'valid_equivalence_partition': {'parameterRange': None, 'ifNull': None},
            'invalid_equivalence_partition': {'parameterRange': None, 'ifNull': None}
        }
    }
    boolean_equivalence_partition_testing_data_for_function = {}
    boolean_equivalence_partition_testing_data_for_testcase = {}
    if parameter['ifNull'] is not None and parameter['ifNull'] != '':
        boolean_equivalence_partition_basic, boolean_equivalence_partition_testing_data_for_function = \
            equivalence_partition_testing_data.generate_boolean_testing_data(parameter,
                                                                          boolean_equivalence_partition_basic)
    boolean_equivalence_partition_testing_data_for_testcase = \
        testcase_in_csv.testcase_enum_content(parameter,  boolean_equivalence_partition_basic)
    return  boolean_equivalence_partition_testing_data_for_function,  boolean_equivalence_partition_testing_data_for_testcase