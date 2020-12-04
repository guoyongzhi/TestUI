import openpyxl
import os
from common.getfiledir import DATADIR  # 导入data目录


class ReadCase(object):
    def __init__(self, case='case', project=None):
        self.file = os.path.join(project, case)  # 得到case文件的路径
        self.sw = openpyxl.load_workbook(self.file)
        # print(self.sw)

    def open_sw(self, file):
        """
        打开文件
        :param file:
        :type: str
        :param dir:
        :return:
        """
        self.sw = openpyxl.load_workbook(file)
    
    @classmethod
    def read_case(cls, sh=None, is_close=True):
        """
        组合sheet页的数据
        :param sh:
        :param is_close:
        :return: list,返回组合数据
        """
        if sh is None:
            return False, '用例页参数未传'
        datas = list(sh.rows)
        if datas == []:
            return False, '用例[' + sh.title + ']里面是空的'
        title = [i.value for i in datas[0]]
        rows = []
        sh_dict = {}
        for i in datas[1:]:
            data = [v.value for v in i]
            row = dict(zip(title, data))
            if not is_close:
                if '关闭浏览器' == row['keyword']:
                    continue
            try:
                if str(row['id'])[0] is not '#':
                    row['sheet'] = sh.title
                    rows.append(row)
            except KeyError:
                raise e
                rows.append(row)
            sh_dict[sh.title] = rows
        return True, sh_dict

    def read_all_case(self):
        """
        取所有sheet页
        :return:list,返回sheet页里的数据
        """
        sheet_list = []
        for sh in self.sw:  # 遍历sheet，
            if 'common' != sh.title.split('_')[0] and 'common' != sh.title.split('-')[0] and sh.title[0] is not '#':
                # 判断是否可用的用例
                isOK, result = self.read_case(sh)  # 传给read_case取用例
                if isOK:
                    sheet_list.append(result)  # 得到结果放到列表，又给用例套了一层sheet页的框
        if sheet_list is None:
            return False, '用例集是空的，请检查用例'
        return True, sheet_list

    def get_common_case(self, case_name, case_index=''):
        """
        得到公共用例
        :param case_name:
        :param case_index:
        :return:
        """
        if case_index and case_index != self.file:
            self.open_sw(case_index)
        try:
            sh = self.sw.get_sheet_by_name(case_name)
        except KeyError:
            return False, '未找到公共用例[' + case_name + '],请检查用例'
        except DeprecationWarning:
            pass
        return self.read_case(sh, is_close=False)


if __name__ == '__main__':
    ReadCase(case='verify_console.xlsx', project=r'I:\work\TestUI\data\identityface').get_common_case('admin', r'I:\work\TestUI\data\identityface\verify_console.xlsx')