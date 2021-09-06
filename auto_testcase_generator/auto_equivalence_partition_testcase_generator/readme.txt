User Guide

1. Precondition: install python-dateutil lib under python3 environment by this command:
pip3 install python-dateutil

2. Download source code package to your local disk from this confluence page - 3 Source Code Package:
https://confluence.roaddb.com:8443/pages/viewpage.action?pageId=117000626

3. Extract files from auto_equivalence_partition_testcase_generator.tar.gz by this command:
tar -xvf auto_equivalence_partition_testcase_generator.tar.gz

4. Change directory to the auto_equivalence_partition_testcase_generator folder by this command:
cd auto_equivalence_partition_testcase_generator

5. Prepare your parameters under test in json format then save them in json file, for example:
[
    {
        "parameterName":"用户名",
        "parameterType":"VARCHAR2",
        "parameterRange":[3,20],
        "ifNull":true,
        "validChar":[
            "uppercase",
            "lowercase",
            "."
        ],
        "caseSensitive":true
    }
]
or use sample file in this confluence page - 4 Parameter Under Test in Json：
https://confluence.roaddb.com:8443/pages/viewpage.action?pageId=117000626

6. Assume json file in the current directory, execute the following command in your terminator then equivalent partition result will be generated:
auto_equivalence_partition_testcase_generator ~$python3 main.py -i ./test.json -o ./test.csv
Notes:
a. -i means that input file is test.json in the current directory
b. -o means that result will save into output file test.csv file; and csv is recommended.

7. Check equivalence partition testcases in csv file:
7.1 All testcases are in the Title column
7.2 There is one valid equivalence partition test case and there are some invalid equivalence partition testcases for one parameter under test
7.3 There are some testing data for every test case

8. New function: this tool support extracting parameters from swagger api_docs, the command:
auto_equivalence_partition_testcase_generator ~$python3 main.py -s http://127.0.0.1:8080/v2/api-docs -o ./test.csv
Notes:
a. -s means swagger api_docs url
b. -s or -i cannot be used in the same time which means parameters under test are from json file or from swagger but cannot be from both source