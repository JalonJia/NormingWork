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
    t_boolean = 7


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

    def get_define_code(self, s_table_name):
        '''
        生成字段C++的定义
        '''
        field_type = ''
        field_size = ''
        if self.type.lower() == 'string':
            field_type = 'CHAR'
            field_size = '[%s_SIZ(%s) + 1]' % (s_table_name, self.field_name.upper())
        elif self.type.lower() == 'number':
            field_type = 'DBSNUMBER'
            field_size = '[%s_SIZ(%s)]' % (s_table_name, self.field_name.upper())
        elif self.type.lower() == 'date':
            field_type = 'DBSDATE'
        elif self.type.lower() == 'time':
            field_type = 'DBSTIME'
        elif self.type.lower() == 'integer':
            field_type = 'DBSINT'
        elif self.type.lower() == 'long':
            field_type = 'DBSLONG'
        elif self.type.lower() == 'boolean':
            field_type = 'DBSBOOL'

        define_code = '    %s %s%s%s;' % (field_type, self.type.lower()[0], self.field_name.upper(), field_size)

        return define_code 

    def get_init_code(self, s_table_name):
        '''
        生成字段C++的定义
        '''
        field_varname = self.type.lower()[0] + self.field_name.upper()
        field_init = ''
        if self.type.lower() == 'string':
            field_init = 'strCopy(%s, "")' % (field_varname)
        elif self.type.lower() == 'number':
            field_init = 'bcdInit(%s, %s_SIZ(%s))' % (field_varname, s_table_name, self.field_name.upper())
        elif self.type.lower() == 'date':
            field_init = 'dateInit(%s)' % (field_varname)
        elif self.type.lower() == 'time':
            field_init = 'dtBCDTimeInit(%s)' % (field_varname)
        elif self.type.lower() == 'integer':
            field_init = '%s = 0' % (field_varname)
        elif self.type.lower() == 'long':
            field_init = '%s = 0' % (field_varname)
        elif self.type.lower() == 'boolean':
            field_init = '%s = FALSE' % (field_varname)

        init_code = '        %s;' % (field_init)

        return init_code 


    def get_getvalue_code(self, s_table_name):
        '''
        生成字段C++的如下代码：vView.Get(FIELD_IDX, &field_value);
        '''
        upper_field = self.field_name.upper()
        field_varname = self.type.lower()[0] + upper_field
        field_idx = '%s_IDX(%s)' % (s_table_name, upper_field)
        addr_flag = '' #&符号
        if self.type.lower() == 'integer' or self.type.lower() == 'long' or self.type.lower() == 'boolean':
            addr_flag = '&'

        get_str = 'Get'
        if self.type.lower() == 'string':
            get_str = 'GetString'

        field_code = '        m_v%s.%s(%s, %sm_%sValues.%s);' % (s_table_name, get_str, field_idx, addr_flag, s_table_name, field_varname)
        return field_code 

    def get_putvalue_code(self, s_table_name):
        '''
        生成字段C++的如下代码：vView.Put(FIELD_IDX, field_value);
        '''
        upper_field = self.field_name.upper()
        field_varname = self.type.lower()[0] + upper_field
        field_idx = '%s_IDX(%s)' % (s_table_name, upper_field)
        field_code = '        m_v%s.Put(%s, m_%sValues.%s);' % (s_table_name, field_idx, s_table_name, field_varname)
        return field_code 

class Table(object):
    '''
    定义Table的数据结构
    '''

    def __init__(self, s_table_name, s_table_desc='', s_key_desc='', b_created = False):
        '''
        Constructor
        '''
        self.table_name = s_table_name
        self.table_desc = s_table_desc
        self.key_desc = s_key_desc
        self.fields = []
        self.b_created = b_created


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


    def get_table_patten(self):
        '''
        得到表结构的ptn内容
        '''
        if len(self.table_desc) == 0:
            return ''

        s_ptn =  'CPPVIEW                     ; pattern type (C++ template)\n'
        s_ptn += 'AAAA=%-23s; application id - symbolic constants\n' % self.table_name[:2]
        s_ptn += 'aaaa=%-23s; application id - filenames\n' % self.table_name[:2].lower()
        s_ptn += 'ZZZZ=%-23s; view name - symbolic constants and module name\n' % self.table_name
        s_ptn += 'zzzz=%-23s; view name - filenames\n' % self.table_name.lower()
        s_ptn += 'xxxx=%-23s; view name - view routine prefix\n' % self.table_name.lower()
        s_ptn += "dddd='Copyright (c) 2019, Norming Software International Ltd.'\n"
        s_ptn += '                            ; copyright notice or view description\n'
        s_ptn += 'tttt=%-23s; table name\n' % self.table_name
        tbl_chars = list(self.table_name)
        s_ptn += "pppp={"
        i = 0
        for c in tbl_chars:
            if i > 0:
                s_ptn += ","
            s_ptn += f"'{c}'"
            i += 1
        
        for i in range(i, 8):
            s_ptn += f",' '"
        s_ptn += "}\n"
        s_ptn += '                            ; table name - padded to eight characters\n'

        return s_ptn


    def get_fileds_desc(self):
        '''
        得到表的字段描述
        '''
        s_fields_desc = ''
        if self.table_desc > '':
            s_fields_desc += f'\n#include "{self.table_name}.i"\n'            
            res_str = 'IDS_%s_VIEW_NAME%s,        "%s"\n' % (self.table_name, ' ' * (15-len(self.table_name)), self.table_desc)
            #print(res_str)
            s_fields_desc += res_str
            res_str = 'IDS_%s_VIEW_NOUN%s,        "%s"\n' % (self.table_name, ' ' * (15-len(self.table_name)), self.table_desc)
            #print(res_str)
            s_fields_desc += res_str
            res_str = 'IDS_%s_KEY_NAME%s,        "%s"\n' % (self.table_name, ' ' * (16-len(self.table_name)), self.table_desc)
            #print(res_str)
            s_fields_desc += res_str

        for field in self.fields:            
            res_str = 'IDS_%s_%s_FLD%s,        "%s"\n' % (self.table_name, field.field_name, ' ' * (20-len(self.table_name)-len(field.field_name)), field.desc)
            #print(res_str)
            s_fields_desc += res_str

        print(s_fields_desc)
        return s_fields_desc

    def get_table_class_code(self):
        '''
        得到表结构的c++ class文件
        '''
        s_code = 'class %sValues{\npublic:\n' % self.table_name.upper()
        s_init_code = '    %sValues()\n    {\n' % self.table_name.upper()
        s_getvalue_code = '    Get%sValuesFromView(NormingView& m_v%s, %sValues& m_%sValues)\n    {\n' % (
            self.table_name.upper(), self.table_name.upper(), self.table_name.upper(), self.table_name.upper())
        s_putvalue_code = '    Put%sValuesToView(NormingView& m_v%s, %sValues&  m_%sValues)\n    {\n' % (
            self.table_name.upper(), self.table_name.upper(), self.table_name.upper(), self.table_name.upper())

        for field in self.fields:                
            s_code += field.get_define_code(self.table_name.upper())
            s_code += '\n'
            s_init_code += field.get_init_code(self.table_name.upper())
            s_init_code += '\n'
            s_getvalue_code += field.get_getvalue_code(self.table_name.upper())
            s_getvalue_code += '\n'
            s_putvalue_code += field.get_putvalue_code(self.table_name.upper())
            s_putvalue_code += '\n'

        s_init_code += '    }\n\n'
        s_getvalue_code += '    }\n\n'
        s_putvalue_code += '    }\n\n'
        s_code = s_code + '\n' + s_init_code + s_getvalue_code + s_putvalue_code + '};\n'

        return s_code


    def generate_tbl_file(self, s_file_path):
        '''
        生成tbl文件
        '''
        s_tbl = self.get_table_define()
        if len(s_tbl) == 0:
            return 
        
        with open(s_file_path, 'w', encoding='UTF-8', errors='ignore' ) as f_w:
            f_w.write(s_tbl)


    def generate_ptn_file(self, s_file_path):
        '''
        生成ptn文件
        '''
        s_ptn = self.get_table_patten()
        if len(s_ptn) == 0:
            return 
        
        with open(s_file_path, 'w', encoding='UTF-8', errors='ignore' ) as f_w:
            f_w.write(s_ptn)
    
    def generate_class_code(self, s_file_path):
        '''
        生成c++ class代码文件
        '''
        s_code = self.get_table_class_code()
        if len(s_code) == 0:
            return 
        
        with open(s_file_path, 'w', encoding='UTF-8', errors='ignore' ) as f_w:
            f_w.write(s_code)
    
