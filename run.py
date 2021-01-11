'''
Description: 
Author: zgong
Date: 2020-08-19 10:27:06
LastEditTime: 2020-10-27 19:31:37
LastEditors: zgong
FilePath: /ArkZeus/run.py
Reference: 
'''
import datetime

from base.TaskServer import Server
from base.Worker import Start, Material
from base.Tasker import Tasker
from etc.update_item import update

def main():
    update()
    server = Server()
    for task in server.send_tasks():
        tasker = Tasker(task)
        if tasker.valid:
            o = Start(tasker.kind, tasker.loader)
            for planer in tasker.planers:
                m = Material(planer)
                m.run()
            o.quit()

if __name__ == "__main__":
    main()
