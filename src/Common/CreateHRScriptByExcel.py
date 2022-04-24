'''
Created on May 23, 2018
To Read Excel and then Create DB Scripts
@author: Jalon Jia
'''

from re import LOCALE
from time import localtime
from TableClass import Field, Table, Security
import xlrd #安装包：pip install xlrd
from datetime import date,datetime
import ReplaceInFile
import os
import copy
import time


class CreateHRScriptByExcel(object):
    '''
    TODO: 根据HR表结构修改的Excel生成创建表、加字段的脚本 
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

        b_new = False
                    
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
            
            if (sheet.name == 'New Tables'):
                b_new = True
            elif (sheet.name == 'Changed Tables') :
                b_new = False
            else:
                continue
                        
            #print Each Cell
            for row in range(sheet.nrows):
                if b_new:
                    s_table = str(sheet.row_values(row)[0]).strip()
                else:
                    split_temp = str(sheet.row_values(row)[1]).strip().split('表名 : ', 1)
                    if len(split_temp)>1:
                        s_table = split_temp[1]
                    else:
                        s_table = ''

                # print(sheet.row_values(row))
                b_created = (str(sheet.row_values(row)[11][:1]).upper() == 'Y') #L列如果是Y表示已经创建过了

                #待新增表的表头
                if b_new and (s_table == 'Table'): 
                    if (table.table_name > '') and (not table.b_created) and (len(table.fields) > 0):
                        last_table = copy.deepcopy(table)
                        tables.append(last_table)

                    table.table_name = sheet.row_values(row)[1].strip().upper()
                    table.table_desc = sheet.row_values(row)[3].strip()
                    table.table_desc2 = sheet.row_values(row)[4].strip()
                    table.fields = []
                    table.b_created = b_created
                    table.isnew = b_new
                    continue

                #待修改表的表头
                if (not b_new) and len(s_table)>0:
                    if table.table_name > '' and (not table.b_created) and (len(table.fields) > 0):
                        last_table = copy.deepcopy(table)
                        tables.append(last_table)

                    table.table_name = s_table.upper()
                    table.table_desc = sheet.row_values(row)[3].strip().replace('描述 : ', '')
                    table.table_desc2 = table.table_desc
                    table.fields = []
                    table.b_created = b_created
                    table.isnew = b_new
                    continue

                if (b_new and sheet.row_values(row)[1] != '') \
                    or ((not b_new) and str(sheet.row_values(row)[0]).strip().upper() == 'NEW'):
                    #Example：'*	RCPNUMBER	String	22	0	Receipt Number	%-22C'
                    #print(sheet.row_values(row)[1])
                    #print(sheet.row_values(row)[5])
                    field = Field()
                    if (sheet.row_values(row)[0].strip() == '*') or (sheet.row_values(row)[8].strip().lower() == 'yes'):
                        field.is_key = True

                    if sheet.row_values(row)[1].strip() > '':
                        field.field_name = sheet.row_values(row)[1].strip().upper()
                    else: #不是合法的行
                        continue

                    if str(sheet.row_values(row)[2]).strip() > '':
                        field.type = str(sheet.row_values(row)[2]).strip().lower()
                        if not (field.type in 'bcd|number|long|string|integer|int|date|time|boolean|decimal|datetime|varchar|nvarchar|'): #不是合法的行
                            continue
                        if field.type == 'bcd' or field.type == 'decimal':
                            field.type = 'number' 
                        if field.type == 'boolean':
                            field.type = 'integer' 
                    else: #不是合法的行
                        continue
                    
                    if str(sheet.row_values(row)[5]).strip() > '':
                        field.length = int(str(sheet.row_values(row)[5]).strip().split('.')[0])
                    
                    if str(sheet.row_values(row)[6]).strip() > '':
                        field.decimal = int(str(sheet.row_values(row)[6]).strip().split('.')[0])

                    if str(sheet.row_values(row)[3]).strip() > '':
                        field.desc = str(sheet.row_values(row)[3]).strip()

                    if str(sheet.row_values(row)[4]).strip() > '':
                        field.desc2 = str(sheet.row_values(row)[4]).strip()

                    if str(sheet.row_values(row)[7]).strip() > '':
                        field.default = str(sheet.row_values(row)[7]).strip()

                    # if str(sheet.row_values(row)[6]).strip() > '':
                    #     s_mask_or_list = str(sheet.row_values(row)[6]).strip()
                    #     s_from = r'(.*)%[-](.*?)([\)]?)$' #为了匹配(%-12N),对最后一个括号之前的字符使用非贪婪模式
                    #     s_to = r'Key\2Mask'
                    #     s_mask_or_list = ReplaceInFile.replace_re(s_mask_or_list, s_from, s_to)
                    #     s_from = r'(.*)List([\S\s]*)'
                    #     s_to = r'\1List'
                    #     s_mask_or_list = ReplaceInFile.replace_re(s_mask_or_list, s_from, s_to)                        
                    #     field.mask_or_list = s_mask_or_list

                    table.add_field(field)                   

        #最后一个table
        if table.table_name > '':
            last_table = copy.deepcopy(table)
            tables.append(last_table)

        return tables


    def generate_table_changes(self, file_path):
        '''
        TODO: 得到数据表的结构变化，并生成sql文件以及资源文件
        '''

        s_date = time.strftime("%Y-%m-%d",time.localtime())

        tables = self.get_changed_tables()
        if len(tables) == 0:
            return
        
        if not os.path.exists(file_path):
            os.makedirs(file_path, mode=0o777, exist_ok=True)
        
        s_file = os.path.join(file_path, 'changed_tables_%s.sql' % s_date)
        with open(s_file, 'w', encoding='UTF-8', errors='ignore' ) as f_w:
            for table in tables:
                f_w.write(table.get_table_sqlscript())
                f_w.write('\n\n')

        s_file = os.path.join(file_path, 'upgrade_tables_%s.sql' % s_date)
        with open(s_file, 'w', encoding='UTF-8', errors='ignore' ) as f_w:
            for table in tables:
                s_sql = table.get_table_upgradesql()
                if len(s_sql)>0:
                    f_w.write(s_sql)
                    f_w.write('\n')
                

        # s_file = os.path.join(file_path, 'changed_tables.rc')
        # with open(s_file, 'w', encoding='UTF-8', errors='ignore' ) as f_w:
        #     for table in tables:                
        #         f_w.write(table.get_fileds_desc())        

        for table in tables:
        #     s_file = os.path.join(file_path, f'{table.table_name}.tbl')
        #     table.generate_tbl_file(s_file)
        #     s_file = os.path.join(file_path, f'{table.table_name}.ptn')
        #     table.generate_ptn_file(s_file)
        #     s_file = os.path.join(file_path, f'{table.table_name}.cpp')
        #     table.generate_class_code(s_file)
        #     s_file = os.path.join(file_path, f'{table.table_name}.sql')
        #     table.generate_sql_file(s_file)
            s_new = ''
            if table.isnew:
                s_new = 'new\\'
            s_module = table.table_name[0:2].upper() + "\\"
            s_folder = os.path.join(file_path, f'{s_new}{s_module}')
            if not os.path.exists(s_folder):
                os.makedirs(s_folder, mode=0o777, exist_ok=True)
            s_file = os.path.join(s_folder, f'{table.table_name}.xml')
            with open(s_file, 'w', encoding='UTF-8', errors='ignore' ) as f_w:
                f_w.write(table.get_table_dictionary())

        s_file = os.path.join(file_path, 'table_define_index_%s.sql' % s_date)
        with open(s_file, 'w', encoding='UTF-8', errors='ignore' ) as f_w:
            for table in tables:
                s_sql = table.get_table_define_index()
                if len(s_sql)>0:
                    f_w.write(s_sql)
                    f_w.write('\n')

            
            
    def get_changed_security(self):
        '''
        TODO: 读取Excel，得到新增的权限列表
        '''

        seclist = []
        sec = Security('')
        
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
            
            if not (sheet.name == 'Security'):
                continue
                        
            #print Each Cell
            for row in range(sheet.nrows):
                s_secname = str(sheet.row_values(row)[1]).strip()
                if (row == 0) or (len(s_secname)==0):
                    continue

                # print(sheet.row_values(row))
                b_created = (str(sheet.row_values(row)[11][:1]).upper() == 'Y') #L列如果是Y表示已经创建过了

                #待修改表的表头
                if len(s_secname)>0:
                    if sec.sec_name > '' and (not sec.b_created):
                        last_sec = copy.deepcopy(sec)
                        seclist.append(last_sec)

                    sec.sec_name = s_secname.upper()
                    sec.sec_sequence = str(int(sheet.row_values(row)[2])).strip()
                    sec.sec_desc = sheet.row_values(row)[3].strip()
                    sec.sec_desc2 = sheet.row_values(row)[4].strip()
                    sec.b_created = b_created                    
                    continue

        #最后一个table
        if sec.sec_name > '':
            last_sec = copy.deepcopy(sec)
            seclist.append(last_sec)

        return seclist
        

    def generate_security_changes(self, file_path):
        '''
        TODO: 得到权限列表的结构变化，并生成sql文件以及资源文件
        '''

        s_date = time.strftime("%Y-%m-%d",time.localtime())
        seclist = self.get_changed_security()
        if len(seclist) == 0:
            return
        
        if not os.path.exists(file_path):
            os.makedirs(file_path, mode=0o777, exist_ok=True)
        
        s_file = os.path.join(file_path, 'ASSEC_%s.sql' % s_date)
        with open(s_file, 'w', encoding='UTF-8', errors='ignore' ) as f_w:
            for sec in seclist:
                f_w.write(sec.get_initsql())
                f_w.write('\n')

        s_file = os.path.join(file_path, 'ASGRPSEC_%s.sql' % s_date)
        with open(s_file, 'w', encoding='UTF-8', errors='ignore' ) as f_w:
            for sec in seclist:
                f_w.write(sec.get_initgroup_sql())
                f_w.write('\n')
                
        


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
    print('Start:' + time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))

    #x = CreateHRScriptByExcel(r'D:\Working\WorkDocuments\OEMDocuments\HRMSDocs\2021.09\eHRMS2021.09数据流.xlsx')
    x = CreateHRScriptByExcel(r'D:\Working\WeeklyWorking\0ThisWeek\HREXTEMP_Module.xlsx')
    #x.read_excel()
    #x.read_excel_create_resource(r'D:\Documents\OEMDocuments\RMDocs\RM65APU2\temp.txt')
    s_saveto = r'D:\Working\WeeklyWorking\0ThisWeek\Temp'
    x.generate_table_changes(s_saveto)
    #x.generate_security_changes(s_saveto)
    
    print('End:' + time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
    # s_mask_or_list = '(%-12N)'
    # s_from = r'(.*)%[-](.*)[\)*]$'
    # s_to = r'Key\2Mask'
    # s_mask_or_list = ReplaceInFile.replace_re(s_mask_or_list, s_from, s_to)
    # s_mask_or_list = 'RateOperList1 - Multiply2 - Divide'
    # s_from = r'(.*)List([\S\s]*)'
    # s_to = r'\1List'
    # s_mask_or_list = ReplaceInFile.replace_re(s_mask_or_list, s_from, s_to) 
    # print(s_mask_or_list)


    