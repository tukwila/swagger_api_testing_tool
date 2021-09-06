#!/usr/bin/env python3
# encoding: utf-8
'''
Provide the class for auto-generate testcase according to orthogonal arrays method in taguchi design
Created on Jul 13, 2021
@author: Guangli.bao
'''
from itertools import groupby
from collections import OrderedDict
import sys
import os
sys.path.append("..")
from common_tools.utils import read_orthogonal_array_file

def dataSplit(data):
    '''
    @summary: reorganize orthogonal array from string list to int list
    @param data: original orthogonal array
    @return: orthogonal array
    '''
    ds = []
    mb = [sum([k for m, k in data['mk'] if m <= 10]), sum([k for m, k in data['mk'] if m > 10])]
    for i in data['data']:
        if mb[1] == 0:
            ds.append([int(d) for d in i])
        elif mb[0] == 0:
            ds.append([int(i[n * 2:(n + 1) * 2]) for n in range(mb[1])])
        else:
            part_1 = [int(j) for j in i[:mb[0]]]
            part_2 = [int(i[mb[0]:][n * 2:(n + 1) * 2]) for n in range(mb[1])]
            ds.append(part_1 + part_2)
    return ds

class OrthogonalArrayTest(object):
    def __init__(self):
        self._orthogonal_array_file = os.path.split(os.path.realpath(__file__))[0]
        self.data = OrderedDict()

    @property
    def orthogonal_array_file(self):
        '''
        @summary: self._orthogonal_array_file getter
        @param: none
        @return: self._orthogonal_array_file
        '''
        return self._orthogonal_array_file

    @orthogonal_array_file.setter
    def orthogonal_array_file(self, design_value):
        '''
        @summary: self._orthogonal_array_file setter
        @param design_value: design mode value
        @return: none
        '''
        if design_value == 0:
            self._orthogonal_array_file = os.path.split(os.path.realpath(__file__))[0] + '/taguchi_designs.txt'
        elif design_value == 1:
            self._orthogonal_array_file = os.path.split(os.path.realpath(__file__))[0] + '/ts723_Designs.txt'
        else:
            logging.error("Design value should be 0(taguchi) or 1(ts723)")
        self.data = read_orthogonal_array_file(self._orthogonal_array_file)

    def get(self, mk):
        '''
        @summary: get the orthogonal array based on m, k; calculation formula is as following:
                m=max(m1,m2,m3,…)
                k=(k1+k2+k3+…)
                n=k1*(m1-1)+k2*(m2-1)+…kx*x-1)+1
                n means testing times
                and chose one orthogonal array which m,k is most close to the request
        @param mk: m is levels, k is factors; mk is levels and factors list such as: [(2,3)],[(5,5),(2,1)]
        @return: original orthogonal array
        '''
        mk = sorted(mk, key=lambda i: i[0])
        m = max([i[0] for i in mk])
        k = sum([i[1] for i in mk])
        n = sum([i[1] * (i[0] - 1) for i in mk]) + 1
        query_key = ' '.join(['^'.join([str(j) for j in i]) for i in mk])
        for data in self.data:
            # firstly query if fully matched orthogonal array
            if query_key in data[0]:
                return dataSplit(data[1])
            # if no fully matched one, get the most close array >= m,k,n
            elif data[1]['n'] >= n and data[1]['mk'][0][0] >= m and data[1]['mk'][0][1] >= k:
                return dataSplit(data[1])
        # if no any matched, return none
        return None

    def genSets(self, params, design, mode=0, num=1):
        '''
        @summary: generate orthogonal array based on request dict and design mode and mode and num
        @param params: parameters under test
        @param design: design mode such as taguchi or ts272
        @param mode: loose mode or strict mode
        @param num: null count
        @return: testing result set
        '''
        sets = []
        mk = [(k, len(list(v)))for k, v in groupby(params.items(), key=lambda x:len(x[1]))]
        data = self.get(mk)
        for d in data:
            # generate testing result set based on orthogonal array
            q = OrderedDict()
            for index, (k, v) in zip(d, params.items()):
                try:
                    if design == 0:
                        q[k] = v[index-1]
                    if design == 1:
                        q[k] = v[index]
                except IndexError:
                    # if parameter under test are out of array scope, set it to None
                    q[k] = None
            if q not in sets:
                if mode == 0:
                    sets.append(q)
                elif mode == 1 and (len(list(filter(lambda v: v is None, q.values())))) <= num:
                    # tail testing result in strict mode set based on num value to remove null
                    sets.append(q)
        return sets
