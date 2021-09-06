#!/usr/bin/env python3
# encoding: utf-8

import requests as requests
import json
import pytest
import pytest_check as check


@pytest.mark.parametrize('username', ['lLnv', 'LlNV', 'RHOybGqxvT.', 'UsdErjiTWcwkDoZuPBxb', 'a', ])
def test_get_username_valid(username): 
	url = 'http://petstore.swagger.io/v2/user/' + username
	resp = requests.get(url=url)
	msg = 'request url: ' + url + ', get ' + 'request return: ' + json.dumps(resp.text)
	check.equal(resp.status_code, 200, msg) 

@pytest.mark.parametrize('username', ['十一二五', '/7@', 'IHhUAFpmXtuinladLYgcE', '', 'None', 'Null', ])
def test_get_username_invalid(username): 
	url = 'http://petstore.swagger.io/v2/user/' + username
	resp = requests.get(url=url)
	msg = 'request url: ' + url + ', get ' + 'request return: ' + json.dumps(resp.text)
	check.equal(resp.status_code, 400, msg) 

