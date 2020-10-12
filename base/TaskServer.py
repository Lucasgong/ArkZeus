# 从 config 中 读取信息并传递给worker
# 之后与前端页面结合
import sys
from pathlib import Path
import yaml
import time

class Server():
    def __init__(self):
        tasks = Path('config/account_info.yaml')
        self.account_dic = yaml.load(open(tasks,'r'),Loader=yaml.FullLoader)
        #edittime = Tasks.stat().st_mtime_ns    
    
    def send_tasks(self):
        for i in self.account_dic:
            task = self.account_dic[i]
            yield task


