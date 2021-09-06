#!/usr/bin/env python3
# encoding: utf-8

'''
Define a logging object which will be quoted by other files
Created on Sep 01, 2021
@author: Guangli.bao
'''
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='auto_equivalence_partition.log',
                    filemode='w')
logger = logging.getLogger('')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
