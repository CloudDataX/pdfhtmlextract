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
    tableList = []
    
    def __init__(self, htmlfile):
        
        htmlfilelog = htmlfile + '.log'
        if os.path.exists(htmlfilelog):
            os.remove(htmlfilelog)
        self.logger = Logger(logname=htmlfilelog, loglevel="DEBUG", logger=__name__).getlogger()
        self.logger.info("Begin extract: %s" % htmlfile)
        
        self.htmlfile = htmlfile
        self.soup = BeautifulSoup(open(self.htmlfile), "html.parser")
        
    def getSectionStartEndPage(self,sectionName):
        
        pageRange = []
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
        
        pageRange.append(startPage)
        pageRange.append(endPage)
        
        self.logger.debug("Page range is (%s, %s, %s)" % (sectionName, startPage, endPage))
        return pageRange
    
    def getPageContent(self,pageNum):
        pageContentList = self.soup.find_all('div',{'id':pageNum})
        pageLen = len(pageContentList)
        
        if  1 == pageLen:
            return pageContentList[0]
        elif 1 < pageLen:
            self.logger.error("Find two same pageNum: %s" % pageNum)
        else:
            self.logger.error("pageLen=", pageLen)            
        return None

    
    def getTablesinPage(self, pageNum):
        
        pageContent = self.getPageContent(pageNum)
        if pageContent == None:
            self.logger.error("Get page content None")
            return None
        
        pageElement = pageContent.div.div
        elementIndex = 0
        totalElemet = 0
        rowNum = 1            #�����ж�����
        columnNum = 1         #�����ж�����
        columnIndex = 1       #��¼�е����
        tableStartIndex = 0   #����table��ʼʱ��Ԫ��λ��
        tableEndIndex = 0     #����table����ʱ��Ԫ��λ��
        
        while True:
            if None != pageElement:
                
                #�ҵ�����class C���ж��ǲ���table��ʼ
                if 'c' == pageElement['class'][0] and 'c' == pageElement.previous_sibling['class'][0]:
                    
                    #�õ�ǰ�и�Ԫ��
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
                                tmpTable = Table(30,5) 
                                tmpTable.tableStartIndex = tableStartIndex
                                tmpTable.setCellValue(rowNum, columnIndex-1, pageElement.previous_sibling.get_text())
                                tmpTable.setCellValue(rowNum, columnIndex, pageElement.get_text())
                               
                                self.logger.debug("Find 1st/2nd cell (rowIndex,columnIndex,value) (%s,%s,%s), (rowIndex,columnIndex,value) (%s,%s,%s)" % (rowNum, columnIndex-1,pageElement.previous_sibling.get_text(),rowNum, columnIndex,pageElement.get_text()))
                            #�ҵ���һ������cell
                            else:
                                tmpTable.setCellValue(rowNum, columnIndex, pageElement.get_text())
                                self.logger.debug("Find other 1st row cell (rowIndex,columnIndex,value) (%s,%s,%s)" % (rowNum, columnIndex,pageElement.get_text()))
                                # Save cur-cell
                        #��ǰһ��Ԫ�ص�Y�ȣ���ǰ�и�Ԫ�ص� X���----����һ�е�һ�������Ԫ��        
                        else:
                            tmpTable.setCellValue(rowNum, columnIndex, pageElement.get_text())
                            self.logger.debug("Find Cell row>1,column>1 (rowIndex,columnIndex,value) (%s,%s,%s)" % (rowNum, columnIndex,pageElement.get_text()))
                            
                    else:
                        #��ǰһ��Ԫ�ص�Y���ȣ���ǰ�и�Ԫ�ص�X���----��(1,1)����ĵ�һ��Ԫ��
                        if pageElement['class'][1] == compareColumnElemnt['class'][1]:
                            if tableStartIndex != 0:
                                rowNum += 1
                                columnNum = columnIndex
                                columnIndex = 1
                            self.logger.debug("Find first column cell(rowIndex,columnIndex,value) (%s,%s,%s)" % (rowNum, columnIndex, pageElement.get_text()))
                            tmpTable.setCellValue(rowNum, columnIndex, pageElement.get_text())                            
                           
                        else:
                            # ��ǰһ��Y���겻�ȣ���ǰ�и�X���겻��----table����
                            if tableStartIndex != 0:
                                tableEndIndex = elementIndex
                                self.logger.info("Table is ended due to Y!=,X!= with info(rowNum,columnNum,tableEndIndex) (%s,%s,%s)" % (rowNum, columnIndex, tableEndIndex))
                                #Save tableEndIndex, rowNum, columnNum append tableList
                                if tableSavedFlag == False:
                                    tmpTable.tableEndIndex = tableEndIndex
                                    tmpTable.rowNum = rowNum
                                    tmpTable.columnNum = columnNum
                                    self.tableList.append(tmpTable)
                                    tableSavedFlag = True
                                
                elif 't' == pageElement['class'][0]:
                    if tableStartIndex != 0:
                        tableEndIndex = elementIndex
                        self.logger.info("Table is ended due to find a class t info(rowNum,columnNum,tableEndIndex) (%s,%s,%s)" % (rowNum, columnIndex, tableEndIndex))
                        #Save tableEndIndex, rowNum, columnNum
                        if tableSavedFlag == False:
                            tmpTable.tableEndIndex = tableEndIndex
                            tmpTable.rowNum = rowNum
                            tmpTable.columnNum = columnNum
                            self.tableList.append(tmpTable)
                            tableSavedFlag = True
                                        
            else:
                if tableStartIndex != 0:
                    tableEndIndex = elementIndex
                    self.logger.info("Page %s with elementNum %s fetch end" % (pageNum, elementIndex))
                break
            pageElement =pageElement.next_sibling
            elementIndex += 1
        pageTotalElemet = elementIndex
         
        
if __name__ == '__main__':
    pdfhtmlextact = PdfHtmlExtractor('../2014.html')
    pageRange = pdfhtmlextact.getSectionStartEndPage(u" ���񱨸�")

    #pageRange = pdfhtmlextact.soup.find_all('div',{'id':pageRange[0]})
    #if 1 < len(pagelist):
       #print "WRN there has more than one same page", pageRange[0] 
    #for page in pagelist:
        #page.next_sibling
    tableinpage = pdfhtmlextact.getTablesinPage('pf3a')
