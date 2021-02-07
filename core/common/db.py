import sqlite3
import common.path as path


class DataBase():

    _connect = None

    def __init__(self):
        self.initConnect()

    def initConnect(self, dbPath=None):
        if self._connect != None:
            self._connect.close()
            self._connect = None

        if dbPath == None:
            dbPath = path.getDataBasePath()
        self._connect = sqlite3.connect(dbPath,check_same_thread=False)
        self._iniDataBase()

        return self._connect

    def execute(self, sql):
        if self._connect != None:
            self._connect.execute(sql)

    def _iniDataBase(self):
        try:
            createTableSql = '''
            CREATE TABLE   IF NOT EXISTS URL_DATA
            (
            URL TEXT  PRIMARY KEY ,
            TAG TEXT ,
            CREATE_TIME TIMESTAMP default (datetime('now', 'localtime'))
            )
            '''
            # 主要就是上面的语句
            self._connect.execute(createTableSql)
            self._connect.commit()
        except BaseException as e:
            print("Create table failed："+str(e))

    def insertData(self, url, tag):
        try:
            insertSql = '''
            INSERT INTO URL_DATA  (URL,TAG) VALUES (?,?)
            '''

            self._connect.execute(insertSql, (url, tag))
            self._connect.commit()
            print(insertSql)
        except Exception as e:
            print("insertData err:"+str(e))

    def insertFromFile(self, fPath, tag):
        fin = open(fPath, 'r')
        try:
            for line in fin:
                if line != '\r\n':
                    dbCon.insertData(line, tag)

        finally:
            fin.close()

    def close(self):
        if self._connect != None:
            self._connect.close()
        self._connect = None

    def getData(self, page, pageSize, tag, startDate='', endDate=''):

        result = []

        selectSql = '''
            SELECT URL,TAG,CREATE_TIME FROM URL_DATA 
            WHERE 1=1  
            '''

        if tag!='':
            selectSql +="AND TAG='"+tag+"'"
        if startDate!='':
                selectSql +="AND CREATE_TIME>='"+startDate+"'"    
        if startDate!='':
                selectSql +="AND CREATE_TIME<='"+endDate+"'"           

        if page > 0:
            selectSql += " ORDER BY CREATE_TIME DESC LIMIT "+ (page-1)*pageSize+" offset "+pageSize



        print(selectSql)
        cur = self._connect.cursor()
        result = cur.execute(selectSql).fetchall()

        # if page < 1:
        #     selectSql = '''
        #     SELECT URL,TAG,CREATE_TIME FROM URL_DATA
        #     '''

        #     cur = self._connect.cursor()
        #     result = cur.execute(selectSql).fetchall()

        # elif startDate != '' or endDate != '':
        #     selectSql = '''
        #         SELECT URL,TAG,CREATE_TIME FROM URL_DATA
        #         WHERE TAG=? and CREATE_TIME>=? AND CREATE_TIME<=?
        #         ORDER BY CREATE_TIME DESC LIMIT ? offset ?
        #     '''

        #     cur = self._connect.cursor()
        #     result = cur.execute(
        #         selectSql, (tag, startDate, endDate, (page-1)*pageSize, pageSize)).fetchall()
        # else:

        #     selectSql = '''
        #         SELECT URL,TAG,CREATE_TIME FROM URL_DATA
        #         WHERE 1=1
        #         ORDER BY CREATE_TIME DESC LIMIT ? offset ?
        #     '''
        #     if startDate != '' or endDate != '':

        #     cur = self._connect.cursor()
        #     result = cur.execute(
        #         selectSql, (tag, (page-1)*pageSize, pageSize)).fetchall()

        return result

    def printDataToFile(self, page, pageSize, tag, printPath,startDate, endDate):
        try:

            res = self.getData(page, pageSize, tag,startDate, endDate)
            f = open(printPath, "a+")

            for row in res:
                f.write(row[0])
                f.write('\r\n')
            f.close()
        except Exception as e:
            print("printDataToFile err:"+str(e))


dbCon = DataBase()
