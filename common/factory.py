from common.getconf import Config
from common.getcase import ReadCase
from base_factory.browseroperator import BrowserOperator
from base_factory.webdriveroperator import WebdriverOperator
# from selenium.webdriver.common.keys import Keys


class Factory(object):
    
    def __init__(self, case='case'):
        self.con = Config()
        self.con_fun = dict(self.con.items('Function'))
        self.con_keys = dict(self.con.items('Keys'))
        self.con_case = dict(self.con.items('Case'))
        self.case = case
        """
        浏览器操作对象
        """
        self.browser_opr = BrowserOperator()
        """
        网页操作对象
        """
        self.webdriver_opr = None

    def init_webdriver_opr(self, driver):
        self.webdriver_opr = WebdriverOperator(driver)

    def get_base_function(self, function_name):
        try:
            function = getattr(self.browser_opr, function_name)
        except Exception:
            try:
                function = getattr(self.webdriver_opr, function_name)
            except Exception:
                return False, '未找到注册方法[' + function_name + ']所对应的执行函数，请检查配置文件'
        return True, function
    
    # @classmethod
    # def get_base_keys(self, keys_name):
    #     try:
    #         keys = getattr(self.con_keys, keys_name)
    #     except Exception:
    #         return False, '未找到键盘操作方法[' + keys_name + ']所对应的操作函数，请检查配置文件'
    #     return True, keys

    def execute_keyword(self, **kwargs):
        """
        工厂函数，用例执行方法的入口
        :param kwargs:
        :return:
        """
        try:
            keyword = kwargs['keyword']
            if keyword is None:
                return False, '没有keyword，请检查用例'
        except KeyError:
            return False, '没有keyword，请检查用例'
    
        _is_browser = False
    
        try:
            function_name = self.con_fun[keyword]
        except KeyError:
            # 获取键盘操作的对应类型
            _is_browser = True
            if keyword[:1] == 'F':
                function_name = keyword
            else:
                try:
                    int(keyword)
                    function_name = 'NUMPAD' + keyword
                except Exception:
                    try:
                        function_name = self.con_keys[keyword]
                    except KeyError:
                        return False, '方法Key[' + keyword + ']未注册，请检查用例'
            
        # 判断是否为键盘操作
        if _is_browser:
            isOK, result = self.webdriver_opr.driver_send_keys(function_name, **kwargs)
            return isOK, result
        
        # 获取基础类方法
        isOK, result = self.get_base_function(function_name)
        if isOK:
            function = result
        else:
            return isOK, result

        # 执行基础方法，如打网点页、点击、定位、隐式等待 等
        isOK, result = function(**kwargs)

        # 如果是打开网页，是浏览器初始化，需要将返回值传递给另一个基础类
        if '打开网页' == keyword and isOK:
            url = kwargs['locator']
            self.init_webdriver_opr(result)
            return isOK, '网页[' + url + ']打开成功'
        return isOK, result

    def init_common_case(self, cases):
        """
        :param cases:
        :return:
        """
        cases_len = len(cases)
        index = 0
        for case in cases:
            if case['keyword'] == '调用用例':
                xlsx = ReadCase(self.con_case[self.case])
                try:
                    case_name = case['locator']
                except KeyError:
                    return False, '调用用例没提供用例名，请检查用例'
                isOK, result = xlsx.get_common_case(case_name)
                if isOK and type([]) == type(result):
                    isOK, result_1 = self.init_common_case(result)  # 递归检查公共用例里是否存在调用用例
                elif not isOK:
                    return isOK, result
                list_rows = result[case_name]
                cases[index: index + 1] = list_rows  # 将公共用例插入到执行用例中去
            index += 1
        if cases_len == index:
            return False, ''
        return True, cases

    # [{"a": [{"A": 2}, {"A": 2}, {"A": 2}, {"A": 2}, {"A": 2}, {"A": 2}, {"A": 2}, {"A": 2}, {"A": 2}]},
    # {"a": [5, 3, 2]}, {"a": [10, 4, 6]}]

    def init_execute_case(self):
        print("----------初始化用例----------")
        xlsx = ReadCase(self.con_case[self.case])
        isOK, result = xlsx.readallcase()
        if not isOK:
            print(result)
            print("----------结束执行----------")
            exit()
        all_cases = result
        excu_cases = []
        for cases_dict in all_cases:
            for key, cases in cases_dict.items():
                isOK, result = self.init_common_case(cases)
                if isOK:
                    cases_dict[key] = result
                else:
                    cases_dict[key] = cases
                excu_cases.append(cases_dict)
                print("----------初始化用例完成----------")
        return isOK, excu_cases

    def close(self):
        return self.browser_opr.close_browser()


if __name__ == '__main__':
    f = Factory('case')
    af = f.con_keys["删除"]
    # af = f.execute_keyword(**{'id': 1, 'result': None, 'keyword': '打开网页', 'type': 'url',
    #                           'locator': 'https://www.baidu.com', 'index': None, 'input': None, 'check': None,
    #                           'time': None, 'sheet': 'baidu'})
    print(af)
