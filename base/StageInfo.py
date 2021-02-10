'''
Description: 
Author: zgong
Date: 2020-05-17 14:24:50
LastEditTime: 2020-11-10 18:22:23
LastEditors: zgong
FilePath: /ArkZeus/utils/info/StageInfo.py
Reference: 
'''
import requests
import pandas as pd

from utils.config.TimeTable import TIME_TABLE

class StageInfo():
    '''
    根据关卡名字得到关卡信息,类型和掉落信息
    '''
    def __init__(self,name):
        self.valid = False
        self.name = name
        self.check_name()
        if not self.valid:
            raise(f'{name} error')
            #self.duration = self.get_run_time()
    
    def check_name(self):
        name = self.name
        if name.isalpha():
            ## 剿灭作战
            self.stageType = 'ANNI'
            self.stageId = None
            self.code = name
            self.dropInfos = None
            self.valid = True
            return

        req_header = {
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
                }
        with requests.Session() as session:
            resp = session.get('https://penguin-stats.cn/PenguinStats/api/v2/stages?server=CN',headers=req_header)
            resp.raise_for_status()
            for stage in resp.json():
                if stage['code'] == name:
                    self.stageType = stage['stageType']
                    self.stageId = stage['stageId']
                    self.code = name
                    #TODO:
                    # self.dropInfos = self.paser_dropinfo(stage['dropInfos'])
                    self.valid = True                    
                    break
    
    def paser_dropinfo(self,dropinfos):
        infos = {'SPECIAL_DROP':[],'NORMAL_DROP':[],'EXTRA_DROP':[],'FURNITURE':[]}
        df = pd.read_csv('utils/config/item_table.csv',index_col='itemId').to_dict()['name']
        for drop_info in dropinfos:
            if 'itemId' in drop_info:
                infos[drop_info['dropType']].append([df[drop_info['itemId']],drop_info['itemId']])
        return infos
    
    def get_run_time(self):
        return TIME_TABLE[self.name]

