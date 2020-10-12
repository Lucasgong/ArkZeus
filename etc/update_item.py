'''
Description: 
Author: zgong
Date: 2020-05-17 19:53:46
LastEditTime: 2020-10-01 16:42:55
LastEditors: zgong
FilePath: /ArkZeus_phone/etc/update_item.py
Reference: 
'''
import requests
import pandas as pd

def update():
    with requests.Session() as session:
        resp = session.get('https://penguin-stats.io/PenguinStats/api/v2/items')
        resp.raise_for_status()
        df = pd.DataFrame(resp.json(),columns=['itemId','name'])
        df.to_csv('utils/config/item_table.csv',index=False)
    print('update ok')