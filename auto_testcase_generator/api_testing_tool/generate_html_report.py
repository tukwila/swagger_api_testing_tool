#!/usr/bin/env python3
# encoding: utf-8
'''
generate html testing report
Created on Aug 18, 2021
@author: Guangli.bao
'''
from HTMLTable import HTMLTable
import os
import re

def generate_result_table(all_testcase_requests):
    title = ['TestSuite', 'Total', 'Pass', 'Fail']
    table_content = []
    TestSuites = os.listdir('./TestSuites')
    for suite in TestSuites:
        total_case_in_testsuite = 0
        pass_case_in_testsuite = 0
        fail_case_in_testsuite = 0
        for key, value in all_testcase_requests.items():
            if suite == value[0]['TestSuite']:
                total_case_in_testsuite += 1
                case_pass_flag = True
                for case in all_testcase_requests[key]:
                    if case['Execution-result'] == 'Fail':
                        case_pass_flag = False
                        fail_case_in_testsuite += 1
                        break
                if case_pass_flag:
                    pass_case_in_testsuite += 1
        table_content.append([suite, str(total_case_in_testsuite), str(pass_case_in_testsuite), str(fail_case_in_testsuite)])
    total_total = 0
    total_pass = 0
    total_fail = 0
    for suite in table_content:
        total_total = int(suite[1]) + total_total
        total_pass = int(suite[2]) + total_pass
        total_fail = int(suite[3]) + total_fail
    table_content.append(['Total', str(total_total), str(total_pass), str(total_fail)])
    col = len(table_content)
    return title, table_content, col


def generate_html_table(title, content, col):
    table = HTMLTable(caption='Test Statistics')
    table.append_header_rows((
        tuple(title),
    ))
    table.append_data_rows(content)
    # title style
    table.caption.set_style({
        'font-size': '20px',
    })
    # header style
    table.set_header_row_style({
        'color': '#000',
        'background-color': '#48a6fb',
        'font-size': '16px',
    })
    table.set_header_cell_style({
        'padding': '10px',
    })
    # <table> style
    table.set_style({
        'border-collapse': 'collapse',
        'word-break': 'break-all',
        'font-size': '12px',
        'width': '800px'
    })
    table.set_cell_style({
        'border-color': '#000',
        'border-width': '1px',
        'border-style': 'solid',
        'padding': '5px',
        'min-width':'100px',
        'text-align':'center'
    })
    table[col].set_cell_style({
        'font-size': '18px'
    })
    html = table.to_html()
    return html

def generate_html(execution, api_version, swagger_base_url, all_testcase_requests):
    info = 'Summary Information<br>' \
           'Swagger Version: {0}<br>' \
           'Swagger URL: {1}'.format(api_version, swagger_base_url)
    title, table_content, col = generate_result_table(all_testcase_requests)
    html = generate_html_table(title, table_content, col)
    message = """
    <html>
    <body>
    <p>%s</p>
    <center><p>%s</p></center>
    </body>
    </html>
    """ % (info, html)
    with open(execution, 'w', encoding='utf-8-sig') as hf:
        hf.write(message)