#!/usr/bin/python
# -*- coding: UTF-8 -*-
import MySQLdb
import string
class dataBaseManager():
    conn=''
    cursor=''
    MaxNumberOfFields = 100
    def openDataBase(self):
        # 打开数据连接
        self.conn = MySQLdb.connect("localhost","admin","huyou123",charset='utf8')
        # 使用cursor()方法获取操作游标 
        self.cursor = self.conn.cursor()
        dbName="stockData"
        #cursor.execute("create database %s" % dbName)
        self.cursor.execute('create database if not exists %s' % dbName)
        self.conn.select_db(dbName)
        
    def displayDataBase(self):
        self.cursor.execute("show databases")
        for db in self.cursor.fetchall():
            print db
            
    def createDataTable(self, datas):
        print "createDataTable:",datas[0]
        #sqlStr="create table stock"+datas[0]+ " if not exists " + "id int" 
        sqlStr="create table if not exists stock"+datas[0]
        sqlStr=sqlStr+"(id int(6) not null primary key auto_increment,"+"stockId int,company varchar(100)"
        for i in range(2, len(datas)):
            sqlStr = sqlStr+","+datas[i]+" double"
        sqlStr=sqlStr+")"
        print sqlStr
        #self.cursor.execute(sqlStr)
        
    def insertStockFieldsTable(self, stockId, sheetName, numberFields, FieldsName):
        tableName=stockId+"_"+sheetName+"Fields"
        print "insertStockFieldsTable:",tableName
        
        #create FieldsName table
        sqlStr="create table if not exists "+ tableName + " (id int primary key auto_increment"
        for i in range(0, self.MaxNumberOfFields):
            sqlStr = sqlStr +",field"+ str(i) +" varchar(50) default ''"
        sqlStr=sqlStr+")"
        
        print "step1:createStockFieldsTable sqlStr:",sqlStr
        self.cursor.execute(sqlStr)
        
        #insert record into FieldsName table  [id, FieldNamePrimary,field1,field2.....]
        sqlStr="insert into "+tableName+"("
        FieldsStr=""
        needToInsertDataStr=""
        isFirstValidField = True
        for i in range(0, numberFields):
            if (False == isFirstValidField ) :
                FieldsStr           = FieldsStr + ",field" + str(i)
                needToInsertDataStr = needToInsertDataStr + ",'" + FieldsName[i]+"'"
            else:
                FieldsStr           = "field" + str(i)
                needToInsertDataStr = "'"+FieldsName[i]+"'"
                isFirstValidField = False
        sqlStr = sqlStr + FieldsStr + ")"
        sqlStr = sqlStr + " values(" + needToInsertDataStr + ")"
        print "step2:insertStockFieldsTable sqlStr:",sqlStr
        self.cursor.execute(sqlStr)
        PrimaryKeyIndex = int(self.cursor.lastrowid)
        self.conn.commit()
        print "PrimaryKeyIndex:",str(PrimaryKeyIndex)
        return PrimaryKeyIndex
        
    def insertStockSheetTable(self, stockId, primaryKeyOfFieldsTable, sheetName, numberFields, FieldsValue):
        tableName=stockId+"_"+sheetName
        print "insertStockSheetTable:",tableName
        
        #create sheet table
        sqlStr="create table if not exists "+ tableName + "(id int primary key auto_increment,fieldsIndex int not NULL"
        for i in range(0, self.MaxNumberOfFields):
            sqlStr = sqlStr +",field"+ str(i) +" double default NULL"
        sqlStr=sqlStr+")"
        print "step1:createStockSheetTable sqlStr:",sqlStr
        self.cursor.execute(sqlStr)
        
        #insert record into FieldsValue table  [id, FieldNamePrimary,field1,field2.....]
        sqlStr="insert into "+tableName+"("
        FieldsStr="fieldsIndex"
        needToInsertDataStr=str(primaryKeyOfFieldsTable)
        for i in range(0, numberFields):
            if(None != FieldsValue[i]):
                FieldsStr           = FieldsStr + ",field" + str(i)
                needToInsertDataStr = needToInsertDataStr + "," + str(FieldsValue[i])
        sqlStr = sqlStr + FieldsStr + ")"
        sqlStr = sqlStr + " values(" + needToInsertDataStr + ")"
        print "step2:createStockSheetTable sqlStr:",sqlStr
        self.cursor.execute(sqlStr)
        self.conn.commit()
    def queryStockDataTable(self, stockId, sheetName): 
        tableName=stockId+"_"+sheetName
        fieldTableName=stockId+"_"+sheetName+"Fields"
        sqlstr="select * from "+tableName
        #self.cursor.execute("SET NAMES 'gbk'")
        count=self.cursor.execute(sqlstr)
        print "count:",count
        #重置游标位置，0,为偏移量，mode＝absolute | relative,默认为relative
        self.cursor.scroll(0,mode='absolute')
        #获取所有结果
        results = self.cursor.fetchall()  
        for r in results: 
            fieldIndex = r[1]
            sqlstrOfField="select * from "+fieldTableName+" where id="+str(fieldIndex)
            countFields=self.cursor.execute(sqlstrOfField)
            print "countFields:",countFields
            resultField = self.cursor.fetchone()  
            for i in range(1,100):
                print resultField[i],r[i+1]       

    def insertDataInTable(self, recordsNames, datas):
        print "insertDataInTable:",datas[0]
        sqlStr="insert into stock"+recordsNames[0]+"(stockId"
        for i in range(1, len(recordsNames)):
            sqlStr = sqlStr+","+recordsNames[i]
        sqlStr=sqlStr+")" +" values("+datas[0]
        sqlStr=sqlStr+","+"'"+datas[1]+"'"
        for i in range(2, len(datas)):
            sqlStr = sqlStr+","+datas[i]
        sqlStr=sqlStr+")"
               
        print sqlStr
        self.cursor.execute(sqlStr)

    def displayDataTableRecords(self, stockNum):
        print "displayDataTableRecords:"
        sqlStr="SELECT column_name FROM information_schema.columns WHERE table_name='stock'"
        for field_desc in self.cursor.execute(sqlStr):
            print field_desc
    def closeDataBase(self, conn):
        cursor = conn.cursor()
        cursor.close()
        conn.commit()
        conn.close()

def stringTof(src):
        src = src.replace(',', '')
        if(-1 != src.find('%')):
            src = src.replace('%', '')
            return (string.atof(src)/100)
        return string.atof(src)
#print "aaaaaaaaaaaaaaa:",str(string.atof(aaaaa))
#recordsNames=["600004","company","aaa","bbb","ccc"]
#datas=["600004","ƽ��","111","222","333"]
#dm=dataBaseManager()
#dm.openDataBase()
#dm.displayDataBase()
#dm.createDataTable(recordsNames)
#dm.insertDataInTable(recordsNames, datas)
#dm.displayDataTableRecords(datas[0])
