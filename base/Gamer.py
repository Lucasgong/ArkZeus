'''
Description: define basic operator
Author: zgong
Date: 2020-05-17 13:16:40
LastEditTime: 2021-01-18 22:53:12
LastEditors: zgong
FilePath: /ArkZeus/base/Gamer.py
Reference: 
'''
# 启动服务器并登陆
import datetime
import os
import platform
import time
from pathlib import Path

from cv2 import cv2
from tqdm import tqdm


class Gamer():
    def __init__(self, kind, device_name):
        # 默认分辨率 1024*640
        self.device_name = device_name
        self.kind = kind

    def connect(self):
        # 自动连接一个adb 文件,之后返回连接的个数
        while True:
            os.system('adb kill-server')
            time.sleep(2)
            os.system(f'adb connect {self.device_name}')
            if platform.system() == 'Windows':
                os.system('adb connect 127.0.0.1:7555')
            else:
                os.system('adb devices')
            f = os.popen('adb devices')
            result = f.read()
            f.close()
            if (self.device_name in result) and not ("offline" in result):
                print('connected !')
                break
            else:
                os.system('adb kill-server')
                os.system('adb start-server')
                os.system(f'adb connect {self.device_name}')
            time.sleep(10)

    def imshow(self, img, name='imageWindow'):
        cv2.imshow(name, img)
        cv2.waitKey(1000)
        cv2.destroyAllWindows()


class PhoneGamer(Gamer):
    '''
    description: 适配于手机旋转界面的操作,要将一系列操作重新定义
    param : 
    return {type} 
    '''
    def __init__(self, kind):
        super().__init__(kind, "192.168.1.105:5555")
        self.get_resolution()

    def rotation_to_row(self):
        os.system(
            'adb shell settings put system user_rotation 1')
        os.system(
            'adb shell settings put system accelerometer_rotation 0'
        )

    def get_resolution(self):
        f = os.popen('adb shell wm size')
        result = f.read()
        Y, X = result.split(' ')[-1].strip().split('x')
        self.x_ratio = int(X) / 1024
        self.y_ratio = int(Y) / 640

    def click(self, x, y, duration=3):
        x, y = self.x_ratio * x, self.y_ratio * y
        os.system(f'adb shell input tap {x} {y}')
        time.sleep(duration)

    def swipe(self, x1, y1, x2, y2, use_time=False, duration=3):
        x1, y1, x2, y2 = self.x_ratio * x1, self.y_ratio * y1, self.x_ratio * x2, self.y_ratio * y2
        if use_time:
            os.system(
                f'adb shell input swipe {x1} {y1} {x2} {y2} {use_time}'
            )
        else:
            os.system(
                f'adb shell input swipe {x1} {y1} {x2} {y2}')
        time.sleep(duration)

    def __swipe_half_page(self):
        self.swipe(1000,
                   300 / self.y_ratio,
                   875,
                   300 / self.y_ratio,
                   duration=1)

    def swipe_page(self, num):
        for _ in range(int(num / 0.5)):
            self.__swipe_half_page()

    def go_to_right(self, n=5):
        for _ in range(n):
            self.swipe(0, 200, 900, 200, 100)
        time.sleep(3)

    def screenshot(self, num=0, name='screen'):
        screen_file = Path(f'data/{name}.png')
        if not screen_file.exists():
            screen_file.parent.mkdir(parents=True,exist_ok=True)
        os.system(
            f'adb exec-out screencap -p > data/{name}.png')
        img = cv2.imread(f'data/{name}.png')
        if img.shape[0] > img.shape[1]:
            img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        img = cv2.resize(img, (1024, 640))
        cv2.imwrite(f'data/{name}.png', img)

    def check(self, pic_path, screen='screen'):
        # find pic location
        template = cv2.imread(pic_path)
        h, w, _ = template.shape
        self.screenshot(screen)
        img = cv2.imread(f'data/{screen}.png')
        res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        _, max_v, _, top_left = cv2.minMaxLoc(res)
        x = top_left[0] + 0.5 * w
        y = top_left[1] + 0.5 * h
        return {'conf': max_v, 'x': x, 'y': y}

    def click_image(self, pic_path, screen_name='screen', check=True):
        # find pic location
        template = cv2.imread(pic_path, 0)
        w, h = template.shape[::-1]
        self.screenshot(screen_name)
        img = cv2.imread(f'data/{screen_name}.png', 0)
        res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        _, max_v, _, top_left = cv2.minMaxLoc(res)
        x = top_left[0] + 0.5 * w
        y = top_left[1] + 0.5 * h
        if check and (max_v < 0.8):
            return False
        else:
            self.click(x, y)
            return True

    def check_angency(self):
        max_v = self.check('utils/config/pic/base/solid.png')['conf']
        if max_v < 0.7:
            self.click(900, 540)

    def check_register(self):
        if self.click_image('utils/config/pic/base/register.png'):
            time.sleep(3)
            self.click_image('utils/config/pic/base/comfirm.png')
            time.sleep(3)
            return True
        else:
            return False
