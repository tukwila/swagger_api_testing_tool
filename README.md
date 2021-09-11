# swagger_api_testing_tool
Config files for my GitHub profile.
工具功能
1. 根据swagger api版本(分2.0、3.0版本)解析api定义，梳理每一个api的如下信息：
a. path作为testsuite，
b. CRUD operation: post/get等
c. parameters: 包括参数名，location即in(被封装在api请求的位置), path， query，body，type, required等
d. response：检查测试结果
c. 其他属性；deprecated
2. 根据每一个api的parameter定义按照等价类划分法生成有效类和无效类测试用例
3. 基于测试用例生成测试数据
4. 保存测试用例和测试数据到csv文件
5. 基于测试用例和测试数据生成自动化测试用例脚本
6. 执行自动化测试用例脚本
7. 保存执行结果，生成测试报告
for detail definitions: https://my.oschina.net/tukwila/blog/5257155
