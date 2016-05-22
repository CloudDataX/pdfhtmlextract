#coding=gbk
__author__ = 'CQC'
# -*- coding:utf-8 -*-

from logger import Logger

class Table(object):
    pageNum = 0
    tableStartIndex = 0
    tableEndIndex = 0
    rowNum = 0
    columnNum = 0
    preExtend = 2    #0��û��ǰ���� 1����ǰ���� 2����ʼֵ
    aftExtend = 2    #0��û�к����� 1���к����� 2����ʼֵ
    cellArray = []
     
    def __init__(self, rowNum, columnNum):
        self.cellArray = [['' for self.columnNum in range(columnNum)] for self.rowNum in range(rowNum)]
        self.rowNum = rowNum
        self.columnNum = columnNum
        return
    
    def setCellValue(self, rowIndex, columnIndex, value):
        self.cellArray[rowIndex][columnIndex] = value
        return
        
    def getCellValue(self, rowIndex, columnIndex):
        if self.cellArray[rowIndex][columnIndex] != None:
            return self.cellArray[rowIndex][columnIndex]
        else:
            return None
        
    def isValidTable(self):
        return True
    def reset(self):
        
        for row in range(0,self.rowNum):
            for column in range(0,self.columnNum):
                self.setCellValue(row, column, "")
        self.pageNum = 0
        self.tableStartIndex = 0
        self.tableEndIndex = 0
        self.rowNum = 0
        self.columnNum = 0
        self.preExtend = 2    #0��û��ǰ���� 1����ǰ���� 2����ʼֵ
        self.aftExtend = 2    #0��û�к����� 1���к����� 2����ʼֵ
     
if __name__ == '__main__':
    my = Table(5,3)
    my.setCellValue(1, 2, u'��')
    print my.getCellValue(1, 2)
    
