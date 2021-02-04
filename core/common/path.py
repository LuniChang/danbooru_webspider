import os
import sys


def getProjectPath():
    if hasattr(sys, 'frozen'):
        # Handles PyInstaller
        # return os.path.dirname(sys.executable)+"\\"  #使用pyinstaller打包后的exe目录
        return ".\\"
    else:
        project_name = "danbooru_webspider"
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
        project_name = "danbooru_webspider"
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
        project_name = "danbooru_webspider"
        curPath = os.path.abspath(os.path.dirname(__file__))
        rootPath = curPath[:curPath.find(
            project_name+"\\")+len(project_name+"\\")]
        return rootPath+"res\\"


def getLogDirPath():
    if hasattr(sys, 'frozen'):
        # Handles PyInstaller
        # return sys._MEIPASS+"\\res\\"  #使用pyinstaller打包后的exe目录
        dirPath = ".\\log"
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)

        return dirPath+"\\"
    else:
        project_name = "danbooru_webspider"
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
