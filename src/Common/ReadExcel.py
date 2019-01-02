'''
Created on May 23, 2018
To Read Excel
@author: Jalon Jia
'''

from TableClass import Field, Table
import xlrd #安装包：pip install xlrd
from datetime import date,datetime
import ReplaceInFile
import os
import copy


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


    def get_changed_tables(self):
        '''
        TODO: 读取Excel，得到新增的表以及调整表结构的表
        '''

        tables = []
        table = Table('', '')
        
        #文件位置
        ExcelFile = xlrd.open_workbook(self.file_name)
        
        #获取目标EXCEL文件sheet名
        #print('Sheets:', ExcelFile.sheet_names())
                    
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
                        
            #print Each Cell
            for row in range(sheet.nrows):
                s_appl = str(sheet.row_values(row)[0][:2])
                if len(s_appl)>0 and (s_appl in 'EN|AM|NP|IS|BS|VS|VI|SS|PS|') :
                    if table.table_name > '':
                        last_table = copy.deepcopy(table)
                        tables.append(last_table)

                    table.table_name = sheet.row_values(row)[0].strip().upper()
                    table.table_desc = sheet.row_values(row)[1].strip()
                    table.fields = []
                    continue
                
                if sheet.row_values(row)[1] != '' :
                    #Example：'*	RCPNUMBER	String	22	0	Receipt Number	%-22C'
                    #print(sheet.row_values(row)[1])
                    #print(sheet.row_values(row)[5])
                    field = Field()
                    if sheet.row_values(row)[0].strip() == '*':
                        field.is_key = True

                    if sheet.row_values(row)[1].strip() > '':
                        field.field_name = sheet.row_values(row)[1].strip().upper()
                    else: #不是合法的行
                        continue

                    if sheet.row_values(row)[2].strip() > '':
                        field.type = sheet.row_values(row)[2].strip().lower()
                        if not (field.type in 'bcd|long|string|integer|int|date|time|'): #不是合法的行
                            continue
                        if field.type == 'bcd':
                            field.type = 'number' 
                    else: #不是合法的行
                        continue
                    
                    if str(sheet.row_values(row)[3]).strip() > '':
                        field.length = int(str(sheet.row_values(row)[3]).strip().split('.')[0])
                    
                    if sheet.row_values(row)[4].strip() > '':
                        field.decimal = int(sheet.row_values(row)[4].strip())

                    if sheet.row_values(row)[5].strip() > '':
                        field.desc = sheet.row_values(row)[5].strip()

                    if sheet.row_values(row)[6].strip() > '':
                        s_mask_or_list = sheet.row_values(row)[6].strip()
                        s_from = r'(.*)%[-](.*?)([\)]?)$' #为了匹配(%-12N),对最后一个括号之前的字符使用非贪婪模式
                        s_to = r'Key\2Mask'
                        s_mask_or_list = ReplaceInFile.replace_re(s_mask_or_list, s_from, s_to)
                        s_from = r'(.*)List([\S\s]*)'
                        s_to = r'\1List'
                        s_mask_or_list = ReplaceInFile.replace_re(s_mask_or_list, s_from, s_to)                        
                        field.mask_or_list = s_mask_or_list

                    table.add_field(field)                   

        #最后一个table
        if table.table_name > '':
            last_table = copy.deepcopy(table)
            tables.append(last_table)

        return tables


    def generate_table_changes(self, file_path):
        '''
        TODO: 得到数据表的结构变化，并生成tbl文件以及资源文件
        '''

        tables = self.get_changed_tables()
        if len(tables) == 0:
            return
        
        if not os.path.exists(file_path):
            os.makedirs(file_path, mode=0o777, exist_ok=True)
        
        s_file = os.path.join(file_path, 'changed_tables.rc')
        with open(s_file, 'w', encoding='UTF-8', errors='ignore' ) as f_w:
            for table in tables:                
                f_w.write(table.get_fileds_desc())

        for table in tables:
            s_file = os.path.join(file_path, f'{table.table_name}.tbl')
            table.generate_tbl_file(s_file)
        



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
    x = ReadExcel(r'D:\Documents\OEMDocuments\RMDocs\RM65APU2\EN65APU2_TablesChange.xlsx')
    #x.read_excel()
    #x.read_excel_create_resource(r'D:\Documents\OEMDocuments\RMDocs\RM65APU2\temp.txt')
    x.generate_table_changes(r'D:\Documents\OEMDocuments\RMDocs\RM65APU2\Temp')

    # s_mask_or_list = '(%-12N)'
    # s_from = r'(.*)%[-](.*)[\)*]$'
    # s_to = r'Key\2Mask'
    # s_mask_or_list = ReplaceInFile.replace_re(s_mask_or_list, s_from, s_to)
    # s_mask_or_list = 'RateOperList1 - Multiply2 - Divide'
    # s_from = r'(.*)List([\S\s]*)'
    # s_to = r'\1List'
    # s_mask_or_list = ReplaceInFile.replace_re(s_mask_or_list, s_from, s_to) 
    # print(s_mask_or_list)


    