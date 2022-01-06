import os
import shutil


def moveImgToDir(imgDir):
  
    for root,dirs,files in os.walk(imgDir):
        count=len(files)
        print("count:"+str(count))
        sum=0
        for file in files: 
          fileNames=file.split('_')
          fileTag=fileNames[2]
          if len(fileTag) == 1:
              fileTag=fileNames[2]+""+fileNames[3]

                    
          tagDirPath=os.path.dirname(imgDir)+"\\order\\"+fileTag+"\\"
          if not os.path.exists(tagDirPath):
            os.makedirs(tagDirPath)    
          try:  
            shutil.move(os.path.join(root,file), tagDirPath)  
          except Exception as e:
               print(e)
          sum=sum+1 
          print("count:"+format(sum/count*100,'.2f'))
    print("finish")

# moveImgToDir("D:\\tensorflow_proj\\danbooru_webspider\\dist\\down")