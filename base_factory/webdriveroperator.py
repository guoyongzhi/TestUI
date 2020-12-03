import os
import time
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import Chrome
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from common.getfiledir import SCREENSHOTDIR


class WebdriverOperator(object):
    
    def __init__(self, driver: Chrome):
        self.driver = driver
        self.alert = None

    def get_screen_shot_as_file(self):
        """
        截屏保存
        :return:返回路径
        """
        pic_name = str.split(str(time.time()), '.')[0] + str.split(str(time.time()), '.')[1] + '.png'
        screen_path = os.path.join(SCREENSHOTDIR, pic_name)
        self.driver.get_screenshot_as_file(screen_path)
        return screen_path

    @classmethod
    def goto_sleep(cls, **kwargs):
        try:
            s = kwargs['time']
        except KeyError:
            s = 3
        time.sleep(s)
        return True, '等待成功'

    def web_implicitly_wait(self, **kwargs):
        """
        隐式等待
        :return:
        type  存时间
        """
        try:
            s = kwargs['time']
        except KeyError:
            s = 10
        try:
            self.driver.implicitly_wait(s)
        except NoSuchElementException:
            return False, '隐式等待设置失败'
        return True, '隐式等待设置成功'

    def web_element_wait(self, **kwargs):
        """
        等待元素可见
        :return:
        """
        try:
            element_type = kwargs['type']
            locator = kwargs['locator']
        except KeyError:
            return False, '未传需要等待元素的定位参数'
        try:
            s = kwargs['time']
            if s is None:
                s = 30
        except KeyError:
            s = 30
    
        try:
            if element_type == 'id':
                WebDriverWait(self.driver, s, 0.5).until(EC.visibility_of_element_located((By.ID, locator)))
            elif element_type == 'name':
                WebDriverWait(self.driver, s, 0.5).until(EC.visibility_of_element_located((By.NAME, locator)))
            elif element_type == 'class':
                WebDriverWait(self.driver, s, 0.5).until(EC.visibility_of_element_located((By.CLASS_NAME, locator)))
            elif element_type == 'xpath':
                WebDriverWait(self.driver, s, 0.5).until(EC.visibility_of_element_located((By.XPATH, locator)))
            elif element_type == 'css':
                WebDriverWait(self.driver, s, 0.5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, locator)))
            else:
                return False, '不能识别元素类型[' + element_type + ']'
        except TimeoutException:
            screen_shot_path = self.get_screen_shot_as_file()
            return False, '元素[' + locator + ']等待出现失败,已截图[' + screen_shot_path + '].'
        return True, '元素[' + locator + ']等待出现成功'

    def find_element(self, find_type, locator, index=None):
        """
        定位元素
        :param find_type:
        :param locator:
        :param index:
        :return:
        """
        time.sleep(1)
        # isinstance(self.driver, selenium.webdriver.Chrome.)
        if index is None:
            index = 0
        find_type = str.lower(find_type)
        try:
            if find_type == 'id':
                elem = self.driver.find_elements_by_id(locator)[index]
            elif find_type == 'name':
                elem = self.driver.find_elements_by_name(locator)[index]
            elif find_type == 'class':
                elem = self.driver.find_elements_by_class_name(locator)[index]
            elif find_type == 'xpath':
                elem = self.driver.find_elements_by_xpath(locator)[index]
            elif find_type == 'css':
                elem = self.driver.find_elements_by_css_selector(locator)[index]
            else:
                return False, '不能识别元素类型:[' + find_type + ']'
        except Exception as e:
            screen_shot_path = self.get_screen_shot_as_file()
            return False, '获取[' + find_type + ']元素[' + locator + ']失败,已截图[' + screen_shot_path + '].'
        return True, elem

    def element_input(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        try:
            input_type = kwargs['type']
            locator = kwargs['locator']
            text = str(kwargs['input'])
        except KeyError:
            return False, '缺少传参'
        try:
            index = kwargs['index']
        except KeyError:
            index = 0
        isOK, result = self.find_element(input_type, locator, index)
        if not isOK:  # 元素没找到，返回失败结果
            return isOK, result
        elem = result
        try:
            elem.send_keys(text)
        except Exception:
            screen_shot_path = self.get_screen_shot_as_file()
            return False, '元素[' + locator + ']输入[' + text + ']失败,已截图[' + screen_shot_path + '].'
        return True, '元素[' + locator + ']输入[' + text + ']成功'

    def element_click(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        try:
            click_type = kwargs['type']
            locator = kwargs['locator']
        except KeyError:
            return False, '缺少传参'
        try:
            index = kwargs['index']
        except KeyError:
            index = 0
        isOK, result = self.find_element(click_type, locator, index)
        if not isOK:  # 元素没找到，返回失败结果
            return isOK, result
        elem = result
        try:
            elem.click()
        except Exception:
            screen_shot_path = self.get_screen_shot_as_file()
            return False, '元素[' + locator + ']点击失败,已截图[' + screen_shot_path + '].'
        return True, '元素[' + locator + ']点击成功'
    
    def upload_input_file(self, **kwargs):
        """
        input上传文件
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        try:
            input_file_type = kwargs['type']
            locator = kwargs['locator']
            filename = kwargs['file']
        except KeyError:
            return False, '缺少传参'
        try:
            index = kwargs['index']
        except KeyError:
            index = 0
        isOK, result = self.find_element(input_file_type, locator, index)
        if not isOK:  # 元素没找到，返回失败结果
            return isOK, result
        elem = result
        try:
            elem.send_keys(filename)
        except Exception:
            screen_shot_path = self.get_screen_shot_as_file()
            return False, 'input上传文件[' + locator + ']失败,已截图[' + screen_shot_path + '].'
        return True, 'input上传文件[' + locator + ']成功'
    
    def execute_js(self, **kwargs):
        """
        执行JS
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        try:
            locator = kwargs['locator']
        except KeyError:
            return False, '缺少传参'
        self.driver.execute_script(locator)
        return True, 'js[' + locator + ']执行成功'
    
    def toggle_page(self, **kwargs):
        """
        切换页面
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        try:
            index = kwargs['index']
        except KeyError:
            return False, '缺少传参'
        try:
            windows = self.driver.window_handles
            self.driver.switch_to.window(windows[index])
        except Exception:
            screen_shot_path = self.get_screen_shot_as_file()
            return False, '窗口[' + index + ']切换失败 已截图[' + screen_shot_path + '].'
        return True, '窗口[' + index + ']切换成功'
    
    def driver_send_keys(self, key, **kwargs):
        """
        键盘操作
        :param key: 操作转义类型
        :type key: str
        :return:
        :rtype:
        """
        try:
            input_file_type = kwargs['type']
            locator = kwargs['locator']
        except KeyError:
            return False, '缺少传参'
        try:
            index = kwargs['index']
        except KeyError:
            index = 0
        isOK, result = self.find_element(input_file_type, locator, index)
        if not isOK:  # 元素没找到，返回失败结果
            return isOK, result
        elem = result
        try:
            exec('elem.send_keys(Keys.key)')
        except Exception:
            screen_shot_path = self.get_screen_shot_as_file()
            return False, '键盘操作[' + locator + ']失败,已截图[' + screen_shot_path + '].'
        return True, '键盘操作[' + locator + ']成功'

    def switch_alert(self, **kwargs):
        """
        切换到弹窗
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        try:
            s = kwargs['time']
            if s is None:
                s = 30
        except KeyError:
            s = 30
        try:
            time.sleep(s)
            self.alert = self.driver.switch_to.alert()
        except Exception:
            screen_shot_path = self.get_screen_shot_as_file()
            return False, '切换失败 已截图[' + screen_shot_path + '].'
        return True, '切换成功'
    
    def alert_input(self, **kwargs):
        try:
            text = str(kwargs['input'])
        except KeyError:
            return False, '缺少传参'
        try:
            self.alert.send_keys(text)
        except Exception:
            screen_shot_path = self.get_screen_shot_as_file()
            return False, '弹窗输入[' + text + ']失败,已截图[' + screen_shot_path + '].'
        return True, '弹窗输入[' + text + ']成功'

    def alert_click(self):
        try:
            self.alert.accept()
        except Exception:
            screen_shot_path = self.get_screen_shot_as_file()
            return False, '弹窗点击确定失败,已截图[' + screen_shot_path + '].'
        return True, '弹窗点击确定成功'
    
    def alert_close(self):
        try:
            self.alert.dismiss()
        except Exception:
            screen_shot_path = self.get_screen_shot_as_file()
            return False, '弹窗点击关闭失败,已截图[' + screen_shot_path + '].'
        return True, '弹窗点击关闭成功'
    
    def upload_end_key_file(self):
        try:
            self.alert.dismiss()
        except Exception:
            screen_shot_path = self.get_screen_shot_as_file()
            return False, '弹窗点击关闭失败,已截图[' + screen_shot_path + '].'
        return True, '弹窗点击关闭成功'
