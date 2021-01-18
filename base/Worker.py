'''
Description: define useful worker
Author: zgong
Date: 2020-10-01 16:07:47
LastEditTime: 2021-01-18 21:59:31
LastEditors: zgong
FilePath: /ArkZeus/base/Worker.py
Reference: 
'''
import datetime
import os
import time

from tqdm import tqdm

from .Gamer import PhoneGamer
from .StageSelector import StageSelector
from utils.info.StageInfo import StageInfo


class Start(PhoneGamer):
    def __init__(self, kind, loader, is_open=False):
        self.device_name = "192.168.1.105:5555"
        self.connect()
        self.rotation_to_row()
        super().__init__(kind)
        if not is_open:
            self.quit()
            self.load(kind)
            self.login(loader['account'], loader['password'])
            self.first_open()

    def quit(self):
        if self.kind == 'guan':
            os.system(
                'adb shell am force-stop com.hypergryph.arknights'
            )
        else:
            os.system(
                'adb shell am force-stop com.hypergryph.arknights.bilibili'
            )

    def load(self, kind):
        if kind == 'bl':
            os.system(
                'adb shell am start -n com.hypergryph.arknights.bilibili/com.u8.sdk.SplashActivity'
            )
            time.sleep(30)
            self.click(100, 100, 10)
            time.sleep(30)

        if kind == 'guan':
            os.system(
                'adb shell am start -n com.hypergryph.arknights/com.u8.sdk.U8UnityContext'
            )
            time.sleep(30)
            self.click(100, 100, 10)
            time.sleep(30)
            # check_load
            v = self.check('utils/config/pic/base/load.png')['conf']
            print(v)
            if v > 0.9:
                self.click(737, 610, 2)

            self.click(315, 430, 2)
            # 可能直接进入到了登陆界面，需要看情况选择,最好是点到空白的地方
            print('ready to login')

    def login(self, account, password):
        self.click(500, 380, 2)
        os.system(f'adb shell input text {account}')
        time.sleep(2)
        self.click(960, 100, 2)

        self.click(500, 430, 2)
        os.system(f'adb shell input text {password}')
        time.sleep(2)
        self.click(960, 100, 2)

        self.click(502, 511, 2)
        time.sleep(30)
        print('login successful')

    def first_open(self):
        #TODO:has problem!
        self.click_image('utils/config/pic/base/quit.png')
        self.click_image('utils/config/pic/base/comfirm.png')
        self.click_image('utils/config/pic/base/quit.png')
        # 登陆奖励
        self.check_register()
        condi = True
        while condi:
            condi = self.click_image('utils/config/pic/base/quit.png')
        print('ready to fight!')


class Material(PhoneGamer):
    # 每次只给一个planer
    def __init__(self, planer):
        super().__init__('guan')
        self.planer = planer

        self.stageinfo = StageInfo(self.planer.name)
        self.stageselector = StageSelector(self.planer.name, self.planer.day,
                                           self.stageinfo.stageType)

    def run(self):
        print(f'go to {self.planer.name}:{self.planer.num}times')
        self.screenshot(name='state_old')
        self.stageselector.run()
        duration = self.stageinfo.duration
        print('ready?')
        time.sleep(5)
        print('go!')
        for _ in tqdm(range(self.planer.num)):
            self.battle(duration, self.planer.name, self.planer.is_potion,
                        self.planer.is_stone)
            time.sleep(5)
        self.back_to_main()
        self.screenshot(name='state_now')

    def battle(self, duration, name, use_potion=False, use_stone=False):
        self.click(900, 600, 5)
        if use_potion:
            # if (not use_stone):
            #     if self.check('utils/config/pic/base/stone.png')['conf'] > 0.9:
            #         self.click(900, 400, 3)
            #     else:
            #         self.click(870, 500, 3)
            # else:
            self.click(870, 500, 3)
        else:
            self.click(900, 400, 3)

        self.click(900, 600, 5)
        self.click(900, 400, 3)
        self.click(570, 500, duration)
        #拉长时间？不需要，
        #parse_reward(name)
        self.click(900, 150, 5)
        self.click(900, 150, 0)

    def back_to_main(self):
        condi = True
        while condi:
            condi = self.click_image('utils/config/pic/base/arrow.png')
        now = datetime.datetime.today().strftime('%Y%m%d %H:%M')
        print(f'back to main {now}')
