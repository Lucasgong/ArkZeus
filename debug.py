'''
Description: 
Author: zgong
Date: 2020-09-25 01:33:50
LastEditTime: 2020-10-15 23:17:32
LastEditors: zgong
FilePath: /ArkZeus/debug.py
Reference: 
'''
import sys
from pathlib import Path

from base.TaskServer import Server
from base.Worker import Start, Material
from base.Tasker import Tasker


server = Server()
o = Start('guan', None, is_open=True,device_name="192.168.50.70:5555")
for task in server.send_tasks():
    tasker = Tasker(task)
    if tasker.valid:
        for planer in tasker.planers:
            m = Material(planer)
            break
            #m.run()



