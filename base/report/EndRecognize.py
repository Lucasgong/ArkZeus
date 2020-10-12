# 对最后对结算页面进行识别
from pathlib import Path
import datetime
import cv2
import numpy as np

#from skimage.measure import compare_ssim
from utils.tools.pic import screenshot
from utils.tools.mouse import swipe

def parse_reward(name):
    # 先保存，再读取
    now = datetime.datetime.now()
    date = now.strftime('%Y%m%d') 
    path = Path(f'data/earn/{date}/{name}')
    if not path.exists():
        path.mkdir(parents=True)
    hours = now.strftime('%H_%M_%S')
    path = path/f'{hours}'
    screenshot()
    img = cv2.imread('data/screen.png',3)
    earn = img[484:602,646:,:]  
    cv2.imwrite(str(path)+'.png',earn)
    #item_list = [earn[:,:100,:],earn[:,130:230,:],earn[:,250:,:]]
    #earn = cv2.resize(earn, (0,0),fx=0.5, fy=0.5)


class CompareImage():
    
    def __init__(self):
        pass

    def compare_image(self, path_image1, path_image2):

        imageA = cv2.imread(path_image1)
        imageB = cv2.imread(path_image2)

        grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
        grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

        #(score, diff) = compare_ssim(grayA, grayB, full=True)
        print("SSIM: {}".format(score))
        return score

class EndRecognize():
    def __init__(self,name,dropinfos):
        self.name = name
        self.dropinfos = dropinfos
        self.type_array = np.array([[0, 101, 243],[175,175,175],[53,227,218],[1,103,253],[20,20,20]])
        self.type_list = ['SPECIAL_DROP','NORMAL_DROP','EXTRA_DROP','FURNITURE','NO']

    def read_resource(self):
        items = {}
        for key in self.dropinfos:
            for name,itemcode in self.dropinfos[key]:
                pic = cv2.imread(f'utils/config/pic/items/{name}.png', 0)
                items[name]=[itemcode,pic,key]
        self.items = items

    def find_item(self,pic,item_name):
        pic2 = cv2.resize(pic, (0,0),fx=0.48, fy=0.48)
        res = cv2.matchTemplate(pic2, self.items[item_name][1],cv2.TM_CCOEFF_NORMED)
        _, max_v, _, top_left = cv2.minMaxLoc(res)

    def check_one_pic(self,pic_path):
        pic = cv2.imread(str(pic_path), 0)

    def check(self):
        path = Path('data/earn/20200524/1-7')
        for f in path.glob(pattern='*.png'):
            pass


    @staticmethod
    def parse_reward(name):
        now = datetime.datetime.now()
        date = now.strftime('%Y%m%d') 
        path = Path(f'data/earn/{date}/{name}')
        if not path.exists():
            path.mkdir(parents=True)
        hours = now.strftime('%H_%M_%S')
        path = path/f'{hours}'
        screenshot()
        img = cv2.imread('data/screen.png',3)
        earn = img[484:602,646:994,:]  
        cv2.imwrite(str(path)+'.png',earn)
        item_list = [earn[:,:100,:],earn[:,130:230,:],earn[:,250:,:]]
        #earn = cv2.resize(earn, (0,0),fx=0.5, fy=0.5)
        for i,item in enumerate(item_list):
            cv2.imwrite(str(path)+f'_{i}.png',item) 

    def check_kind(self,array):
        return self.type_list[np.linalg.norm(self.type_array - array,axis=1).argmin()]

    def recognize(self,subpic):
        kind = self.check_kind(subpic[-1,50,:])
        item = subpic[:100,:100,:]
        num = item[68:90,60:85,:]
        item = cv2.resize(item, (0,0),fx=0.48, fy=0.48)