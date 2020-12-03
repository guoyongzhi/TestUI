import os
from configparser import ConfigParser
from common.getfiledir import CONFDIR, DATADIR


class Config(ConfigParser):
    
    def __init__(self):
        self.conf_name = os.path.join(CONFDIR, 'base.ini')
        super().__init__()
        super().read(self.conf_name, encoding='utf-8')
    
    def save_data(self, section, option, value):
        super().set(section=section, option=option, value=value)
        super().write(fp=open(self.conf_name, 'w'))


def file_name(file_dir, file_type):
    for root, dirs, files in os.walk(file_dir):
        if file_type == 'root':
            return root  # 当前目录路径
        if file_type == 'dirs':
            return dirs  # 当前路径下所有子目录
        if file_type == 'files':
            return files  # 当前路径下所有非目录子文件
        

if __name__ == '__main__':
    con = Config()
    # print(dict(con.items('base'))['project'])
    names = file_name(os.path.join(DATADIR, con.get('base', 'project')), 'files')
    name = []
    for n in names:
        name.append(n.split('.')[0])
        print(n, type(n))
    print(dict(zip(name, names)))
