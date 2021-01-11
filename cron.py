'''
Description: 
Author: zgong
Date: 2020-10-19 03:18:16
LastEditTime: 2020-10-27 19:57:37
LastEditors: zgong
FilePath: /ArkZeus/cron.py
Reference: 
'''
from crontab import CronTab
import os
import sys
import getopt


def set_crontab():
    script_path = os.path.join(os.getcwd(), 'ark.sh')
    log_path = os.path.join(os.getcwd(), 'log/cron.log')
    command = f"{script_path} >> {log_path} 2>&1"

    with CronTab(user=True) as user_cron:
        job = user_cron.new(command=command, comment='ark')
        job.hour.on(7)
        job.hour.also.on(19)
        job.minute.on(0)
        job.enable()
        user_cron.write()
    print('成功添加定时任务')

def del_crontab():
    with CronTab(user=True) as del_cron:
        iter_job = del_cron.find_comment('ark')
        count = 0
        for job in iter_job:
            del_cron.remove(job)
            count += 1
        del_cron.write()
        print(f'成功清除{count}项定时任务~')

if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], 'c')
    is_reset = False
    for cmd, arg in opts:
        if cmd == '-c':
            is_reset = True

    if is_reset:
        del_crontab()
    else:
        set_crontab()
