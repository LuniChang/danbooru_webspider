
import tkinter as tk
import re

from spider.main_spider import MainSpider
import common.path as path
import datetime
import configparser


baseUrl=None
try:
    conf= configparser.RawConfigParser()
    conf.read(path.getConfPath())  # 文件路径
    print(path.getConfPath())
    baseUrl = conf.get("spider", "url") 

except Exception as e:
    print("conf err:"+str(e))

main = tk.Tk()


main.title("d爬虫工具")
main.geometry("600x300")

fm1 = tk.Frame(main)
fm1.pack()


def initJdSpider(pRow):

  
    spider=MainSpider()

    useTag = tk.IntVar()
    useTag.set(1)
    needDown = tk.IntVar()
    needDown.set(1)
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
    def startRun():
        spider.baseUrl=url.get() 
        spider.savePath=savePath.get()
        spider.spider=totalPage.get()
        spider.start()

    
                

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

    tk.Button(fm1, text="启动爬虫", width=10, height=1,
              command=startRun).grid(row=pRow+4, column=1)
    tk.Button(fm1, text="关闭", width=10, height=1,
              command=spider.stop).grid(row=pRow+4, column=2)



initJdSpider(0)


def  initSplitFile(pRow):

    filePath = tk.StringVar()
    rowNum = tk.IntVar()
    rowNum.set(2000)
    def  splitFile():
        path.splitByLineCount(filePath.get(),rowNum.get())

    
    tk.Label(fm1, text="文件切割路径:").grid(row=pRow, column=0)
    tk.Entry(fm1, textvariable=filePath, width=100).grid(row=pRow, column=1,columnspan=4)
    tk.Label(fm1, text="行数:").grid(row=pRow+1, column=0)
    tk.Entry(fm1, textvariable=rowNum, width=20).grid(row=pRow+1, column=1,columnspan=1)


    tk.Button(fm1, text="开始切割", width=10, height=1,
              command=splitFile).grid(row=pRow+4, column=1)



initSplitFile(5)
    

# 进入消息循环
main.mainloop()

main.protocol("WM_DELETE_WINDOW", exit(0))
