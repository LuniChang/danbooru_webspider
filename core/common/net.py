import requests
import json
import common.path as path
import os
import common.log as log
from tqdm import tqdm

from urllib.request import urlopen
def postData(url, parameter):
    try:
        print('入参：' + str(parameter))
        # json串数据使用
        parameter = json.dumps(parameter).encode(encoding='utf-8')
        # 普通数据使用
        # parameter = parse.urlencode(parameter).encode(encoding='utf-8')
       

        header_info = {"Content-Type": "application/json"}
        req = requests.post(headers=header_info,url=url, data=parameter )

        print(req.text)
    except BaseException as e:
        print(e)
        

def downUrl(url,dirPath=None):
    urlFile = requests.get(url)

    fileNames=url.split("/")
    fileName=fileNames[len(fileNames)-1]

    if  dirPath==None:
        dirPath= path.getProjectPath()+"down"

    if not os.path.exists(dirPath):
        os.makedirs(dirPath)    

    savePath = dirPath+"\\"+fileName

    if os.path.exists(savePath):
        log.err("had:"+savePath)
        return
    

    print("down:"+url)    
    with open(savePath, "wb") as code:
       code.write(urlFile.content)




def download_from_url(url, dirPath=None):
    if  dirPath==None:
        dirPath= path.getProjectPath()+"down"

    if not os.path.exists(dirPath):
        os.makedirs(dirPath)    
    # 获取文件长度
    try:
        file_size = int(urlopen(url).info().get('Content-Length', -1))
    except Exception as e:
        print(e)
        print("错误，访问url: %s 异常" % url)
        return False

    fileNames=url.split("/")
    fileName=fileNames[len(fileNames)-1]

    savePath = dirPath+"\\"+fileName
    # 文件大小
    if os.path.exists(savePath):
        first_byte = os.path.getsize(savePath)
    else:
        first_byte = 0
    if first_byte >= file_size:
        return file_size

    header = {"Range": "bytes=%s-%s" % (first_byte, file_size)}
    pbar = tqdm(
        total=file_size, initial=first_byte,
        unit='B', unit_scale=True, desc=url.split('/')[-1])

    # 访问url进行下载
    req = requests.get(url, headers=header, stream=True)
    try:
        with(open(savePath, 'ab')) as f:
            for chunk in req.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    pbar.update(1024)
    except Exception as e:
        print(e)
        return False

    pbar.close()
    return True