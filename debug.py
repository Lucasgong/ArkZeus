'''
Description: 
Author: zgong
Date: 2020-09-25 01:33:50
LastEditTime: 2021-03-09 23:49:11
LastEditors: zgong
FilePath: /ArkZeus/debug.py
Reference: 
'''
import sys
from pathlib import Path

from base.TaskServer import Server
from base.Worker import Start, Material
from base.Tasker import Tasker

DEVICE="192.168.1.100:5555"
server = Server()
o = Start('guan', None, is_open=True,device_name=DEVICE)
for task in server.send_tasks():
    tasker = Tasker(task)
    if tasker.valid:
        for planer in tasker.planers:
            m = Material(planer)
            break
            #m.run()



