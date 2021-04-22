# coding=utf-8

import sys
import json
import base64
from pathlib import Path

# 保证兼容python2以及python3
IS_PY3 = sys.version_info.major == 3
if IS_PY3:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import URLError
    from urllib.parse import urlencode
    from urllib.parse import quote_plus
else:
    import urllib2
    from urllib import quote_plus
    from urllib2 import urlopen
    from urllib2 import Request
    from urllib2 import URLError
    from urllib import urlencode

# 防止https证书校验不正确
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from config.baidu_API import API_KEY,SECRET_KEY


OCR_URL = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate"
#OCR_URL =  "https://aip.baidubce.com/rest/2.0/ocr/v1/general"

"""  TOKEN start """
TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'

"""
    获取token
"""
def fetch_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    if (IS_PY3):
        post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req, timeout=5)
        result_str = f.read()
    except URLError as err:
        print(err)
    if (IS_PY3):
        result_str = result_str.decode()


    result = json.loads(result_str)

    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not 'brain_all_scope' in result['scope'].split(' '):
            print ('please ensure has check the  ability')
            exit()
        return result['access_token']
    else:
        print ('please overwrite the correct API_KEY and SECRET_KEY')
        exit()

"""
    读取文件
"""
def read_file(image_path):
    f = None
    try:
        f = open(image_path, 'rb')
        return f.read()
    except:
        print('read image file fail')
        return None
    finally:
        if f:
            f.close()


"""
    调用远程服务
"""
def request(url, data):
    req = Request(url, data.encode('utf-8'))
    has_error = False
    try:
        f = urlopen(req,timeout=10)
        result_str = f.read()
        if (IS_PY3):
            result_str = result_str.decode()
        return result_str
    except  URLError as err:
        print(err)

def detection_image(name,pic='data/screen.png'):
    token_path = Path('config/token.txt')
    if token_path.exists():
        with open(token_path,'r') as handler:
            token = handler.read()
    else:
        token = fetch_token()
        with open(token_path,'w') as handler:
            handler.write(token)
    image_url = OCR_URL + "?access_token=" + token
    file_content = read_file(pic)

    # 调用文字识别服务
    result = request(image_url, urlencode({'image': base64.b64encode(file_content)}))

    #  result_init
    detected = False
    center_x = 0
    center_y = 0
    
    # 解析返回结果
    result_json = json.loads(result)
    if 'error_code' in result_json:
        if result_json["error_msg"] == 'Access token expired':
            token = fetch_token()
            with open(token_path,'w') as handler:
                    handler.write(token)
            print('refresh token')
            detected,center_x,center_y = detection_image(name,pic)
            return detected,center_x,center_y
        else:
            raise Exception(f'{result_json["error_msg"]}')

    for words in result_json['words_result']:
        if name in words['words'].strip() :
            center_x = int(words['location']['left']+0.5*words['location']['width'])
            center_y = int(words['location']['top']+0.5*words['location']['height'])
            detected = True
            break
    return detected,center_x,center_y

if __name__ == '__main__':

    # 获取access token
    token = fetch_token()

    # 拼接通用文字识别高精度url
    image_url = OCR_URL + "?access_token=" + token

    text = "行动记录"

    # 读取书籍页面图片
    file_content = read_file('data/screen.png')

    # 调用文字识别服务
    result = request(image_url, urlencode({'image': base64.b64encode(file_content)}))

    # 解析返回结果
    result_json = json.loads(result)
    for words in result_json['words_result']:
        if words['words'].strip() == 'WR-8':
            center_x = int(words['location']['left']+0.5*words['location']['width'])
            center_y = int(words['location']['top']+0.5*words['location']['height'])
            break

    for words_result in result_json["words_result"]:
        text = text + words_result["words"]

    # 打印文字
    print(text)