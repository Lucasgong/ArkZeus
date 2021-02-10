'''
Description: 
Author: zgong
Date: 2020-05-17 19:17:24
LastEditTime: 2021-01-30 13:05:13
LastEditors: zgong
FilePath: /ArkZeus_phone/base/Tasker.py
Reference: 
'''
import sys
import time
from pathlib import Path

from utils.config.setting import Calendar_Chip
from utils.config.setting import Calendar_Supply


class Planer():
    def __init__(self,plan,day):
        self.valid = False
        if plan['num'] > 0:
            if self.check_plan(plan['name'],day):
                self.day = day
                self.name = plan['name']
                self.num = plan['num']
                self.valid = True
    
    def add_potion_stone(self,is_potion,is_stone):
        self.is_potion = is_potion
        self.is_stone = is_stone

    def __str__(self):
        return f'{self.name}:{self.num}'
    
    @staticmethod
    def check_plan(name,day):
        # 检查芯片
        # TODO: 根据关卡时间检查活动图
        condition = True
        if name[:2] == 'PB':
            na = name[4]
            ls = Calendar_Chip[day]
            if na not in ls:
                condition = False
        elif name[:2] in ['LS', 'CA', 'AP', 'CE', 'SK']:
            ls = Calendar_Supply[day]
            if name[:2] not in ls:
                condition = False
        return condition


class Tasker():

    def __init__(self,task):
        self.valid = False
        if task['skip']:
            return
        self.kind = task['kind']
        self.loader = {'account':task['account'],'password':task['password']}
        self.day = [time.ctime()[:3], 'holiday'][task['holiday']]
        self.planers = []
        for plan in task['plan']:
            planer = Planer(plan,self.day)
            if planer.valid:
                planer.add_potion_stone(task['use_potion'],task['use_stone'])
                self.planers.append(planer)
                self.valid = True

    def __repr__(self):
        return f'plan:{len(self.planers)} {bool(self.valid)}'
