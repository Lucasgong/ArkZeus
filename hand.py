'''
Description: 
Author: zgong
Date: 2020-09-25 01:33:50
LastEditTime: 2020-10-01 17:44:42
LastEditors: zgong
FilePath: /ArkZeus_phone/hand.py
Reference: 
'''
import sys
from pathlib import Path

from base.TaskServer import Server
from base.Worker import Start, Material
from base.Tasker import Tasker


def hand():
    server = Server()
    o = Start('guan', None, is_open=True)
    for task in server.send_tasks():
        tasker = Tasker(task)
        if tasker.valid:
            for planer in tasker.planers:
                m = Material(planer)
                m.run()
    o.quit()


if __name__ == "__main__":
    hand()