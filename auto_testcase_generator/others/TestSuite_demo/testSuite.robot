*** Settings ***
Documentation    Suite description
Library           requests
Library           RequestsLibrary

*** Test Cases ***
sum with two digits
    [Tags]    DEMO
    log       hello, RF
    ${sum}=    evaluate    12+13
test GET request
    ${host_addr}    set variable    https://www.baidu.com/
    create session    InterfaceT    ${host_addr}
    ${response}    GET On Session    InterfaceT    ${host_addr}
    log    ${response.content}
DemoCase1
    ${host_addr}    set variable    https://query.aliyun.com
    ${url}    set variable    /rest/content-platform.api.deliveryGoods
    ${param}    set variable    id=5199093&count=6&env=com&cna=pVmMFp%2FDMX0CAbf2oPzexp3s&realTimeRecommend=[]&version=Goods-2&static=false&showVersion=1&false=1&manual=false&lang=zh
    create session    InterfaceTest    ${host_addr}
    ${ret_result}    get request    InterfaceTest    ${url}    params=${param}
    log    ${ret_result.content}

*** Keywords ***

