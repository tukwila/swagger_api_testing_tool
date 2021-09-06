User Guide
1. Download source code package to your local disk from this confluence page - 3 Source Code Package:
https://confluence.roaddb.com:8443/pages/viewpage.action?pageId=117010978

2. Extract files from auto_testcase_generator.tar.gz by this command:
tar -xvf auto_testcase_generator.tar.gz

3. Change directory to the auto_testcase_generator folder by this command:
cd auto_testcase_generator/auto_orthogonal_arrays_testcase_generator

4. Prepare your parameters under test in json format then save them in json file, for example:
[
  {
    "SuiteName": "suite1",
    "Mode": 0,
    "Num": 0,
    "Design": 1,
    "FactorLevel": {
    "K1": [0, 1],
    "K2": [0, 1],
    "K3": [0, 1]
    }
  }
]
or use sample file in this confluence page - 4 Parameter Under Test in Json：
https://confluence.roaddb.com:8443/pages/viewpage.action?pageId=117010978

5. Assume json file in the current directory, execute the following command in your terminator then orthogonal result will be generated:
auto_orthogonal_arrays_testcase_generator ~$python3 main.py -i ./test.json -o ./test.csv
Notes:
a. -i means that input file is test.json in the current directory
b. -o means that result will save into output file test.csv file; and csv is recommended.

6. New function: this tool support extracting parameters from swagger api_docs, the command:
auto_orthogonal_arrays_testcase_generator ~$python3 main.py -s http://127.0.0.1:8080/v2/api-docs -o ./test.csv
Notes:
a. -s means swagger api_docs url
b. -s or -i cannot be used in the same time which means parameters under test are from json file or from swagger but cannot be from both source