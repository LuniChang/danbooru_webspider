import os
import sys


project_name = "danbooru_webspider"

def getProjectPath():
    if hasattr(sys, 'frozen'):
        # Handles PyInstaller
        # return os.path.dirname(sys.executable)+"\\"  #使用pyinstaller打包后的exe目录
        return ".\\"
    else:
         
        curPath = os.path.abspath(os.path.dirname(__file__))
        rootPath = curPath[:curPath.find(
            project_name+"\\")+len(project_name+"\\")]
        return rootPath

def getConfPath():
    if hasattr(sys, 'frozen'):
        # Handles PyInstaller
        # return os.path.dirname(sys.executable)+"\\"  #使用pyinstaller打包后的exe目录
        return ".\\user.conf"
    else:
         
        curPath = os.path.abspath(os.path.dirname(__file__))
        rootPath = curPath[:curPath.find(
            project_name+"\\")+len(project_name+"\\")]
        return rootPath+"core\\user.conf"


def getResDirPath():
    if hasattr(sys, 'frozen'):
        # Handles PyInstaller
        # return sys._MEIPASS+"\\res\\"  #使用pyinstaller打包后的exe目录
        return ".\\res\\"
    else:
         
        curPath = os.path.abspath(os.path.dirname(__file__))
        rootPath = curPath[:curPath.find(
            project_name+"\\")+len(project_name+"\\")]
        return rootPath+"res\\"


def getDataBasePath():
    if hasattr(sys, 'frozen'):
            # Handles PyInstaller
        # return sys._MEIPASS+"\\res\\"  #使用pyinstaller打包后的exe目录
        dirPath = ".\\data"
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)

        return dirPath+"\\url_db.db"
    else:
         
        curPath = os.path.abspath(os.path.dirname(__file__))
        rootPath = curPath[:curPath.find(
            project_name+"\\")+len(project_name+"\\")]

        dirPath = rootPath+"data"
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)

        return dirPath+"\\url_db.db"   

def getLogDirPath():
    if hasattr(sys, 'frozen'):
        # Handles PyInstaller
        # return sys._MEIPASS+"\\res\\"  #使用pyinstaller打包后的exe目录
        dirPath = ".\\log"
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)

        return dirPath+"\\"
    else:
         
        curPath = os.path.abspath(os.path.dirname(__file__))
        rootPath = curPath[:curPath.find(
            project_name+"\\")+len(project_name+"\\")]

        dirPath = rootPath+"log"
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)

        return dirPath+"\\"    





def mkSubFile(lines, head, srcName, sub):

    [des_filename, extname] = os.path.splitext(srcName)
    filename = des_filename + '_' + str(sub) + extname
    print('make file: %s' % filename)
    fout = open(filename, 'w')
    try:
            fout.writelines([head])
            fout.writelines(lines)
            return sub + 1
    finally:
            fout.close()


def splitByLineCount(filename, count):
    fin = open(filename, 'r')
    try:
        head = fin.readline()
        buf = []
        sub = 1
        for line in fin:
            buf.append(line)
            if len(buf) == count:
                sub = mkSubFile(buf, head, filename, sub)
                buf = []
        if len(buf) != 0:
            sub = mkSubFile(buf, head, filename, sub)
    finally:
        fin.close()

def checkFileDown(dirPath, downfilePath,outfilePath):
# 把下载文件路径拿出来
    try:
        fin = open(downfilePath, 'r')
        downPaths=[]
        try:
            i=0
            for line in fin:
                if line != '\r\n':
                    i=i+1
                    downPaths.append(line)
                   
            print('=========inFIle===finishi===========')        

        finally:
            fin.close()
        outFile = open(outfilePath, "a+")

  
        for root,dirs,files in os.walk(dirPath):
            count=len(downPaths)
          
            sum=0 
            for downPath in downPaths:
                if len(downPath)>0 and downPath != '\r\n':
                  for file in files: 
                   
                    try:
                        hadnotFile= downPath.index(file) 
                        if hadnotFile >= 0:
                            downPaths.remove(downPath)
                            
                           
                    except ValueError:
                        continue  
                           
      


                sum=sum+1 
                print("count:"+format(sum/count*100,'.2f'))

                 
        print("not down count:"+str(len(downPaths)))
        for downPath in downPaths:
            if len(downPath)>0 and downPath != '\r\n':
               outFile.write(downPath)

            
        outFile.close()
        
        print("finish")
    except Exception as e:
            print("checkFileDown err:"+str(e))