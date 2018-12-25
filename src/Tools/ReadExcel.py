'''
Created on May 23, 2018
To Read Excel
@author: Jalon Jia
'''

import xlrd #安装包：pip install xlrd
from datetime import date,datetime


class ReadExcel(object):
    '''
    classdocs
    '''
    def __init__(self, p_file_name):
        '''
        Constructor
        '''
        self.file_name = p_file_name
    
    def read_excel(self):
        #文件位置
        ExcelFile = xlrd.open_workbook(self.file_name)
        
        #获取目标EXCEL文件sheet名
        print('Sheets:', ExcelFile.sheet_names())
        
        #------------------------------------
        #若有多个sheet，则需要指定读取目标sheet例如读取sheet2
        #sheet2_name=ExcelFile.sheet_names()[1]
        #------------------------------------
        #获取sheet内容【1.根据sheet索引2.根据sheet名称】
        #sheet=ExcelFile.sheet_by_index(1)
        for sheet_name in ExcelFile.sheet_names():
            sheet = ExcelFile.sheet_by_name(sheet_name)        
            #打印sheet的名称，行数，列数
            print('Sheet Name:%s, Rows: %d, Columns: %d' % (sheet.name, sheet.nrows, sheet.ncols))
            
            #获取整行或者整列的值
            #print Each Row
            for row in range(sheet.nrows):
                print(sheet.row_values(row))
                
            #print Each Column
            for col in range(sheet.ncols):
                print(sheet.col_values(col))
            
            #print Each Cell
            for row in range(sheet.nrows):
                for col in range(sheet.ncols):
                    print(sheet.cell(row, col))
                    
                    #打印单元格内容格式
                    print(sheet.cell(row, col).ctype)
                
                    #获取单元格内容
                    if sheet.cell(row, col).ctype == xlrd.XL_CELL_NUMBER: #判断类型
                        print(sheet.cell(row, col).value)
                        print(sheet.cell_value(row, col))
                        print(sheet.row(row)[col].value)
                    else:
                        print(sheet.cell(row, col).value.encode('utf-8'))
                        print(sheet.cell_value(row, col).encode('utf-8'))
                        print(sheet.row(row)[col].value.encode('utf-8'))


    def read_excel_create_resource(self, to_file_name):
        #文件位置
        ExcelFile = xlrd.open_workbook(self.file_name)
        
        #获取目标EXCEL文件sheet名
        #print('Sheets:', ExcelFile.sheet_names())
        
        file = open(to_file_name, 'w', encoding = 'UTF-8')
             
        #------------------------------------
        #若有多个sheet，则需要指定读取目标sheet例如读取sheet2
        #sheet2_name=ExcelFile.sheet_names()[1]
        #------------------------------------
        #获取sheet内容【1.根据sheet索引2.根据sheet名称】
        #sheet=ExcelFile.sheet_by_index(1)
        for sheet_name in ExcelFile.sheet_names():
            sheet = ExcelFile.sheet_by_name(sheet_name)        
            #打印sheet的名称，行数，列数
            #print('Sheet Name:%s, Rows: %d, Columns: %d' % (sheet.name, sheet.nrows, sheet.ncols))
            
            if (sheet.name != 'New Tables') and (sheet.name != 'Changed Tables') :
                continue
            
            table_name = ''
             
            #print Each Cell
            for row in range(sheet.nrows):
                if sheet.row_values(row)[0][:2] == 'EN' :
                    table_name = sheet.row_values(row)[0]
                    res_str = 'IDS_%s_VIEW_NAME%s,        "%s"\nIDS_%s_VIEW_NOUN%s,        "%s"\n' % (table_name, ' ' * (15-len(table_name)), sheet.row_values(row)[1], table_name, ' ' * (15-len(table_name)), sheet.row_values(row)[1])
                    print(res_str)
                    if sheet.row_values(row)[1] != '' :
                        file.write(f'#include "{table_name}.i"\n')
                        file.write(res_str)
                        #print(table_name)
                    continue
                
                if sheet.row_values(row)[1] != '' :
                    #print(sheet.row_values(row)[1])
                    #print(sheet.row_values(row)[5])
                    res_str = 'IDS_%s_%s_FLD%s,        "%s"\n' % (table_name, sheet.row_values(row)[1], ' ' * (20-len(table_name)-len(sheet.row_values(row)[1])), sheet.row_values(row)[5])
                    print(res_str)
                    file.write(res_str)
                    
                
                        
        file.close()               

#def __main__():
#    pass


'''
def read_excel():
    #文件位置
    ExcelFile = xlrd.open_workbook(r'D:\Documents\RM64ADocs\PU3\EN64APU3_TablesChange.xlsx')
    
    #获取目标EXCEL文件sheet名
    print(ExcelFile.sheet_names())
    
    #------------------------------------
    #若有多个sheet，则需要指定读取目标sheet例如读取sheet2
    #sheet2_name=ExcelFile.sheet_names()[1]
    #------------------------------------
    #获取sheet内容【1.根据sheet索引2.根据sheet名称】
    #sheet=ExcelFile.sheet_by_index(1)
    sheet=ExcelFile.sheet_by_name('EN64APU2_ChangedTables')
    
    #打印sheet的名称，行数，列数
    print(sheet.name,sheet.nrows,sheet.ncols)
    
    #获取整行或者整列的值
    rows=sheet.row_values(2)#第三行内容
    cols=sheet.col_values(1)#第二列内容
    print(cols,rows)
    
    #获取单元格内容
    print(sheet.cell(1,0).value.encode('utf-8'))
    print(sheet.cell_value(1,0).encode('utf-8'))
    print(sheet.row(1)[0].value.encode('utf-8'))
    
    #打印单元格内容格式
    print(sheet.cell(1,0).ctype)
'''

#Testing
if (__name__ == '__main__') :
    #print(xlrd.XL_CELL_NUMBER)
    x = ReadExcel(r'D:\Documents\OEMDocuments\RMDocs\RM65APU2\EN65APU2_TablesChange.xlsx')
    #x.read_excel()
    x.read_excel_create_resource(r'D:\Documents\OEMDocuments\RMDocs\RM65APU2\temp.txt')
    
    