#!/usr/bin/env python3
# encoding: utf-8

'''
Define a logging object which will be quoted by other files
Created on Jul 01, 2021
@author: Guangli.bao
'''
import os
import logging

def create_log(log_file_name):
    '''
    @summary: create log file and record log content
    @param log_file_name: log file path and name
    @return logger: logging instance
    '''
    logger = logging.getLogger('')
    if logger is not None:
        for handler in logger.handlers[:]:
            handler.stream.close()
            logger.removeHandler(handler)
    if os.path.exists(log_file_name):
        os.remove(log_file_name)
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=log_file_name,
                        filemode='w')
    return logger
