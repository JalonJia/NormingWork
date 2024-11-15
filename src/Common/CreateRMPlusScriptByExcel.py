'''
Created on April 03, 2023
To Read Excel and then Create DB Scripts
@author: Jalon Jia
'''

from re import LOCALE
from time import localtime
from TableClass import TableIndex, Field, Table, Security, DropdownList
import xlrd #安装包：pip install xlrd
from datetime import date,datetime
import ReplaceInFile
import os
import copy
import time


class CreateRMPlusScriptByExcel(object):
    '''
    TODO: 根据RM+表结构修改的Excel生成创建表、加字段的脚本 
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
        '''
            暂时不用
        '''
        #resolved
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
        用途: 读取Excel，得到新增的表以及调整表结构的表
        '''

        tables = []
        table = Table('', '')

        dropdowns = {}
        
        #文件位置
        ExcelFile = xlrd.open_workbook(self.file_name)
        
        #获取目标EXCEL文件sheet名
        #print('Sheets:', ExcelFile.sheet_names())

        b_new = False
        # s_table_flag = ''
                    
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
                s_table_flag = str(sheet.row_values(row)[0]).strip().lower()
                # if b_new:
                #     s_table = str(sheet.row_values(row)[0]).strip()
                # else:
                #     split_temp = str(sheet.row_values(row)[1]).strip().split('表名 : ', 1)
                #     if len(split_temp)>1:
                #         s_table = split_temp[1]
                #     else:
                #         s_table = ''

                # print(sheet.row_values(row))
                
                #下一个表开始行
                if ('table' in s_table_flag): 
                    if (table.table_name > '') and (not table.b_created) and (len(table.fields) > 0):
                        last_table = copy.deepcopy(table)
                        tables.append(last_table)

                    table.table_name = sheet.row_values(row)[1].strip().lower()     #B列==表名
                    table.table_desc = sheet.row_values(row)[9].strip()             #J列==表描述-英文
                    table.table_desc2 = sheet.row_values(row)[10].strip()           #K列==表描述-中文
                    #M列值==Y表示已经创建过了
                    b_created = (str(sheet.row_values(row)[12]).upper() == 'Y') or (str(sheet.row_values(row)[12]).upper() == 'YES')
                    table.fields = []
                    table.indexes = []
                    table.b_created = b_created
                    table.isnew = b_new
                    table.issetup = (str(sheet.row_values(row)[2]).upper() == 'SETUP') #C列标记是否是Setup表
                    continue

                #B列为字段名
                tmp_field_name = str(sheet.row_values(row)[1]).strip().lower()
                #J列为字段英文描述
                temp_desc = str(sheet.row_values(row)[9]).strip()
                #K列为字段中文描述
                temp_desc2 = str(sheet.row_values(row)[10]).strip()
                #G列为Yes或Y表示是主键字段或不可重复
                b_unique = False
                if (str(sheet.row_values(row)[0]).strip() == '*') \
                    or (str(sheet.row_values(row)[6]).strip().lower() == 'yes') \
                    or (str(sheet.row_values(row)[6]).strip().lower() == 'y'): 
                    b_unique = True

                #index
                if ('index' in s_table_flag):
                    idx_seq = 1
                    if len(s_table_flag.strip().split('index')[1]) > 0:
                        idx_seq = int(s_table_flag.strip().split('index')[1])
                    ind = TableIndex(tmp_field_name, b_unique, temp_desc, temp_desc2, idx_seq)
                    table.add_index(ind)
                    continue

                if (b_new and tmp_field_name != '') \
                    or ((not b_new) and s_table_flag == '+'):
                    #Example：'+	yyyy_id	bigint			1	Y	Y		increment ID	自增ID'
                    #print(sheet.row_values(row)[1])
                    #print(sheet.row_values(row)[5])
                    field = Field()
                    
                    if tmp_field_name > '':
                        field.field_name = tmp_field_name
                    else: #不是合法的行
                        continue

                    #C列为字段类型
                    temp_field_type = str(sheet.row_values(row)[2]).strip().lower()
                    if len(temp_field_type) ==0:
                        continue

                    if not (temp_field_type in 
                        'bcd|number|long|string|integer|int|bigint|date|time|boolean|decimal|datetime|varchar|nvarchar|text|ntext|blob'): #不是合法的行
                        continue
                    
                    field.is_key = b_unique
                    field.desc = temp_desc
                    field.desc2 = temp_desc2
                    
                    field.type = temp_field_type
                    if field.type == 'bcd' or field.type == 'decimal':
                        field.type = 'number' 
                    elif field.type == 'boolean':
                        field.type = 'integer'
                    elif field.type == 'bigint':
                        field.type = 'bigint'
                    
                    #D列为字段长度
                    if str(sheet.row_values(row)[3]).strip() > '':
                        field.length = int(str(sheet.row_values(row)[3]).strip().split('.')[0])
                    
                    #E列为字段精度
                    if str(sheet.row_values(row)[4]).strip() > '':
                        field.decimal = int(str(sheet.row_values(row)[4]).strip().split('.')[0])

                    #F列为字段默认值
                    if str(sheet.row_values(row)[5]).strip() > '':
                        field.default = str(sheet.row_values(row)[5]).strip()

                    #H列为字段是否不允许为空的标记
                    if (sheet.row_values(row)[7].strip().lower() == 'yes') \
                        or (sheet.row_values(row)[7].strip().lower() == 'y'): 
                        field.not_null = True

                    #I列为Mask/List定义
                    if str(sheet.row_values(row)[8]).strip() > '':
                        s_mask_or_list = str(sheet.row_values(row)[8]).strip()
                        s_from = r'(.*)%[-](.*?)([\)]?)$' #为了匹配(%-12N),对最后一个括号之前的字符使用非贪婪模式
                        s_to = r'Key\2Mask'
                        field.mask_or_list = ReplaceInFile.replace_re(s_mask_or_list, s_from, s_to)

                        if '%' in s_mask_or_list:
                            field.mask = s_mask_or_list
                        else:
                            s_from = r'(.*)List([\S\s]*)'
                            s_to = r'\1List'
                            field.list_name = ReplaceInFile.camel_to_underscore(
                                ReplaceInFile.replace_re(s_mask_or_list, s_from, s_to)).replace('_list', '')
                            dropdowns[field.list_name] = DropdownList(field.list_name, field.mask_or_list)


                    table.add_field(field)                   

        #最后一个table
        if (table.table_name > '') and (not table.b_created) and (len(table.fields) > 0):
            last_table = copy.deepcopy(table)
            tables.append(last_table)

        return tables, dropdowns


    def get_dropdown_scripts(self, file_path, dorpdowns):
        '''
        将Dropdown生成对应的脚本
        '''

        if len(dorpdowns) == 0:
            return

        s_date = time.strftime("%Y-%m-%d", time.localtime())
        s_folder = os.path.join(file_path, 'tables')
        if not os.path.exists(s_folder):
            os.makedirs(s_folder, mode=0o777, exist_ok=True)
        s_file = os.path.join(s_folder, 'table_dict.json')
        s_next_line = '\n'
        with open(s_file, 'w', encoding='UTF-8', errors='ignore' ) as f_w:
            f_w.write('{')
            for dp in dorpdowns.values():
                f_w.write(f'{s_next_line}    ')
                f_w.write(dp.get_json_context())
                s_next_line = ',\n'
            f_w.write('\n}')

        s_folder = os.path.join(file_path, 'i18n\\dict')
        if not os.path.exists(s_folder):
            os.makedirs(s_folder, mode=0o777, exist_ok=True)
        s_file = os.path.join(s_folder, 'messages_en_US.properties')
        with open(s_file, 'w', encoding='UTF-8', errors='ignore' ) as f_w:
            for dp in dorpdowns.values():
                f_w.write(dp.get_json_res_eng())

        s_file = os.path.join(s_folder, 'messages_zh_CN.properties')
        with open(s_file, 'w', encoding='UTF-8', errors='ignore' ) as f_w:
            for dp in dorpdowns.values():
                f_w.write(dp.get_json_res_eng())

        # s_file = os.path.join(file_path, 'changed_dict_resouces_%s.sql' % s_date)
        s_file = os.path.join(file_path, 'changed_tables_resouces_%s.sql' % s_date)
        with open(s_file, 'a', encoding='UTF-8', errors='ignore') as f_w:
            # f_w.write("delete from SYS_TRANS_NM WHERE CATEGORY='Dict';")
            f_w.write("\n\n")
            for dp in dorpdowns.values():
                f_w.write(dp.get_resources_SQL_RMPlus())
                f_w.write('\n')


    def get_table_relations(self, file_path, tables):
        '''
        比较所有的数据表结构和Setup表，得到字段之间的关联关系，生成SQL脚本
        '''

        s_date = time.strftime("%Y-%m-%d", time.localtime())
        # 初始化关联关系表
        possible_relations = []
        for table1 in tables:
            for table2 in tables:
                if not table2.issetup or table1 == table2:
                    continue

                # 寻找相同的字段名或相似的字段名
                ignore_fields = {'create_by', 'create_time', 'update_time', 'update_by', 'date_inactive', 'status',
                                 'comments', 'notes', 'pmflag', 'wf_ver', 'pmbg_over', 'home_cur', 'fisc_year',
                                 'rate_date', 'attaches', 'doc_ref', 'fisc_period', 'substitute_by', 'submit_date',
                                 'in_endorse', 'trans_type', 'order_num', 'bpmn_id', 'pid'}
                fields_set1 = set(d.field_name for d in table1.fields
                                  if (not d.is_key) and ('id' in d.field_name or 'code' in d.field_name)) - ignore_fields
                fields_set2 = set(d.field_name for d in table2.fields if d.is_key) - ignore_fields
                common_fields = []
                for key_uuid in fields_set2:
                    for relation_field in fields_set1:
                        if (key_uuid == relation_field) \
                            or (f'_{key_uuid}' in relation_field) \
                            or (f'{key_uuid}_' in relation_field):
                            common_fields.append([relation_field, key_uuid])
                # common_fields = fields_set1.intersection(fields_set2)

                if common_fields:
                    code_fields = list(d.field_name for d in table2.fields if 'CODE' in d.field_name.upper())
                    code_field = '' if len(code_fields) == 0 else code_fields[0]
                    desc_fields = list(d.field_name for d in table2.fields
                                       if 'DESC' in d.field_name.upper() or 'NAME' in d.field_name.upper())
                    desc_field = '' if len(desc_fields) == 0 else desc_fields[0]
                    possible_relations.extend(
                        [(f"{table1.table_name}", f"{field[0]}", f"{table2.table_name}", f"{field[1]}",
                          f"{code_field}", f"{desc_field}")
                         for field in common_fields])
                        # [(f"{table1.table_name}.{field}", f"{table2.table_name}.{field}") for field in common_fields])

        #添加一些特殊的关联关系，字段名不一样的
        # possible_relations.extend(["HRE_EMP", "CA_WF_UUID", "CMS_WF_CATE", "WF_UUID", "WF_CODE", "WF_DESC", ""])
        # possible_relations.extend(["HRE_EMP", "EXP_WF_UUID", "CMS_WF_CATE", "WF_UUID", "WF_CODE", "WF_DESC", ""])
        # possible_relations.extend(["HRE_EMP", "TRV_WF_UUID", "CMS_WF_CATE", "WF_UUID", "WF_CODE", "WF_DESC", ""])
        # possible_relations.extend(["HRE_EMP", "EXP_ACCST_UUID", "EXP_ACCST", "ACCST_UUID", "ACCST_CODE", "ACCST_DESC", ""])
        # possible_relations.extend(["HRE_TMP", "CA_WF_UUID", "CMS_WF_CATE", "WF_UUID", "WF_CODE", "WF_DESC", ""])
        # possible_relations.extend(["HRE_TMP", "EXP_WF_UUID", "CMS_WF_CATE", "WF_UUID", "WF_CODE", "WF_DESC", ""])
        # possible_relations.extend(["HRE_TMP", "TRV_WF_UUID", "CMS_WF_CATE", "WF_UUID", "WF_CODE", "WF_DESC", ""])
        # possible_relations.extend(["HRE_TMP", "EXP_ACCST_UUID", "EXP_ACCST", "ACCST_UUID", "ACCST_CODE", "ACCST_DESC", ""])


        s_file = os.path.join(file_path, 'relation_fields_%s.sql' % s_date)
        with open(s_file, 'w', encoding='UTF-8', errors='ignore') as f_w:
            for relation in possible_relations:
                s_sql = """\
INSERT INTO SYS_TABLE_RELATION(TR_UUID, CREATE_BY, UPDATE_BY, BASE_TABLE, BASE_FIELD, \
LINKTO_TABLE, LINKTO_FIELD, LINK_TYPE, LINKTO_CODE, LINKTO_DESC, LINKTO_ADD_FIELDS, LINKTO_FINDER_FIELDS, \
ADD_FILTER, USED_BY, IS_SYSTEM, STATUS, DATE_INACTIVE, COMMENTS) \
VALUES (NEWID(), N'SYSTEM', N'SYSTEM', N'%s', N'%s', N'%s', N'%s', \
0, N'%s', N'%s', N'', N'', N'', 0, 1, 1, '1900-01-01 00:00:00.000', N'');
""" % (relation[0].upper(), relation[1].upper(), relation[2].upper(),
       relation[3].upper(), relation[4].upper(), relation[5].upper())
                f_w.write(s_sql)
                # f_w.write('\n')


    def generate_table_changes(self, file_path):
        '''
        用途: 得到数据表的结构变化，并生成sql文件以及资源文件
        '''

        s_date = time.strftime("%Y-%m-%d",time.localtime())

        tables = self.get_changed_tables()[0]
        if len(tables) == 0:
            return

        tables.sort(key=lambda x:x.table_name)

        if not os.path.exists(file_path):
            os.makedirs(file_path, mode=0o777, exist_ok=True)
        
        # s_file = os.path.join(file_path, 'changed_tables_list_%s.sql' % s_date)
        # with open(s_file, 'w', encoding='UTF-8', errors='ignore' ) as f_w:
        #     for table in tables:
        #         f_w.write(table.get_table_desc())
        #         f_w.write('\n')

        s_file = os.path.join(file_path, 'changed_tables_%s.sql' % s_date)
        with open(s_file, 'w', encoding='UTF-8', errors='ignore' ) as f_w:
            f_w.write(f'-- {s_date}\n')
            for table in tables:
                f_w.write(table.get_table_desc())
                f_w.write('\n')

            f_w.write('\n')
            for table in tables:
                f_w.write(table.get_table_sqlscript())
                f_w.write('\n')

        s_file = os.path.join(file_path, 'upgrade_tables_%s.sql' % s_date)
        with open(s_file, 'w', encoding='UTF-8', errors='ignore' ) as f_w:
            f_w.write(f'-- {s_date}\n')
            for table in tables:
                s_sql = table.get_table_upgradesql()
                if len(s_sql)>0:
                    f_w.write(s_sql)
                    f_w.write('\n')

        s_file = os.path.join(file_path, 'changed_tables_desc_%s.sql' % s_date)
        with open(s_file, 'w', encoding='UTF-8', errors='ignore' ) as f_w:
            f_w.write(f'-- {s_date}\n')
            f_w.write('--sp_addextendedproperty sp_updateextendedproperty\n\n')
            for table in tables:
                f_w.write(table.get_table_fields_desc_sqlscript())
                f_w.write('\n')

        s_file = os.path.join(file_path, 'changed_tables_resouces_%s.sql' % s_date)
        with open(s_file, 'w', encoding='UTF-8', errors='ignore' ) as f_w:
            f_w.write(f'-- {s_date}\n')
            f_w.write('delete from SYS_TRANS_NM;\n\n')
            for table in tables:
                f_w.write(table.get_fileds_resources_SQL_RMPlus())
                f_w.write('\n')

        s_file = os.path.join(file_path, 'clear_tables_%s.sql' % s_date)
        with open(s_file, 'w', encoding='UTF-8', errors='ignore' ) as f_w:
            f_w.write(f'-- {s_date}\n')
            for table in tables:
                f_w.write(table.generate_table_clear_sql())
                f_w.write('\n')

        # s_file = os.path.join(file_path, 'messages_en_US_%s.properties' % s_date)
        # with open(s_file, 'w', encoding='UTF-8', errors='ignore' ) as f_w:
        #     for table in tables:                
        #         f_w.write(table.get_fileds_resources_RMPlus())        

        # s_file = os.path.join(file_path, 'messages_zh_CN_%s.properties' % s_date)
        # with open(s_file, 'w', encoding='UTF-8', errors='ignore' ) as f_w:
        #     for table in tables:                
        #         f_w.write(table.get_fileds_resources_RMPlus('cn'))


        for table in tables:
        #     s_file = os.path.join(file_path, f'{table.table_name}.tbl')
        #     table.generate_tbl_file(s_file)
        #     s_file = os.path.join(file_path, f'{table.table_name}.ptn')
        #     table.generate_ptn_file(s_file)
        #     s_file = os.path.join(file_path, f'{table.table_name}.cpp')
        #     table.generate_class_code(s_file)
        #     s_file = os.path.join(file_path, f'{table.table_name}.sql')
        #     table.generate_sql_file(s_file)

            # #类定义-不需要了
            # s_class = 'java_class\\'
            # s_folder = os.path.join(file_path, f'{s_class}')
            # if not os.path.exists(s_folder):
            #     os.makedirs(s_folder, mode=0o777, exist_ok=True)
            # s_file = os.path.join(s_folder, f'{table.get_table_class_name_java()}Entity.java')
            # table.generate_class_file_java(s_file)

            #资源化文件
            s_table = f'i18n\\table\\{table.table_name.lower()}\\'
            s_folder = os.path.join(file_path, f'{s_table}')
            if not os.path.exists(s_folder):
                os.makedirs(s_folder, mode=0o777, exist_ok=True)
            s_file = os.path.join(s_folder, 'messages_en_US.properties')
            with open(s_file, 'w', encoding='UTF-8', errors='ignore' ) as f_w:
                f_w.write(table.get_fileds_resources_RMPlus())
            s_file = os.path.join(s_folder, 'messages_zh_CN.properties')
            with open(s_file, 'w', encoding='UTF-8', errors='ignore' ) as f_w:
                f_w.write(table.get_fileds_resources_RMPlus('cn'))

            # 数据字典 - json格式
            s_new = ''
            if table.isnew:
                s_new = 'new\\'
            s_module = table.table_name[0:3].upper() + "\\"
            s_folder = os.path.join(file_path, f'tables\\{s_module}')
            if not os.path.exists(s_folder):
                os.makedirs(s_folder, mode=0o777, exist_ok=True)
            s_file = os.path.join(s_folder, f'{table.table_name}.json')
            with open(s_file, 'w', encoding='UTF-8', errors='ignore' ) as f_w:
                f_w.write(table.get_table_dictionary_RMPlus())

        dorpdowns = self.get_changed_tables()[1]
        self.get_dropdown_scripts(file_path, dorpdowns)

        self.get_table_relations(file_path, tables)


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
    x = CreateRMPlusScriptByExcel(r'D:\Working\01WorkDocuments\OEMDocuments\RMPlusDocs\2023.01\Temp\RMPlus数据表设计-Jalon.xlsx')
    #x.read_excel()
    #x.read_excel_create_resource(r'D:\Documents\OEMDocuments\RMDocs\RM65APU2\temp.txt')
    s_saveto = r'D:\Working\02WeeklyWorking\0ThisWeek\Temp'
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


    