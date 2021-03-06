# 从主页面到选定页面
import os
import time
import re

from .Gamer import PhoneGamer
from utils.config.setting import Calendar_Supply


class StageSelector(PhoneGamer):
    def __init__(self, name, day, stagetype, device_name="192.168.1.105:5555"):
        super().__init__('guan', device_name)
        self.name = name
        self.day = day
        self.stagetype = stagetype

    def route(self):
        # {'ACTIVITY', 'DAILY', 'MAIN', 'SUB'}
        if self.stagetype == 'ACTIVITY':
            self.route_activity(self.name, self.day)
            self.click_stage(self.name)

        elif self.stagetype == 'MAIN':
            self.route_main(self.name, self.day)
            self.click_stage(self.name)

        elif self.stagetype == 'DAILY':
            self.route_daily(self.name, self.day)
            #self.click_image(pic_path, check=False)

        elif self.stagetype == 'SUB':
            self.route_main(self.name, self.day)
            self.click_stage(self.name)

        elif self.stagetype == 'ANNI':
            self.route_annihilation(self.name, self.day)

        self.check_angency()

    def run(self):
        self.route()

    def route_activity(self, name, day, loc=0):
        # 根据活动位置修改
        up_down = [(950, 150, 3), (950, 200, 3)]
        activity = name[:2]
        if activity == 'DM':
            self.click(*up_down[loc])
            self.click(750, 450, 3)
            return

        if activity == 'SV':
            self.click(*up_down[loc])
            self.click(150, 450, 3)
            return
        if activity == 'TW':
            self.click(*up_down[loc])
            self.click(920, 300, 3)
            self.go_to_right()
            self.swipe_page(0.5)
            return
        if activity == 'OF':
            self.click(*up_down[loc])
            if name[3] == 'F':
                self.click(880, 360, 3)
            else:
                self.click(880, 300, 3)
                self.go_to_right()
                self.swipe_page(2)
            return
        if activity == 'RI':
            self.click(*up_down[1])
            self.click(930, 300, 3)
            self.go_to_right()
            self.swipe_page(2)
            return
        if activity == 'GT':
            self.click(650, 200, 3)
            self.click(680, 600, 3)
            self.click(800, 355, 3)
            return
        if activity == 'MN':
            self.click(*up_down[loc])
            self.click(2000 / self.x_ratio, 830 / self.y_ratio, 3)
            self.go_to_right(2)
            self.swipe_page(1.5)
            return
        if activity == 'MB':
            self.click(*up_down[loc])
            self.click(2240 / self.x_ratio, 350 / self.y_ratio, 3)
            return
        if activity == 'BH':
            self.click(*up_down[loc])
            self.click(880, 500, 3)
            return
        if activity == 'WR':
            self.click(*up_down[loc])
            self.click(920, 550, 3)
            self.go_to_right(2)
            self.swipe_page(1)
            return
        if activity == 'OD':
            self.click(*up_down[1])
            time.sleep(10)
            self.click_detected_text('行动记录')
            self.go_to_right(2)
            self.swipe_page(2)
            return
        if activity == 'WD':
            self.click(*up_down[1])
            time.sleep(10)
            self.click_detected_text('独行')
            self.go_to_right(2)
            self.swipe_page(1)
            return
        else:
            raise Exception(f'place set entrance of {activity}!')

    def route_main(self, name, day):
        self.click(650, 200, 3)
        for i in name:
            if i.isdigit():
                self.go_to_chapter(i)
                break

        # with open('utils/config/stage_loc_table.csv', 'r') as handler:
        #     for line in handler:
        #         stage, num_tmp = line.strip().split(',')
        #         if stage == name:
        #             num = float(num_tmp)
        #             self.swipe_page(num)
        #             return

        # print(f'please set stage page')
        # raise Exception

    def route_annihilation(self, name, day):
        self.click(650, 200, 3)
        if name == 'jiaomie':
            self.click_detected_text('合成玉')
            
        # self.click(430, 600, 3)
        # self.go_to_right(1)
        # self.click(970, 570, 3)
        # self.click(500, 300, 3)
            
        # if name == 'shiqu':
        #     self.click(800, 300, 3)
        # elif name == 'waihuan':
        #     self.click(600, 400, 3)
        # elif name == 'qishi':
        #     self.click(500, 250, 3)
        # elif name == 'feixu':
        #     self.click_detected_text('北原冰封废城')
        # elif name == 'kuangqu':
        #     self.click_detected_text('废弃矿区')

    def route_daily(self, name, day):
        self.click(650, 200, 3)
        if self.is_supplies(name):
            index = self.return_index(name, day)
            self.go_to_supplies(index)
            level = int(name[-1])
            l = 780 - 100 * (5 - level)
            h = 180 + 90 * (5 - level)
            self.click(l, h)

        else:
            chiptype = self.which_chip(name)
            if chiptype:
                self.click(300, 600)
                self.click_stage(chiptype)
                if name[-1] == '1':
                    self.click(320, 380)
                elif name[-1] == '2':
                    self.click(670, 230)

    def go_to_chapter(self, chapter):
        self.go_to_right()
        self.click(720, 360)
        for _ in range(int(chapter) - 1):
            self.click(950, 620)
        self.go_to_right()

        print(f'go to {chapter}chapter')

    def go_to_supplies(self, position):
        self.click(180, 600)
        self.swipe(0, 200, 1000, 200)
        self.click(200 * position - 50, 300)

    def return_index(self, name, day):
        na = name[:2]
        ls = Calendar_Supply[day]
        if na in ls:
            return ls.index(na) + 1
        else:
            print(f'no {na}')
            return (1)

    def is_supplies(self, name):
        na = name[:2]
        return na in ['LS', 'CA', 'AP', 'CE', 'SK']

    def is_chip(self, name):
        na = name[:2]
        return na in ['PR']

    def which_chip(self, name):
        chip_dic = {'A': '固若金汤', 'B': '摧枯拉朽', 'C': '势不可挡', 'D': '身先士卒'}
        if self.is_chip(name):
            chip_type = chip_dic[name[3]]
            return chip_type
        else:
            return False
