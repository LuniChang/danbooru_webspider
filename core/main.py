
import tkinter as tk
import re

from spider.main_spider import MainSpider
import common.path as path
import datetime


main = tk.Tk()


main.title("d爬虫工具")
main.geometry("600x200")

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

        if needDown.get() == 1:
           spider.needDown=True
        else:
           spider.needDown=False

    url = tk.StringVar()
    url.set(spider.baseUrl)


    savePath = tk.StringVar()
    savePath.set(path.getProjectPath()+"down\\"+str(datetime.date.today()))

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
                   offvalue=0, command=checkUseTag).grid(row=pRow, column=2)

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



initJdSpider(1)


# print(float(re.search('(\d|(\d*[.]\d*))*斤',"武鸣沃柑 10斤新鲜")[0].replace('斤','')))

# import net
# import config

# param={'price': 6.76, 'srcPrice': '16.90', 'shopName': '果迎鲜官方旗舰店', 'commit': '10000', 'itemName': '第二件9.9元 沃柑 5斤装 广西沃柑\n柑橘\n新鲜水果桔子 广西沃柑 非皇帝柑 武鸣沃柑 送开果器。第二件9.9元 ，买2件合并发货不拆包。因快递超重的原因合发净果9斤以净果为准，广西沃柑礼盒装，过节送礼必备，点此购买'}

# net.postData(config.API_URL+"/api/jdData/add",param)

# 进入消息循环
main.mainloop()

main.protocol("WM_DELETE_WINDOW", exit(0))
