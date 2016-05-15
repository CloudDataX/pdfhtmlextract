#coding=gbk

__author__ = 'CQC'
# -*- coding:utf-8 -*-
 
import os
from bs4 import BeautifulSoup
#import urllib2
import re
from table import Table
from logger import Logger
import string

class PdfHtmlExtractor(object):
    htmlfile = ''
    soup = ''
    tableList = []   #����ÿҳ���ҵ���
    table1=[0,0]
    table2=[0,0]
    table3=[0,0]
    
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
        
        #Find section start/end page from catalogue
        outline=self.soup.find_all('div',{'id':'outline'})
        for li in outline:
            li_list = li.find_all('li')
            for li in li_list:
                if re.search(sectionName, li.a.get_text()):
                    secondLiList = li.find_all('li')
                    for secondLi in secondLiList:
                        regex = u"���񱨱�"
                        if re.search(regex, secondLi.a.get_text()):
                            print "secondLi",secondLi.encode('utf-8')
                            startPage = secondLi.a['href'][1:]
                            endPage = secondLi.next_sibling.a['href'][1:]
        
        #Get page list between start/end
        pagesContainer=self.soup.find_all('div',id=re.compile("pf"))
        startParse=0
        for page in pagesContainer:
            if(page['id']==startPage):
                startParse=1
            elif (page['id']==endPage):
                startParse=0
                exit
            if(startParse==1):
                pageList.append(page['id'])
        
        self.logger.info("Section:%s, Page list is: %s" % (sectionName, pageList))
        
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
        
        #�ж��Ƿ���ǰ������
        if tmpTable.tableStartIndex < 5:
            myTable.preExtend = 1
        else:
            myTable.preExtend = 0
        if (pageElementNum - tmpTable.tableEndIndex) < 5:
            myTable.aftExtend = 1
        else:
            myTable.aftExtend = 0
            
        #����������
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
        
        #table��Ϣ�����ʱ����
        rowNum = 1            #�����ж����� �� rowIndex
        columnNum = 1         #�����ж�����
        columnIndex = 1       #��¼�е����
        tableStartIndex = 0   #����table��ʼʱ��Ԫ��λ��
        tableEndIndex = 0     #����table����ʱ��Ԫ��λ��
        
        while True:
            if None != pageElement:
                
                #�ҵ�����class C���ж��ǲ���table��ʼ
                if 'c' == pageElement['class'][0] and 'c' == pageElement.previous_sibling['class'][0]:
                    tmpTable = Table(50,20)
                    #�õ�ǰ�и�Ԫ��
                    compareColumnElemnt = self.getCompareColumnElemnt(pageElement, columnNum)
                    
                    self.logger.debug("pageElement= %s, pre-pageElement= %s, compareColumnElemnt= %s" % (pageElement.get_text(), pageElement.previous_sibling.get_text(), compareColumnElemnt.get_text()))                    
                    self.logger.debug("pageElement Y= %s, pre-pageElement Y= %s" % (pageElement['class'][2], pageElement.previous_sibling['class'][2]))
                    self.logger.debug("pageElement X= %s, compareColumnElemnt X= %s" % (pageElement['class'][1], compareColumnElemnt['class'][1]))

                    # ��ǰһ��Ԫ�ص�Y����Ƚ�
                    if pageElement.previous_sibling['class'][2] == pageElement['class'][2]:    
                        columnIndex += 1
                        #��ǰһ��Ԫ�ص�Y�ȣ���ǰ�и�Ԫ�ص� X���� ----��һ��Ԫ��
                        if pageElement['class'][1] != compareColumnElemnt['class'][1]:
                            columnNum = columnIndex
                            # ���tableû��ʼ�����ҵ���һ��1/2cell
                            if tableStartIndex == 0:
                                tableStartIndex = elementIndex
                                self.logger.info("Find a table in page:%s, table start index:%s" % (pageNum, tableStartIndex))
                                
                                # Save cur-cell, pre-cell, tableStartIndex
                                tableSavedFlag = False
                                 
                                tmpTable.tableStartIndex = tableStartIndex
                                tmpTable.setCellValue(rowNum-1, columnIndex-2, pageElement.previous_sibling.get_text())
                                tmpTable.setCellValue(rowNum-1, columnIndex-1, pageElement.get_text())
                               
                                self.logger.debug("Find 1st/2nd cell (rowIndex,columnIndex,value) (%s,%s,%s), (rowIndex,columnIndex,value) (%s,%s,%s)" % (rowNum, columnIndex-1,pageElement.previous_sibling.get_text(),rowNum, columnIndex,pageElement.get_text()))
                            #�ҵ���һ������cell
                            else:
                                tmpTable.setCellValue(rowNum-1, columnIndex-1, pageElement.get_text())
                                self.logger.debug("Find other 1st row cell (rowIndex,columnIndex,value) (%s,%s,%s)" % (rowNum, columnIndex,pageElement.get_text()))
                                # Save cur-cell
                        #��ǰһ��Ԫ�ص�Y�ȣ���ǰ�и�Ԫ�ص� X���----����һ�е�һ�������Ԫ��        
                        else:
                            tmpTable.setCellValue(rowNum-1, columnIndex-1, pageElement.get_text())
                            self.logger.debug("Find Cell row>1,column>1 (rowIndex,columnIndex,value) (%s,%s,%s)" % (rowNum, columnIndex,pageElement.get_text()))
                            
                    else:
                        #��ǰһ��Ԫ�ص�Y���ȣ���ǰ�и�Ԫ�ص�X���----��(1,1)����ĵ�һ��Ԫ��
                        if pageElement['class'][1] == compareColumnElemnt['class'][1]:
                            if tableStartIndex != 0:
                                rowNum += 1
                                columnNum = columnIndex
                                columnIndex = 1
                            self.logger.debug("Find first column cell(rowIndex,columnIndex,value) (%s,%s,%s)" % (rowNum, columnIndex, pageElement.get_text()))
                            tmpTable.setCellValue(rowNum-1, columnIndex-1, pageElement.get_text())                            
                           
                        else:
                            # ��ǰһ��Y���겻�ȣ���ǰ�и�X���겻��----table����
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
                                # ���������tmptable��ر���
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
                        # ���������tmptable��ر���
                        tableStartIndex = 0
                        rowNum = 1
                        columnNum = 1
                        columnIndex = 1
                        tableEndIndex = 0
                        del tmpTable    
            #���������һ��Ԫ�أ�������ѭ��
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
                    # ���������tmptable��ر���
                    tableStartIndex = 0
                    rowNum = 1
                    columnNum = 1
                    columnIndex = 1
                    tableEndIndex = 0
                    del tmpTable   
                break
            
            # ��ȡ��һ��Ԫ��
            pageElement =pageElement.next_sibling
            elementIndex += 1
        
        return True
    
    def getOutLine(self):
        outlines=self.soup.find_all('div',{'id':'outline'})
        outlineIndex = 0
        times = 0
        for outline in outlines:
            if outlineIndex > 1:
                print "Find more than one outline"
                return
            for child in outline.children:
                self.processNode(child, times)
            #print "len(outline)!!!outline.contents", len(outline.contents), outline.contents
            outlineIndex += 1
        print "start-end:",self.table1[0],self.table1[1] ,self.table2[0],self.table2[1],self.table3[0],self.table3[1]
        
    def processNode(self, node, times):
        
        if node.name == "a":
            print "string a",node.string, "times:", times, "href:",string.atoi(node['href'][3:],base=16)
        if node.name == "li":
            for child in node.children:
                if child.name == "a":
                    strTable1 = u"�ϲ��ʲ���ծ��"
                    strTable2 = u"�ϲ������"
                    strTable3 = u"�ϲ��ֽ�������"
                    pageNum=string.atoi(child['href'][3:],base=16)
                    if re.search(strTable1, child.string):
                        self.table1[0]=pageNum
                    elif 0!=self.table1[0] and 0==self.table1[1]:
                        self.table1[1]=pageNum
                    
                    if re.search(strTable2, child.string):
                        self.table2[0]=pageNum
                    elif 0!=self.table2[0] and 0==self.table2[1]:
                        self.table2[1]=pageNum
                        
                    if re.search(strTable3, child.string):
                        self.table3[0]=pageNum
                    elif 0!=self.table3[0] and 0==self.table3[1]:
                        self.table3[1]=pageNum
                        
                    print "string li.a",child.string, "times:", times, "href:",string.atoi(child['href'][3:],base=16)
                if child.name == "ul":
                    self.processNode(child,times)
        if node.name == "ul":
            times += 1
            for child in node.children:
                self.processNode(child,times)
                
    
if __name__ == '__main__':
    pdfhtmlextact = PdfHtmlExtractor('../2014.html')
    pageList = pdfhtmlextact.getSectionStartEndPage(u" ���񱨸�")

    for page in pageList:    
        tableinpage = pdfhtmlextact.getTablesinPage(page)
        
