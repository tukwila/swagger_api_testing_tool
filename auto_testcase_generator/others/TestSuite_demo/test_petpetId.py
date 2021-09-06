#!/usr/bin/env python3
# encoding: utf-8

import requests as requests
import json
import pytest
import pytest_check as check
import unittest
from parameterized import parameterized
from HTMLTestRunner import HTMLTestRunner

class Test_test(unittest.TestCase):

	#@pytest.mark.parametrize('petId', ['2456031811345596463', '9223372036854775807', '-9223372036854775807', '9223372036854775808', '-9223372036854775808', ])
	#@parameterized.expand([("2456031811345596463")])
	@parameterized.expand(['2456031811345596463', '9223372036854775807', '-9223372036854775807', '9223372036854775808', '-9223372036854775808', ])
	def test_get_petId_valid(self, petId):
		url = 'http://petstore.swagger.io/v2/pet/' + petId
		resp = requests.get(url=url)
		msg = 'request url: ' + url + ', get ' + 'request return: ' + json.dumps(resp.text)
		check.equal(resp.status_code, 200, msg)

	#@pytest.mark.parametrize('petId', ['9223372036854775809', '-9223372036854775809', 'None', 'Null', ])
	# @parameterized.expand([('9223372036854775809'), ('-9223372036854775809'), ('None'), ('Null'), ])
	# def test_get_petId_invalid(self, petId):
	# 	url = 'http://petstore.swagger.io/v2/pet/' + petId
	# 	resp = requests.get(url=url)
	# 	msg = 'request url: ' + url + ', get ' + 'request return: ' + json.dumps(resp.text)
	# 	check.equal(resp.status_code, 400, msg)


if __name__ == '__main__':
    #unittest.main(verbosity=2)
	# suit = unittest.defaultTestLoader.discover('./', pattern='test_petpetId.py')
	# runner = unittest.TextTestRunner(verbosity=2)
	# runner.run(suit)
	suit = unittest.defaultTestLoader.discover('/', pattern='test_petpetId.py')
	report_dirc = "/Report"
	report_name = "./unitest_report.html"
	with open(report_name, 'wb') as fp:
		runner = HTMLTestRunner(stream=fp, verbosity=2, title="test html report", description="test")
		runner.run(suit)
