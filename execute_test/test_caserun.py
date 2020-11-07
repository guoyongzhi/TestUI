import unittest
from common.factory import Factory
from common.log import mylog
from ddt import ddt, data


@ddt
class Test_case_run(unittest.TestCase):
    fac = Factory('case')
    isOK, execute_cases = fac.init_execute_case()
    
    @data(*execute_cases)
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
            mylog.info('----------用例【%s】结束----------\n' % cases[0].get('sheet'))
    
    # def tearDown(self):
    #     return self.fac.close()


@ddt
class Test_console_run(unittest.TestCase):
    fac = Factory('console')
    isOK, execute_cases = fac.init_execute_case()
    
    @unittest.skipIf(execute_cases is None, '用例为空，不执行')
    @data(*execute_cases)
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
            mylog.info('----------用例【%s】结束----------\n' % cases[0].get('sheet'))
    
    # def tearDown(self):  #     return self.fac.close()


@ddt
class Test_login_run(unittest.TestCase):
    fac = Factory('login')
    isOK, execute_cases = fac.init_execute_case()
    
    @data(*execute_cases)
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
            mylog.info('----------用例【%s】结束----------\n' % cases[0].get('sheet'))


if __name__ == '__main__':
    unittest.main()
