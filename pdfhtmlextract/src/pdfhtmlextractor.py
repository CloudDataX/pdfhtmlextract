#coding=gbk

__author__ = 'CQC'
# -*- coding:utf-8 -*-
 
import os
from bs4 import BeautifulSoup
#import urllib2
import re
from table import Table
from logger import Logger

class PdfHtmlExtractor(object):
    htmlfile = ''
    soup = ''
    tableList = []   #保存每页中找到的
    
    def __init__(self, htmlfile):
        
        htmlfilelog = htmlfile + '.log'
        if os.path.exists(htmlfilelog):
            os.remove(htmlfilelog)
        self.logger = Logger(logname=htmlfilelog, loglevel="INFO", logger=__name__).getlogger()
        self.logger.info("Begin extract: %s" % htmlfile)
        
        self.htmlfile = htmlfile
        self.soup = BeautifulSoup(open(self.htmlfile), "html.parser")
        
    def getSectionStartEndPage(self,sectionName):
        
        pageList = []
        startPage = ''
        endPage = ''
        
        if sectionName == None:
            self.logger.error("sectionName is None")
            return None
        
        self.logger.info("Begin find Page range of section: %s" % sectionName)
        
        outline=self.soup.find_all('div',{'id':'outline'})

        for li in outline:
            li_list = li.find_all('li')
            for li in li_list:
                if re.search(sectionName, li.a.get_text()):
                    startPage = li.a['href'][1:]
                    endPage = li.next_sibling.a['href'][1:]
        
        PageContainer = self.soup.find_all('div',{'id':'page-container'})
        
        if PageContainer[0].div['id'] == startPage:
            
        nextPageContent = startPageContent[0]
        print nextPageContent['id'], nextPageContent.next_sibling['id']
        nextPage = nextPageContent['id']
        
        while nextPage != endPage and nextPageContent != None:
            print "!!",nextPageContent['id']
            pageList.append(nextPageContent['id'])
            nextPageContent = nextPageContent.next_sibling
            nextPage = nextPageContent['id']
            
        print "pageList is:",pageList
        
        self.logger.info("Scetion:%s, Page list is: %s" % (sectionName, pageList))
        
        return pageList
    
    def getPageContent(self,pageNum):
        
        pageContentList = self.soup.find_all('div',{'id':pageNum}) 
        if  1 == len(pageContentList):
            return pageContentList[0]
        elif 1 < len(pageContentList):
            self.logger.error("Find two same pageNum: %s" % pageNum)
        else:
            self.logger.error("pageLen=", len(pageContentList))            
        return None

    def saveTable(self, tmpTable, rowNum, columnNum, pageElementNum):
        myTable = Table(rowNum,columnNum)
        myTable.tableStartIndex = tmpTable.tableStartIndex
        myTable.tableEndIndex = tmpTable.tableEndIndex
        myTable.rowNum = rowNum
        myTable.columnNum = columnNum
        myTable.pageNum = tmpTable.pageNum
        
        #判断是否有前后续表
        if tmpTable.tableStartIndex < 5:
            myTable.preExtend = 1
        else:
            myTable.preExtend = 0
        if (pageElementNum - tmpTable.tableEndIndex) < 5:
            myTable.aftExtend = 1
        else:
            myTable.aftExtend = 0
            
        #保存表格内容
        for row in range(0,rowNum):
            for column in range(0,columnNum):
                myTable.setCellValue(row, column, tmpTable.getCellValue(row,column))
                self.logger.debug("Save cell (row, column, tmpTablevalue, myTablevalue) (%s, %s, %s ,%s)" % (row, column, tmpTable.getCellValue(row,column), myTable.getCellValue(row, column)))
                 
        self.tableList.append(myTable)

        return
        
    def getPageTotalElementNum(self,pageNum):
        pageElementNum = 0
        
        pageContent = self.getPageContent(pageNum)
        if pageContent == None:
            self.logger.error("Get page content None")
            return None
        pageElement = pageContent.div.div
        
        while True:
            if None != pageElement:
                pageElement =pageElement.next_sibling
                pageElementNum += 1
            else:
                break
        self.logger.info("Page:%s. Total element Num:%s" % (pageNum, pageElementNum))
        return pageElementNum    
     
    def getCompareColumnElemnt(self, pageElement, columnNum):
        if columnNum == 1:
            compareColumnElemnt = pageElement.previous_sibling
        if columnNum == 2:
            compareColumnElemnt = pageElement.previous_sibling.previous_sibling
        if columnNum == 3:
            compareColumnElemnt = pageElement.previous_sibling.previous_sibling.previous_sibling
        if columnNum == 4:
            compareColumnElemnt = pageElement.previous_sibling.previous_sibling.previous_sibling.previous_sibling
        if columnNum == 5:
            compareColumnElemnt = pageElement.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling
        if columnNum == 6:
            compareColumnElemnt = pageElement.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling
        if columnNum == 7:
            compareColumnElemnt = pageElement.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling
        if columnNum == 8:
            compareColumnElemnt = pageElement.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling
        if columnNum == 9:
            compareColumnElemnt = pageElement.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling
        if columnNum == 10:
            compareColumnElemnt = pageElement.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling
        if columnNum == 11:
            compareColumnElemnt = pageElement.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling
        if columnNum == 12:
            compareColumnElemnt = pageElement.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling
        return compareColumnElemnt
    
    def getTablesinPage(self, pageNum):
        
        pageContent = self.getPageContent(pageNum)
        if pageContent == None:
            self.logger.error("Get page content None")
            return None
        
        pageElement = pageContent.div.div
        pageElementNum =  self.getPageTotalElementNum(pageNum)
        elementIndex = 0
        
        #table信息相关临时标量
        rowNum = 1            #保存有多少行 兼 rowIndex
        columnNum = 1         #保存有多少列
        columnIndex = 1       #记录列的序号
        tableStartIndex = 0   #保存table开始时的元素位置
        tableEndIndex = 0     #保存table结束时的元素位置
        
        while True:
            if None != pageElement:
                
                #找到连续class C，判断是不是table开始
                if 'c' == pageElement['class'][0] and 'c' == pageElement.previous_sibling['class'][0]:
                    tmpTable = Table(50,20)
                    #得到前列个元素
                    compareColumnElemnt = self.getCompareColumnElemnt(pageElement, columnNum)
                    
                    self.logger.debug("pageElement= %s, pre-pageElement= %s, compareColumnElemnt= %s" % (pageElement.get_text(), pageElement.previous_sibling.get_text(), compareColumnElemnt.get_text()))                    
                    self.logger.debug("pageElement Y= %s, pre-pageElement Y= %s" % (pageElement['class'][2], pageElement.previous_sibling['class'][2]))
                    self.logger.debug("pageElement X= %s, compareColumnElemnt X= %s" % (pageElement['class'][1], compareColumnElemnt['class'][1]))

                    # 与前一个元素的Y坐标比较
                    if pageElement.previous_sibling['class'][2] == pageElement['class'][2]:    
                        columnIndex += 1
                        #与前一个元素的Y等，与前列个元素的 X不等 ----第一行元素
                        if pageElement['class'][1] != compareColumnElemnt['class'][1]:
                            columnNum = columnIndex
                            # 如果table没开始，则找到第一个1/2cell
                            if tableStartIndex == 0:
                                tableStartIndex = elementIndex
                                self.logger.info("Find a table in page:%s, table start index:%s" % (pageNum, tableStartIndex))
                                
                                # Save cur-cell, pre-cell, tableStartIndex
                                tableSavedFlag = False
                                 
                                tmpTable.tableStartIndex = tableStartIndex
                                tmpTable.setCellValue(rowNum-1, columnIndex-2, pageElement.previous_sibling.get_text())
                                tmpTable.setCellValue(rowNum-1, columnIndex-1, pageElement.get_text())
                               
                                self.logger.debug("Find 1st/2nd cell (rowIndex,columnIndex,value) (%s,%s,%s), (rowIndex,columnIndex,value) (%s,%s,%s)" % (rowNum, columnIndex-1,pageElement.previous_sibling.get_text(),rowNum, columnIndex,pageElement.get_text()))
                            #找到第一行其他cell
                            else:
                                tmpTable.setCellValue(rowNum-1, columnIndex-1, pageElement.get_text())
                                self.logger.debug("Find other 1st row cell (rowIndex,columnIndex,value) (%s,%s,%s)" % (rowNum, columnIndex,pageElement.get_text()))
                                # Save cur-cell
                        #与前一个元素的Y等，与前列个元素的 X相等----除第一行第一列以外的元素        
                        else:
                            tmpTable.setCellValue(rowNum-1, columnIndex-1, pageElement.get_text())
                            self.logger.debug("Find Cell row>1,column>1 (rowIndex,columnIndex,value) (%s,%s,%s)" % (rowNum, columnIndex,pageElement.get_text()))
                            
                    else:
                        #与前一个元素的Y不等，与前列个元素的X相等----除(1,1)以外的第一列元素
                        if pageElement['class'][1] == compareColumnElemnt['class'][1]:
                            if tableStartIndex != 0:
                                rowNum += 1
                                columnNum = columnIndex
                                columnIndex = 1
                            self.logger.debug("Find first column cell(rowIndex,columnIndex,value) (%s,%s,%s)" % (rowNum, columnIndex, pageElement.get_text()))
                            tmpTable.setCellValue(rowNum-1, columnIndex-1, pageElement.get_text())                            
                           
                        else:
                            # 与前一个Y坐标不等，与前列个X坐标不等----table结束
                            if tableStartIndex != 0:
                                tableEndIndex = elementIndex
                                self.logger.info("Table is ended due to Y!=,X!= with info(rowNum,columnNum,tableEndIndex,content) (%s,%s,%s,%s)" % (rowNum, columnIndex, tableEndIndex, pageElement.get_text()))
                                #Save tableEndIndex, rowNum, columnNum append tableList
                                if tableSavedFlag == False and rowNum >= 1 and columnNum > 1:
                                    tmpTable.tableEndIndex = tableEndIndex
                                    tmpTable.rowNum = rowNum
                                    tmpTable.columnNum = columnNum
                                    self.saveTable(tmpTable,rowNum,columnNum,pageElementNum)
                                    tableSavedFlag = True
                                # 结束表清空tmptable相关变量
                                tableStartIndex = 0
                                rowNum = 1
                                columnNum = 1
                                columnIndex = 1
                                tableEndIndex = 0
                                del tmpTable    
                                
                elif 't' == pageElement['class'][0]:
                    if tableStartIndex != 0:
                        tableEndIndex = elementIndex
                        self.logger.info("Table is ended due to find a class t info(rowNum,columnNum,tableEndIndex) (%s,%s,%s)" % (rowNum, columnIndex, tableEndIndex))
                        #Save tableEndIndex, rowNum, columnNum
                        if tableSavedFlag == False and rowNum >= 1 and columnNum > 1:
                            tmpTable.tableEndIndex = tableEndIndex
                            tmpTable.rowNum = rowNum
                            tmpTable.columnNum = columnNum
                            self.saveTable(tmpTable,rowNum,columnNum,pageElementNum)
                            tableSavedFlag = True
                        # 结束表清空tmptable相关变量
                        tableStartIndex = 0
                        rowNum = 1
                        columnNum = 1
                        columnIndex = 1
                        tableEndIndex = 0
                        del tmpTable    
            #检索完最后一个元素，跳出死循环
            else:
                if tableStartIndex != 0:
                    tableEndIndex = elementIndex
                    self.logger.info("Table is ended due to last element info(rowNum,columnNum,tableEndIndex) (%s,%s,%s)" % (rowNum, columnIndex, tableEndIndex))
                    #Save tableEndIndex, rowNum, columnNum
                    if tableSavedFlag == False and rowNum >= 1 and columnNum > 1:
                        tmpTable.tableEndIndex = tableEndIndex
                        tmpTable.rowNum = rowNum
                        tmpTable.columnNum = columnNum
                        self.saveTable(tmpTable,rowNum,columnNum,pageElementNum)
                        tableSavedFlag = True
                    self.logger.info("Page %s fetch end" % pageNum)
                    # 结束表清空tmptable相关变量
                    tableStartIndex = 0
                    rowNum = 1
                    columnNum = 1
                    columnIndex = 1
                    tableEndIndex = 0
                    del tmpTable   
                break
            
            # 获取下一个元素
            pageElement =pageElement.next_sibling
            elementIndex += 1
        
        return True
        
if __name__ == '__main__':
    pdfhtmlextact = PdfHtmlExtractor('../2014.html')
    pageList = pdfhtmlextact.getSectionStartEndPage(u" 财务报告")

    for page in pageList:    
        tableinpage = pdfhtmlextact.getTablesinPage(page)
        
