# encoding:utf-8

import logging
import common.path as path
import datetime


logging.basicConfig(level=logging.INFO,  # 控制台打印的日志级别
                    filename=path.getLogDirPath()+str(datetime.date.today())+".txt",
                    filemode='a',  # 模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    )


def info(message):
    logging.info(message)


def err(message):
    logging.error(message)


def history(message):

    historyPath = path.getLogDirPath()+"down_history_" + \
        str(datetime.date.today())+".txt"
    f = open(historyPath, "a+")

    f.write(message)
    f.write('\r\n')
    f.close()


def lastUrl(message):

    fPath = path.getLogDirPath()+"lasturl.txt"
    f = open(fPath, "a+")
    f.write('\r\n')
    f.write(message)
    f.close()

def errUrl(message):

    fPath = path.getLogDirPath()+"err_url.txt"
    f = open(fPath, "a+")
    f.write('\r\n')
    f.write(message)
    f.close()

def getLastUrl():

    fPath = path.getLogDirPath()+".txt"
    f = open(fPath)

    res = f.readline()
    f.close()

    return res

