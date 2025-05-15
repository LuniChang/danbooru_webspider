
import tkinter as tk

from spider.main_spider import MainSpider
import common.path as path

import common.imgMove as imgMove
import datetime
import configparser
import tkinter.filedialog as filedialog
from common.db import dbCon

import time
import datetime

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
dbCon.initConnect(dbPath)




main = tk.Tk()


main.title("d爬虫工具")
main.geometry("800x800")




def initJdSpider(paramFrame,bg='#ddd'):

  
    spider=MainSpider()

    useTag = tk.IntVar()
    useTag.set(0)   

    openBs = tk.IntVar()
    openBs.set(1) 
    needDown = tk.IntVar()
    needDown.set(0)

    dataTag=tk.StringVar()
    dataTag.set(confTag)



    def checkUseTag():
        if useTag.get() == 1:
           spider.useTag=True
        else:
           spider.useTag=False
    checkUseTag()

    def checkOpenBs():
        if openBs.get() == 1:
           spider.openBs=True
        else:
           spider.openBs=False
    checkOpenBs()
    def checkNeedDown():
        if needDown.get() == 1:
            spider.needDown=True
        else:
            spider.needDown=False
    checkNeedDown()
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

    def openWebBrowser():
        spider.openWebBrowser()

    def openPage():      
        spider.baseUrl=url.get() 
        spider.savePath=savePath.get()
        spider.totalPage=totalPage.get()
        spider.dataTag=dataTag.get()
        spider.openPage()
    def startRun():
        spider.baseUrl=url.get() 
        spider.savePath=savePath.get()
        spider.totalPage=totalPage.get()
        spider.dataTag=dataTag.get()
        spider.start()
    def selectDbFile():
        dbPath =filedialog.askopenfilename() 
        dbCon.initConnect(dbPath)   
        dbPathShow.set(dbPath)
    
                

    # tk.Checkbutton(paramFrame,bg=bg, text="打开标签模式", variable=useTag, onvalue=1,
    #                offvalue=0, command=checkUseTag).grid(row=0, column=1)

    tk.Checkbutton(paramFrame,bg=bg, text="打开浏览器模式", variable=openBs, onvalue=1,
                   offvalue=0, command=checkOpenBs).grid(row=0, column=1)
    tk.Checkbutton(paramFrame,bg=bg, text="自动下载（很慢）", variable=needDown, onvalue=1,
                   offvalue=0, command=checkNeedDown).grid(row=0, column=2)

    tk.Label(paramFrame,bg=bg, text="url").grid(row=1, column=0)

    tk.Entry(paramFrame,bg=bg, textvariable=url, width=100).grid(row=1, column=1,columnspan=4)

    tk.Label(paramFrame,bg=bg, text="保存路径:").grid(row=2, column=0)

    tk.Entry(paramFrame,bg=bg, textvariable=savePath, width=100).grid(row=2, column=1,columnspan=4)

    tk.Label(paramFrame,bg=bg, text="翻页数量:").grid(row=3, column=0)

    tk.Entry(paramFrame,bg=bg, textvariable=totalPage, width=20).grid(row=3, column=1,columnspan=1)

    tk.Label(paramFrame,bg=bg, text="数据库标签:").grid(row=4, column=0)

    tk.Entry(paramFrame,bg=bg, textvariable=dataTag, width=20).grid(row=4, column=1,columnspan=1)


    tk.Label(paramFrame,bg=bg, text="数据库路径:").grid(row=5, column=0)
    tk.Label(paramFrame,bg=bg, textvariable=dbPathShow).grid(row=5, column=1)
    tk.Button(paramFrame,bg=bg, text="选择数据库", width=10, height=1,
              command=selectDbFile).grid(row=5, column=2)

    
    tk.Button(paramFrame,bg=bg, text="打开浏览器", width=10, height=1,
              command=openWebBrowser).grid(row=6, column=1)
    tk.Button(paramFrame,bg=bg, text="链接浏览器", width=10, height=1,
              command=openPage).grid(row=6, column=2)

    tk.Button(paramFrame,bg=bg, text="启动爬虫", width=10, height=1,
              command=startRun).grid(row=6, column=3)
    tk.Button(paramFrame,bg=bg, text="关闭", width=10, height=1,
              command=spider.stop).grid(row=6, column=4)


fm1 = tk.Frame(main,bg='#ddd')
fm1.grid(row=0, column=0)
initJdSpider(fm1)





def  initDataBase(paramFrame,bg='#ddd'):
    
    infilePath = tk.StringVar()
    outfilePath = tk.StringVar()

    outfilePath.set( path.getLogDirPath() +'export_' +  time.strftime("%Y-%m-%d", time.localtime())+'.txt')
    page = tk.IntVar()
    page.set(0)
    rowNum = tk.IntVar()
    rowNum.set(2000)

    dataTag=tk.StringVar()
    dataTag.set(confTag)

    endDate=tk.StringVar()
   

    startDate=tk.StringVar()
    threeDayAgo = (datetime.datetime.now() - datetime.timedelta(days = 2))
    twoDayLater = (datetime.datetime.now() + datetime.timedelta(days = 2))
    # 转换为时间戳
    timeStamp = int(time.mktime(threeDayAgo.timetuple()))
    # 转换为其他字符串格式
    otherStyleTime = threeDayAgo.strftime("%Y-%m-%d")
    startDate.set(otherStyleTime)
    timeStamp = int(time.mktime(twoDayLater.timetuple()))

    endDate.set(twoDayLater.strftime("%Y-%m-%d"))

    def selectInFile():
        tmpPath =filedialog.askopenfilename()    
        infilePath.set(tmpPath)

    def selectOutFile():
        tmpPath =filedialog.askopenfilename()    
        outfilePath.set(tmpPath) 


    def insertDatas():     
        dbCon.insertFromFile(infilePath.get(),dataTag.get())  
        msgbox.showinfo("提示","导入完成")

    def prinOutDatas():     
        dbCon.printDataToFile(page.get(),rowNum.get(),dataTag.get(),outfilePath.get(),startDate=startDate.get(),endDate=endDate.get())
        msgbox.showinfo("提示","出完成")
    
    
    tk.Label(paramFrame,bg=bg, text="导入数据文件路径:").grid(row=0, column=0)
    tk.Entry(paramFrame,bg=bg, textvariable=infilePath, width=100).grid(row=1, column=1,columnspan=4)
    tk.Button(paramFrame,bg=bg, text="选择文件", width=10, height=1,
              command=selectInFile).grid(row=2, column=1)
    tk.Button(paramFrame,bg=bg, text="导入", width=10, height=1,
              command=insertDatas).grid(row=2, column=2)

    tk.Label(paramFrame,bg=bg, text="").grid(row=3, column=0)
    tk.Label(paramFrame,bg=bg, text="页数(0不分页):").grid(row=4, column=0)
    tk.Entry(paramFrame,bg=bg, textvariable=page, width=20).grid(row=4, column=1,columnspan=1)

    tk.Label(paramFrame,bg=bg, text="行数:").grid(row=4, column=2)
    tk.Entry(paramFrame,bg=bg, textvariable=rowNum, width=20).grid(row=4, column=3,columnspan=1)

    tk.Label(paramFrame,bg=bg, text="标签:").grid(row=5, column=0)
    tk.Entry(paramFrame,bg=bg, textvariable=dataTag, width=20).grid(row=5, column=1,columnspan=1)

    tk.Label(paramFrame,bg=bg, text="开始时间:").grid(row=6, column=0)
    tk.Entry(paramFrame,bg=bg, textvariable=startDate, width=20).grid(row=6, column=1,columnspan=1)

    tk.Label(paramFrame,bg=bg, text="结束时间:").grid(row=6, column=2)
    tk.Entry(paramFrame,bg=bg, textvariable=endDate, width=20).grid(row=6, column=3,columnspan=1)

    tk.Label(paramFrame,bg=bg, text="导出数据文件路径:").grid(row=7, column=0)
    tk.Entry(paramFrame,bg=bg, textvariable=outfilePath, width=100).grid(row=8, column=1,columnspan=4)
    tk.Button(paramFrame,bg=bg, text="选择文件", width=10, height=1,
              command=selectOutFile).grid(row=9, column=1)
    tk.Button(paramFrame,bg=bg, text="导出", width=10, height=1,
              command=prinOutDatas).grid(row=9, column=2)


fm2 = tk.Frame(main,bg='#fff')
fm2.grid(row=1, column=0)
initDataBase(fm2,'#fff')




def  initSplitFile(paramFrame,bg='#ddd'):

    filePath = tk.StringVar()
    rowNum = tk.IntVar()
    rowNum.set(2000)
    def  splitFile():
        path.splitByLineCount(filePath.get(),rowNum.get())

    def selectFile():
        tmpPath =filedialog.askopenfilename()    
        filePath.set(tmpPath)

    
    tk.Label(paramFrame,bg=bg, text="文件切割路径:").grid(row=0, column=0)

    tk.Entry(paramFrame,bg=bg, textvariable=filePath, width=100).grid(row=0, column=1,columnspan=4)

    tk.Button(paramFrame,bg=bg, text="选择文件", width=10, height=1,
              command=selectFile).grid(row=1, column=1)


    tk.Label(paramFrame,bg=bg, text="行数:").grid(row=1, column=0)
    tk.Entry(paramFrame,bg=bg, textvariable=rowNum, width=20).grid(row=2, column=1,columnspan=1)


    tk.Button(paramFrame,bg=bg, text="开始切割", width=10, height=1,
              command=splitFile).grid(row=3, column=1)


fm3 = tk.Frame(main,bg='#ddd')
fm3.grid(row=2, column=0)
initSplitFile(fm3)






def  initOrderImg(paramFrame,bg='#fff'):

    filePath = tk.StringVar()

  

    def selectFile():
        tmpPath =filedialog.askdirectory()    
        filePath.set(tmpPath)
    def orderFile():
        if filePath.get() == "" or filePath.get() is None:
            msgbox.showinfo("提示","未选择文件夹")
        else:    
          imgMove.moveImgToDir(filePath.get())
          msgbox.showinfo("提示","整理完成")
    
    tk.Label(paramFrame,bg=bg, text="整理文件夹路径:").grid(row=0, column=0)

    tk.Entry(paramFrame,bg=bg, textvariable=filePath, width=100).grid(row=0, column=1,columnspan=4)

    tk.Button(paramFrame,bg=bg, text="选择文件夹", width=10, height=1,
              command=selectFile).grid(row=1, column=1)


 
    tk.Button(paramFrame,bg=bg, text="开始", width=10, height=1,
              command=orderFile).grid(row=3, column=1)


fm4 = tk.Frame(main,bg='#fff')
fm4.grid(row=3, column=0)
initOrderImg(fm4)




def  initCheckFile(paramFrame,bg='#ddd'):
    dirPath = tk.StringVar()
    downfilePath = tk.StringVar()
    outfilePath = tk.StringVar()

    def checkFile():
        path.checkFileDown(dirPath.get(),downfilePath.get(),outfilePath.get())

    def selectDirFile():
        tmpPath =filedialog.askdirectory()    
        dirPath.set(tmpPath)
    def selectDownFile():
        tmpPath =filedialog.askopenfilename()    
        downfilePath.set(tmpPath)
    def selectOutFile():
        tmpPath =filedialog.askopenfilename()    
        outfilePath.set(tmpPath)
    
    tk.Label(paramFrame,bg=bg, text="已下载文件夹检查路径:").grid(row=0, column=0)

    tk.Entry(paramFrame,bg=bg, textvariable=dirPath, width=100).grid(row=0, column=1,columnspan=4)

    tk.Button(paramFrame,bg=bg, text="选择文件夹", width=10, height=1,
              command=selectDirFile).grid(row=2, column=1)


       
    tk.Label(paramFrame,bg=bg, text="下载文件列表:").grid(row=3, column=0)

    tk.Entry(paramFrame,bg=bg, textvariable=downfilePath, width=100).grid(row=3, column=1,columnspan=4)

    tk.Button(paramFrame,bg=bg, text="选择文件", width=10, height=1,
              command=selectDownFile).grid(row=4, column=1)
    
    tk.Label(paramFrame,bg=bg, text="输出检查路径:").grid(row=5, column=0)

    tk.Entry(paramFrame,bg=bg, textvariable=outfilePath, width=100).grid(row=5, column=1,columnspan=4)

    tk.Button(paramFrame,bg=bg, text="选择文件", width=10, height=1,
              command=selectOutFile).grid(row=6, column=1)

    tk.Button(paramFrame,bg=bg, text="开始检查", width=10, height=1,
              command=checkFile).grid(row=7, column=1)


fm4 = tk.Frame(main,bg='#ddd')
fm4.grid(row=4, column=0)
initCheckFile(fm4)

# 进入消息循环
main.mainloop()

dbCon.close()

main.protocol("WM_DELETE_WINDOW", exit(0))
