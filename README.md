<!--
 * @Author: zgong
 * @Date: 2020-05-17 15:00:18
 * @LastEditors: zgong
 * @LastEditTime: 2021-01-19 00:20:45
-->
For game "Arknights" ,instead of watching video games over and over again, use this automated tool to manage your "reason".

Enjoying your game and life :)

## how to use
1. install adb

## how to add new stage
修改setting utils/config/setting.py
增加新关卡：
    1. 增加图片 utils/config/pic/stage_pic
    2. 到达关卡方式 utils/config/stage.py
    3. 关卡完成时间 utils/config/stage.py

## 
1. 关卡结束判断
2. 增加滚动到边缘判定
3. 滚动翻页的 robust 实现

## 下一步计划
1. 优化判断单局游戏结束的办法 读取行动结束
2. 不用opencv库，换别的库
