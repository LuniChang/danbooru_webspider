import requests
import json
import common.path as path
import os
import common.log as log

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
