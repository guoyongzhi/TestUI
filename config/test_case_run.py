import unittest
from common.factory import Factory
from common.log import mylog
from ddt import ddt, data, feed_data, add_test
from common.getconf import *


@ddt
class Test_case_run(unittest.TestCase):
    run_path = os.path.join(DATADIR, Config().get('base', 'project'))
    names = file_name(run_path, 'files')
    execute_cases = []
    
    def run_case(self, cases_dict):
        for key, cases in cases_dict.items():
            mylog.info('\n----------用例【%s】开始----------' % cases[0].get('sheet'))
            print('\n')
            for case in cases:
                # print(case)
                isOK, result = self.fac.execute_keyword(**case)
                if isOK:
                    # print(result)
                    mylog.info(result)
                else:
                    mylog.error(result)
                    raise Exception(result)
            mylog.info('\n----------用例【%s】结束----------' % cases[0].get('sheet'))
    for n in names:
        fac = Factory(n, run_path)
        isOK, execute_case = fac.init_execute_case()
        execute_cases.extend(execute_case)
        for i in execute_case:
            # add_test(cls=data(), test_name=n.split('.')[0], test_docstring=i, func=run_case)  # 添加测试方法1
            feed_data(func=run_case, new_name=n.split('.')[0], test_data_docstring=i)  # 添加测试方法二
    
    @data(*execute_cases)  # 方法三（data数据list重载，需要缩进到for循环添加重载后面）
    def test_run(self, cases_dict):
        for key, cases in cases_dict.items():
            mylog.info('\n----------用例【%s】开始----------' % cases[0].get('sheet'))
            print('\n')
            for case in cases:
                # print(case)
                isOK, result = self.fac.execute_keyword(**case)
                if isOK:
                    # print(result)
                    mylog.info(result)
                else:
                    mylog.error(result)
                    raise Exception(result)
            mylog.info('\n----------用例【%s】结束----------' % cases[0].get('sheet'))
        
        # def tearDown(self):
        #     return self.fac.close()
    

# @ddt
# class Test_console_run(unittest.TestCase):
#     fac = Factory('console')
#     isOK, execute_cases = fac.init_execute_case()
#
#     @unittest.skipIf(execute_cases is None, '用例为空，不执行')
#     @data(*execute_cases)
#     def test_run(self, cases_dict):
#         for key, cases in cases_dict.items():
#             mylog.info('\n----------用例【%s】开始----------' % cases[0].get('sheet'))
#             print('\n')
#             for case in cases:
#                 # print(case)
#                 isOK, result = self.fac.execute_keyword(**case)
#                 if isOK:
#                     # print(result)
#                     mylog.info(result)
#                 else:
#                     mylog.error(result)
#                     raise Exception(result)
#             mylog.info('----------用例【%s】结束----------\n' % cases[0].get('sheet'))
#
#     # def tearDown(self):  #     return self.fac.close()


# @ddt
# class Test_login_run(unittest.TestCase):
#     fac = Factory('login')
#     isOK, execute_cases = fac.init_execute_case()
#
#     @data(*execute_cases)
#     def test_run(self, cases_dict):
#         for key, cases in cases_dict.items():
#             mylog.info('\n----------用例【%s】开始----------' % cases[0].get('sheet'))
#             print('\n')
#             for case in cases:
#                 # print(case)
#                 isOK, result = self.fac.execute_keyword(**case)
#                 if isOK:
#                     # print(result)
#                     mylog.info(result)
#                 else:
#                     mylog.error(result)
#                     raise Exception(result)
#             mylog.info('----------用例【%s】结束----------\n' % cases[0].get('sheet'))


if __name__ == '__main__':
    unittest.main()
