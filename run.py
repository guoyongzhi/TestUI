import os
import unittest
import time
from library.HTMLTestRunnerNew import HTMLTestRunner
from common.getfiledir import CASEDIR, REPORTDIR
from common.sendemil import Opr_email


class Test_run(object):
    
    def __init__(self):
        self.suit = unittest.TestSuite()
        self.load = unittest.TestLoader()
        self.suit.addTest(self.load.discover(CASEDIR))
        nowTime = time.strftime("%Y-%m-%d %H_%M_%S")
        self.report = os.path.join(REPORTDIR, nowTime + '_report.html')
        
        self.runner = HTMLTestRunner(stream=open(self.report, 'wb'),
                                     title='小郭自动化UI测试工厂', description='We are 伐木累', tester='郭永志')
    
    def execute(self):
        self.runner.run(self.suit)
        # Opr_email(self.report).send_email()


if __name__ == "__main__":
    test_run = Test_run()
    test_run.execute()
