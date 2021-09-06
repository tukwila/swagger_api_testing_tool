# -*- coding:utf-8 -*-
import unittest
import time,os,sys,logging
import HTMLTestRunner

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + r'\..')  # 返回脚本的路径
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='log_test.log',
                    filemode='w')
logger = logging.getLogger()
class MyTest(unittest.TestCase):  # 继承unittest.TestCase

    def setUp(self):
        # 每个测试用例执行之前做操作
        print('执行用例开始')

    def tearDown(self):
        # 每个测试用例执行之后做操作
        print('执行用例结束')

    @classmethod
    def tearDownClass(self):
        # 必须使用 @ classmethod装饰器, 所有test运行完后运行一次
        print('--------测试执行结束--------')

    @classmethod
    def setUpClass(self):
        # 必须使用@classmethod 装饰器,所有test运行前运行一次
        print('--------测试执行开始--------')

    def test_1_add(self):
        """添加类别信息"""
        logger.info("Now: %r", '执行添加')
        self.assertEqual(1, 1)

    def test_2_que(self):
        """查询类别信息"""
        logger.info("Now: %r", '执行查询')
        self.assertEqual(2, 2)

if __name__ == '__main__':
    current_time = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    test_suite = unittest.TestSuite()  # 创建一个测试集合
    test_suite.addTest(MyTest('test_1_add'))
    test_suite.addTest(MyTest('test_2_que'))# 测试套件中添加测试用例
    # test_suite.addTest(unittest.makeSuite(MyTest))#使用makeSuite方法添加所有的测试方法
    report_path = current_time + '.html'  # 生成测试报告的路径
    fp = open(report_path, "wb")
    runner = HTMLTestRunner.HTMLTestRunner(stream = fp,
                                           title = '自动化测试报告',
                                           description = '用例执行情况：',
                                           verbosity = 2)
    runner.run(test_suite)
    fp.close()