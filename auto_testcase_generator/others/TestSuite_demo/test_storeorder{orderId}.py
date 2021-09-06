#!/usr/bin/env python3
# encoding: utf-8

import requests as requests
import json
import pytest
import pytest_check as check
from robot.api import TestSuite
from robot.api import ResultWriter

class SwaggerTest:
	def __init__(self, name):
		self.suite = TestSuite(name)
	#@pytest.mark.parametrize('orderId', ['6', '9', '2', '10', '1', ])
	def test_get_orderId_valid(self):
		test_01 = self.suite.tests.create('valid test')
		url = 'http://petstore.swagger.io/v2/store/order/' + '6'
		resp = requests.get(url=url)
		msg = 'request url: ' + url + ', get ' + 'request return: ' + json.dumps(resp.text)
		check.equal(resp.status_code, 200, msg)

	#@pytest.mark.parametrize('orderId', ['11', '0', 'None', 'Null', ])
	def test_get_orderId_invalid(self):
		test_02 = self.suite.tests.create('invalid test')
		url = 'http://petstore.swagger.io/v2/store/order/' + '11'
		resp = requests.get(url=url)
		msg = 'request url: ' + url + ', get ' + 'request return: ' + json.dumps(resp.text)
		check.equal(resp.status_code, 400, msg)

	def run(self):
		self.test_get_orderId_valid()
		self.test_get_orderId_invalid()
		result = self.suite.run(critical = "RF test", output = "output.xml")
		ResultWriter(result).write_results(report = "RFreport.html", log="log.html")

if __name__ == "__main__":
	suite = SwaggerTest("RF swagger testing")
	suite.run()
