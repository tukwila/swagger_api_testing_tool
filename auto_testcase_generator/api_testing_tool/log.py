#!/usr/bin/env python3
# encoding: utf-8

'''
Define a logging object which will be quoted by other files
Created on Jul 01, 2021
@author: Guangli.bao
'''
import logging
from datetime import datetime
import os

if not os.path.exists(os.getcwd() + '/TestResult'):
    os.makedirs(os.getcwd() + '/TestResult')

timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='./TestResult/api_testing_tool.log',
                    filemode='w')
logger = logging.getLogger('')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
