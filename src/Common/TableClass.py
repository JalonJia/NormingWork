'''
TODO: 提供以下功能：
1. 定义数据表结构
2. 将数据表结构输出为格式化的字符串
'''
from enum import Enum

class FieldType(Enum):
    t_string = 1
    t_integer = 2
    t_long = 3
    t_number = 4
    t_date = 5
    t_time = 6


class Field(object):
    '''
    定义字段
    '''
    def __init__(self, s_field_name = '', s_type = 'string', i_length = 0, i_decimal = 0, s_desc = '', s_mask_list = '', b_is_key = False):
        self.field_name = s_field_name.lower()
        self.type = s_type.lower()
        if self.type == 'bcd':
            self.type = 'number'
        self.length = i_length
        self.decimal = i_decimal
        self.desc = s_desc
        self.mask_or_list = s_mask_list
        self.is_key = b_is_key
    

    def __str__(self):
        '''
        生成与以下标题对齐的字符串
        ##___C-name______C-type______name________type_____elements_____________decimals____validator_____presents_____________flags__________attributes_____________
        '''
        str = ''
        ##C-name______C-type______name________type_____
        str += ('%-4s%-12s%-12s%-12s%-9s' % ('*', self.field_name.lower(), '-', self.field_name.upper(), self.type.lower()))

        #elements_____________
        if self.type.lower() in 'string|number':
            str += '%-21d' % self.length
        else:
            str += '%-21s' % '-'
        
        #decimals____
        if self.type.lower() == 'number':
            str += '%-12d' % self.decimal
        else:
            str += '%-12s' % '-'
        
        if self.mask_or_list > '':
            #validator_____
            str += '%-14s' % '-'
            #presents_____________
            str += '%-21s' % self.mask_or_list

        return str


class Table(object):
    '''
    定义Table的数据结构
    '''

    def __init__(self, s_table_name, s_table_desc='', s_key_desc=''):
        '''
        Constructor
        '''
        self.table_name = s_table_name
        self.table_desc = s_table_desc
        self.key_desc = s_key_desc
        self.fields = []


    def add_field(self, field):
        '''
        增加字段
        '''
        self.fields.append(field)


    def remove_field(self, field_name):
        '''
        删除字段
        '''
        for f in self.fields[:]:
            if f.field_name == field_name:
                self.fields.remove(f)


    def get_table_define(self):
        '''
        得到表结构的tbl内容，不包括字段描述
        '''
        b_split_key = False 
        s_tbl = '#___C-name______C-type______name________type_____elements_____________decimals____validator_____presents_____________flags__________attributes_____________\n'

        for field in self.fields:
            if not b_split_key and field.is_key == False:
                s_tbl += '!   audt_Date   -           AUDTDATE    date     -                    -\n'
                s_tbl += '!   audt_Time   -           AUDTTIME    time     -                    -\n'
                s_tbl += '!   audt_User   -           AUDTUSER    string   SIZEOF_USERID        -\n'
                s_tbl += '!   audt_Org    -           AUDTORG     string   SIZEOF_ORGID         -\n'
                b_split_key = True
                
            s_tbl += str(field)
            s_tbl += '\n'
        return s_tbl


    def get_fileds_desc(self):
        '''
        得到表的字段描述
        '''
        s_fields_desc = f'#include "{self.table_name}.i"\n'
        #file.write(f'#include "{self.table_name}.i"\n')
        
        res_str = 'IDS_%s_VIEW_NAME%s,        "%s"\n' % (self.table_name, ' ' * (15-len(self.table_name)), self.table_desc)
        print(res_str)
        s_fields_desc += res_str
        #file.write(res_str)
        res_str = 'IDS_%s_VIEW_NOUN%s,        "%s"\n' % (self.table_name, ' ' * (15-len(self.table_name)), self.table_desc)
        print(res_str)
        s_fields_desc += res_str
        #file.write(res_str)

        for field in self.fields:            
            res_str = 'IDS_%s_%s_FLD%s,        "%s"\n' % (self.table_name, field.field_name, ' ' * (20-len(self.table_name)-len(field.field_name)), field.desc)
            print(res_str)
            s_fields_desc += res_str
            #file.write(res_str)

        return s_fields_desc


    def generate_tbl_file(self, s_file_path):
        '''
        生成tbl文件
        '''
        s_tbl = self.get_table_define()
        if len(s_tbl) == 0:
            return 
        
        with open(s_file_path, 'w', encoding='UTF-8', errors='ignore' ) as f_w:
            f_w.write(s_tbl)

    
