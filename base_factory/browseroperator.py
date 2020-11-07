import os
import win32gui
import win32con
import time
from selenium import webdriver
from common.getconf import Config
from common.getfiledir import LIBRARY
from pywinauto import application


class BrowserOperator(object):
    
    def __init__(self):
        self.conf = Config()
        # self.driver_path = os.path.join(BASEFACTORYDIR, 'chromedriver.exe')
        self.deriver_type = str(self.conf.get('base', 'browser_type')).lower()
    
    def open_url(self, **kwargs):
        """
        打开网页
        :param url:
        :return: 返回 webdriver
        """
        try:
            url = kwargs['locator']
        except KeyError:
            return False, '没有URL参数'
        try:
            if self.deriver_type == 'chrome':
                # 处理chrom弹出的info
                # chrome_options = webdriver.ChromeOptions()
                # #option.add_argument('disable-infobars')
                # chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
                # self.driver = webdriver.Chrome(options=chrome_options, executable_path=self.driver_path)
                self.driver = webdriver.Chrome(executable_path=os.path.join(LIBRARY, 'chromedriver.exe'))
            elif self.deriver_type == 'ie':
                self.driver = webdriver.Ie(executable_path=os.path.join(LIBRARY, 'IEDriverServer.exe'))
            elif self.deriver_type == 'firefox':
                self.driver = webdriver.Firefox(executable_path=os.path.join(LIBRARY, 'geckodriver.exe'))
            else:
                print("不支持的浏览器插件")
            time.sleep(1)
            self.driver.maximize_window()
            self.driver.get(url)
        except Exception as e:
            return False, e
        return True, self.driver
    
    def close_browser(self, **kwargs):
        """
        关闭浏览器
        :return:
        """
        time.sleep(1)
        self.driver.quit()
        time.sleep(2)
        return True, '关闭浏览器成功'
    
    def upload_file(self, **kwargs):
        """
        上传文件
        :param kwargs:
        :return:
        """
        try:
            dialog_class = kwargs['type']
            file_dir = kwargs['locator']
            button_name = kwargs['index']
        except KeyError:
            return True, '没传对话框的标记或没传文件路径,'
        
        if self.deriver_type == "chrome":
            title = "打开"
        elif self.deriver_type == "firefox":
            title = "文件上传"
        elif self.deriver_type == "ie":
            title = "选择要加载的文件"
        else:
            title = ""  # 这里根据其它不同浏览器类型来修改  # 找元素  # 一级窗口"#32770","打开"
        dialog = win32gui.FindWindow(dialog_class, title)
        if dialog == 0:
            return False, '传入对话框的class定位器有误'
        # 向下传递
        ComboBoxEx32 = win32gui.FindWindowEx(dialog, 0, "ComboBoxEx32", None)  # 二级
        comboBox = win32gui.FindWindowEx(ComboBoxEx32, 0, "ComboBox", None)  # 三级
        # 编辑按钮
        edit = win32gui.FindWindowEx(comboBox, 0, 'Edit', None)  # 四级
        # 打开按钮
        
        button = win32gui.FindWindowEx(dialog, 0, 'Button', button_name)  # 二级
        if button == 0:
            return False, '按钮text属性传值有误'
        # 输入文件的绝对路径，点击“打开”按钮
        win32gui.SendMessage(edit, win32con.WM_SETTEXT, None, file_dir)  # 发送文件路径
        time.sleep(1)
        win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)  # 点击打开按钮
        return True, '上传文件成功'
