import os
import shutil
import unittest
import time
from library.HTMLTestRunnerNew import HTMLTestRunner
from common.getfiledir import CASEDIR, REPORTDIR, CONFDIR, DATADIR
from common.new_add_file import write_test_info
from common.getconf import Config, file_name
from common.sendemil import Opr_email


class Test_run(object):
    def __init__(self, is_establish=False):
        CASEDIR_test = os.path.join(CASEDIR, 'test_case_run.py')
        now_names = file_name(CASEDIR, 'files')  # 获取现在的test文件夹
        if not is_establish:  # 处理不分类的测试（全部在一个套件）
            if not os.path.exists(CASEDIR_test):
                common_test = os.path.join(CONFDIR, 'test_case_run.py')
                shutil.copy(common_test, CASEDIR)
            if len(now_names) > 3:
                for s in now_names:
                    if 'init' not in s and 'test_case_run' not in s:
                        try:
                            os.remove(os.path.join(CASEDIR, s))
                        except Exception as e:
                            if 'geckodriver' in s:
                                pass
                            else:
                                print("删除文件失败", e)
        else:  # 处理分类的测试
            run_path = os.path.join(DATADIR, Config().get('base', 'project'))
            for s in now_names:
                if 'init' not in s:
                    try:
                        os.remove(os.path.join(CASEDIR, s))
                    except Exception as e:
                        if 'geckodriver' in s:
                            pass
                        else:
                            print("删除文件失败", e)
            
            names = file_name(run_path, 'files')
            for n in names:
                if not os.path.exists(os.path.join(run_path, 'test_' + n)):
                    write_test_info(file_dir=CASEDIR, name=n.split('.')[0], n=n, path=run_path)
        # time.sleep(5)
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
    test_run = Test_run(is_establish=True)
    test_run.execute()
