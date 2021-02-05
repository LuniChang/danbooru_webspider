
import tkinter as tk
import re

from spider.main_spider import MainSpider
import common.path as path
import datetime
import configparser
import tkinter.filedialog as filedialog
from common.db import dbCon

import tkinter.messagebox as msgbox

baseUrl=None
dbPath=path.getDataBasePath()
confTag=""
try:
    conf= configparser.RawConfigParser()
    conf.read(path.getConfPath())  # 文件路径
    print(path.getConfPath())
    baseUrl = conf.get("spider", "url") 
    confTag = conf.get("spider", "tag") 
    dbPath = conf.get("spider", "dbpath") 
except Exception as e:
    print("conf err:"+str(e))





main = tk.Tk()


main.title("d爬虫工具")
main.geometry("800x600")

fm1 = tk.Frame(main)
fm1.pack()


def initJdSpider(pRow):

  
    spider=MainSpider()

    useTag = tk.IntVar()
    useTag.set(1)
    needDown = tk.IntVar()
    needDown.set(1)

    dataTag=tk.StringVar()
    dataTag.set(confTag)


    def checkUseTag():
        if useTag.get() == 1:
           spider.useTag=True
        else:
           spider.useTag=False
    def checkNeedDown():
        if needDown.get() == 1:
            spider.needDown=True
        else:
            spider.needDown=False

    url = tk.StringVar()

    if baseUrl == None:
       url.set(spider.baseUrl)
    else:
       url.set(baseUrl)

    savePath = tk.StringVar()
    savePath.set(path.getProjectPath()+"down\\down_list_"+str(datetime.date.today()))

    totalPage = tk.IntVar()
    totalPage.set(spider.totalPage)
    
    dbPathShow=tk.StringVar()
    dbPathShow.set(dbPath)
    def startRun():
        spider.baseUrl=url.get() 
        spider.savePath=savePath.get()
        spider.spider=totalPage.get()
        spider.dataTag=dataTag.get()
        spider.start()
    def selectDbFile():
        dbPath =filedialog.askopenfilename() 
        dbCon.initConnect(dbPath)   
        dbPathShow.set(dbPath)
    
                

    tk.Checkbutton(fm1, text="打开标签模式", variable=useTag, onvalue=1,
                   offvalue=0, command=checkUseTag).grid(row=pRow, column=1)


    tk.Checkbutton(fm1, text="自动下载（很慢）", variable=needDown, onvalue=1,
                   offvalue=0, command=checkNeedDown).grid(row=pRow, column=2)

    tk.Label(fm1, text="url").grid(row=pRow+1, column=0)

    tk.Entry(fm1, textvariable=url, width=100).grid(row=pRow+1, column=1,columnspan=4)

    tk.Label(fm1, text="保存路径:").grid(row=pRow+2, column=0)

    tk.Entry(fm1, textvariable=savePath, width=100).grid(row=pRow+2, column=1,columnspan=4)

    tk.Label(fm1, text="翻页数量:").grid(row=pRow+3, column=0)

    tk.Entry(fm1, textvariable=totalPage, width=20).grid(row=pRow+3, column=1,columnspan=1)

    tk.Label(fm1, text="数据库标签:").grid(row=pRow+4, column=0)

    tk.Entry(fm1, textvariable=dataTag, width=20).grid(row=pRow+4, column=1,columnspan=1)


    tk.Label(fm1, text="数据库路径:").grid(row=pRow+5, column=0)
    tk.Label(fm1, textvariable=dbPathShow).grid(row=pRow+5, column=1)
    tk.Button(fm1, text="选择数据库", width=10, height=1,
              command=selectDbFile).grid(row=pRow+5, column=2)




    tk.Button(fm1, text="启动爬虫", width=10, height=1,
              command=startRun).grid(row=pRow+6, column=1)
    tk.Button(fm1, text="关闭", width=10, height=1,
              command=spider.stop).grid(row=pRow+6, column=2)



initJdSpider(0)





def  initDataBase(pRow):
    
    infilePath = tk.StringVar()
    outfilePath = tk.StringVar()

    page = tk.IntVar()
    page.set(1)
    rowNum = tk.IntVar()
    rowNum.set(2000)

    dataTag=tk.StringVar()
    dataTag.set(confTag);

    def selectInFile():
        tmpPath =filedialog.askopenfilename()    
        infilePath.set(tmpPath)

    def selectOutFile():
        tmpPath =filedialog.askopenfilename()    
        outfilePath.set(tmpPath) 


    def insertDatas():     
        dbCon.insertFromFile(infilePath.get(),dataTag.get())  
        msgbox.showinfo("提示","导入完成")
    
    

    tk.Label(fm1, text="导入数据文件路径:").grid(row=pRow, column=0)
    tk.Entry(fm1, textvariable=infilePath, width=100).grid(row=pRow+1, column=1,columnspan=4)
    tk.Button(fm1, text="选择文件", width=10, height=1,
              command=selectInFile).grid(row=pRow+2, column=1)
    tk.Button(fm1, text="导入", width=10, height=1,
              command=insertDatas).grid(row=pRow+2, column=2)


    tk.Label(fm1, text="页数:").grid(row=pRow+3, column=0)
    tk.Entry(fm1, textvariable=rowNum, width=20).grid(row=pRow+3, column=1,columnspan=1)
    tk.Label(fm1, text="行数:").grid(row=pRow+3, column=2)
    tk.Entry(fm1, textvariable=rowNum, width=20).grid(row=pRow+3, column=3,columnspan=1)
    tk.Label(fm1, text="标签:").grid(row=pRow+4, column=0)
    tk.Entry(fm1, textvariable=dataTag, width=20).grid(row=pRow+4, column=1,columnspan=1)
    tk.Label(fm1, text="导出数据文件路径:").grid(row=pRow+5, column=0)
    tk.Entry(fm1, textvariable=infilePath, width=100).grid(row=pRow+6, column=1,columnspan=4)
    tk.Button(fm1, text="选择文件", width=10, height=1,
              command=selectInFile).grid(row=pRow+7, column=1)
    # tk.Button(fm1, text="导出", width=10, height=1,
    #           command=splitFile).grid(row=pRow+6 column=1)



initDataBase(15)




def  initSplitFile(pRow):

    filePath = tk.StringVar()
    rowNum = tk.IntVar()
    rowNum.set(2000)
    def  splitFile():
        path.splitByLineCount(filePath.get(),rowNum.get())

    def selectFile():
        tmpPath =filedialog.askopenfilename()    
        filePath.set(tmpPath)

    
    tk.Label(fm1, text="文件切割路径:").grid(row=pRow, column=0)

    tk.Entry(fm1, textvariable=filePath, width=100).grid(row=pRow, column=1,columnspan=4)

    tk.Button(fm1, text="选择文件", width=10, height=1,
              command=selectFile).grid(row=pRow+1, column=1)


    tk.Label(fm1, text="行数:").grid(row=pRow+1, column=0)
    tk.Entry(fm1, textvariable=rowNum, width=20).grid(row=pRow+2, column=1,columnspan=1)


    tk.Button(fm1, text="开始切割", width=10, height=1,
              command=splitFile).grid(row=pRow+3, column=1)



initSplitFile(30)


# 进入消息循环
main.mainloop()

dbCon.close()

main.protocol("WM_DELETE_WINDOW", exit(0))
