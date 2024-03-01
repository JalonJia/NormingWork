'''
Created on 2023-12-17
读取一个文件夹下的Excel，统计每个人的工作时间
@author: Jalon Jia
'''

from TableClass import Field, Table
import xlrd #安装包：pip install xlrd
from datetime import date,datetime
import ReplaceInFile
import os
import copy


s_UI_home = 'D:\\Pluswdev\\AM65A\\UISource'
s_runner_home = 'D:\\Software\\ResourceHacker'
s_RC_save_home = 'D:\\Pluswdev\\AM65A\\AM65AENG'

#Test Funtions
#sPath = "D:\Pluswdev\AM65A\UISource"
#print(os.listdir(sPath))
#print(os.path.split(sPath)) #将路径分解成两部分，第一部分从开始到最后一个路径分隔符，最后一个分隔符后面的路径\
#sPath = 'D:\\ACCPAC\\AM65A\\am.ini'
#print(os.path.dirname(sPath)) #路径的第一部分
#print(os.path.basename(sPath)) #路径的第二部分
#print(os.path.splitext(sPath))

class GetWorkHours(object):
    '''
    循环文件夹下的excel，
    '''

    @staticmethod
    def read_excel(file_name):
        #文件位置
        ExcelFile = xlrd.open_workbook(file_name)
        
        #获取目标EXCEL文件sheet名
        print('Sheets:', ExcelFile.sheet_names())
        
        #------------------------------------
        #若有多个sheet，则需要指定读取目标sheet例如读取sheet2
        #sheet2_name=ExcelFile.sheet_names()[1]
        #------------------------------------
        #获取sheet内容【1.根据sheet索引2.根据sheet名称】
        sheet=ExcelFile.sheet_by_index(1)
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
                    print(sheet.cell(row, col).value)
                    print(sheet.cell_value(row, col))
                    print(sheet.row(row)[col].value)


    @staticmethod
    def read_files(s_folder, file_encoding='UTF-8') :
        """
        读取文件夹下所有的Excel的第2个页签
        """
        print('----------------------Read Excels------------------------------------')

        #replace from *.ctl and *.frm
        # s_from_list = [r'(.*)SetControlsBackColor(.*)Me.BackColor', r'(.*)Let BackColor = Me.BackColor']
        # s_to_list = [r'\1SetControlsBackColor\2mDefaultBackColor', r'\1Let BackColor = mDefaultBackColor']

        for root, dirs, files in os.walk(s_folder): #files会得到目录下的文件（不包括文件夹）；dirs会获取到每个文件夹下面的子目录；root会遍历每个子文件夹
            # print('Current Folder: ', root)
            for file in files:
                s_filename = os.path.splitext(file)[0] #文件名
                s_filetype = os.path.splitext(file)[1] #文件后缀
                
                s_filepath = os.path.join(root, file)
                if not (os.path.exists(s_filepath)):
                    continue

                if (s_filetype == '.xlsx'):
                    GetWorkHours.read_excel(s_filepath)
                    #print(f'Current File: {s_filepath}')
                    #replace_infile(s_filepath, s_from_list, s_to_list, file_encoding)
                
 
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
if __name__ == '__main__' :
    #print(xlrd.XL_CELL_NUMBER)
    #GetWorkHours.read_files(r'D:\Working\02WeeklyWorking\2023\2023Weekly')
    GetWorkHours.read_files(r'D:\Working\02WeeklyWorking\2023\test')

    #GetWorkHours.read_excel(r'D:\Working\WeeklyWorking\0ThisWeek\2021Work\2021\OEM20210109.xlsx')
    #x = ReadExcel(r'D:\Documents\OEMDocuments\RMDocs\RM66A\PU2\Design\EN66A_PU2_TablesChange.xlsx')
    #x = ReadExcel(r'D:\Documents\OEMDocuments\RMDocs\RM67A\PU0\Design\POTables.xlsx')
    #x.read_excel_create_resource(r'D:\Documents\OEMDocuments\RMDocs\RM65APU2\temp.txt')
    #x.generate_table_changes(r'D:\Documents\OEMDocuments\RMDocs\RM67A\PU2\Temp')
 
    # s_mask_or_list = '(%-12N)'
    # s_from = r'(.*)%[-](.*)[\)*]$'
    # s_to = r'Key\2Mask'
    # s_mask_or_list = ReplaceInFile.replace_re(s_mask_or_list, s_from, s_to)
    # s_mask_or_list = 'RateOperList1 - Multiply2 - Divide'
    # s_from = r'(.*)List([\S\s]*)'
    # s_to = r'\1List'
    # s_mask_or_list = ReplaceInFile.replace_re(s_mask_or_list, s_from, s_to) 
    # print(s_mask_or_list)


    