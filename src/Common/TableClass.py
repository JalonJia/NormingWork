'''
TODO: 提供以下功能：
1. 定义数据表结构
2. 将数据表结构输出为格式化的字符串
3. 生成HR的数据字典xml文件
'''
from enum import Enum
from os import replace
from re import split

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
    def __init__(self, s_field_name = '', s_type = 'string', i_length = 0, i_decimal = 0, s_desc = '', s_mask_list = '', b_is_key = False, s_desc2 = '', s_default = ''):
        self.field_name = s_field_name.lower()
        self.type = s_type.lower()
        if self.type == 'bcd' or self.type == 'decimal':
            self.type = 'number'
        self.length = i_length
        self.decimal = i_decimal
        self.desc = s_desc
        self.desc2 = s_desc2
        self.mask_or_list = s_mask_list
        self.is_key = b_is_key
        self.default = s_default
  

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
        

    def get_sql_script(self):
        '''
        生成创建此字段的SQL语句，类似于
        LVLEAVEWF_REQID             		NVARCHAR(36)     	DEFAULT '' NOT NULL,
        LVLEAVEWF_LINENUM           		INT     			DEFAULT 1 NOT NULL,
        LVLEAVEWF_CREATEDT 		   	 		DATETIME       	 	DEFAULT GETDATE(),
        LVLEAVEWF_CREATEBY 		    		NVARCHAR(36)     	DEFAULT '',
        LVLEAVEWF_WFID              		NVARCHAR(36)     	DEFAULT '', 
        LVLEAVEWF_WFUSER            		NVARCHAR(36)     	DEFAULT '',
        LVLEAVEWF_WFDATE            		DATETIME        	DEFAULT GETDATE(),
        LVLEAVEWF_WFACTION          		NVARCHAR(36)     	DEFAULT '',-- 1 Request 2 Approve 3 Reject 8 Cancel
        LVLEAVEWF_WFTIME            		NVARCHAR(36)     	DEFAULT '',
        LVLEAVEWF_LINENOTES         		NVARCHAR(1024)    	DEFAULT '', 
        LVLEAVEWF_LSTMNTDT 					DATETIME 			DEFAULT GETDATE(),
        LVLEAVEWF_LSTMNTBY 					NVARCHAR(36) 		DEFAULT '',
        '''

        s_type_name = self.type.upper()
        if self.type.lower() == 'number':
            s_type_name = 'DECIMAL(%-d, %-d)' % (self.length, self.decimal)
        elif self.type.lower() in 'string|nvarchar':
            s_type_name = 'NVARCHAR(%-d)' % self.length

        s_default = self.default
        if self.type.lower() == 'datetime':
            s_default = s_default.replace('#', '').replace('-', '')
        elif self.type.lower() in 'string|nvarchar' and (len(s_default) == 0):
            s_default = "''"
        elif len(s_default) == 0:
            s_default = '0'

        s_allownull = ''
        if self.is_key:
            s_allownull = 'NOT NULL'

        s_sql = ('%-4s%-36s%-24s%-8s%-16s%-16s' % (' ', self.field_name.upper(), s_type_name, 'DEFAULT', s_default, s_allownull)).rstrip()

        return s_sql


    def get_dictionary_script(self, iIndex = 0):
        '''
        生成字段的数据字典，类似于
        <column>
        <index>5</index>
        <name>LVLEAVE_LVFLAG</name>
        <description>Banked Overtime,0:No, 1:Yes</description>
        <description_cn>是否倒休，0:否, 1:是</description_cn>
        <type>int</type>
        <initialValue>0</initialValue>
        <allownulls>true</allownulls>
        <mask></mask>
        <attribute></attribute>
        </column>
        '''

        s_type_name = self.type.lower()
        s_size = ''
        s_precision = ''
        if self.type.lower() == 'number':
            s_type_name = 'decimal'
            s_size = '\n    <size>%s</size>' % self.length
            s_precision = '\n    <precision>%s</precision>' % self.decimal
        elif self.type.lower() in 'string|nvarchar':
            s_type_name = 'varchar'
            s_size = '\n    <size>%d</size>' % self.length

        s_default = self.default
        if self.type.lower() in 'datetime|string|nvarchar':
            s_default = self.default
        elif len(s_default) == 0:
            s_default = '0'

        s_allownull = 'true'
        if self.is_key:
            s_allownull = 'false'  

        s_dictionary = '''<column>
    <index>%d</index>
    <name>%s</name>
    <description>%s</description>
    <description_cn>%s</description_cn>
    <type>%s</type>%s%s
    <initialValue>%s</initialValue>
    <allownulls>%s</allownulls>
    <mask></mask>
    <attribute></attribute>
</column>        
''' % (iIndex, self.field_name.upper(), self.desc.rstrip(), self.desc2.rstrip(), s_type_name, s_size, s_precision, s_default, s_allownull)

        return s_dictionary

    def get_upgrade_sql(self):
        '''
        生成Upgrade此字段的SQL语句，类似于
        UPGRADE LVLEAVEWF SET LVLEAVEWF_REQID='';
        '''

        s_default = self.default
        if self.type.lower() == 'datetime':
            s_default = s_default.replace('#', '').replace('-', '')
        elif self.type.lower() in 'string|nvarchar' and (len(s_default) == 0):
            s_default = "''"
        elif len(s_default) == 0:
            s_default = '0'

        s_sql = ('SET %s = %s' % (self.field_name.upper(), s_default)).rstrip()

        return s_sql


class Table(object):
    '''
    定义Table的数据结构
    '''

    def __init__(self, s_table_name, s_table_desc='', s_key_desc='', b_created = False, s_table_desc2='', b_new = False):
        '''
        Constructor
        '''
        self.table_name = s_table_name
        self.table_desc = s_table_desc
        self.table_desc2 = s_table_desc2 #中文描述
        self.key_desc = s_key_desc
        self.fields = []
        self.b_created = b_created
        self.isnew = b_new


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


    def get_table_sqlscript(self):
        '''
        得到表结构的tbl内容，不包括字段描述
        '''

        if len(self.fields) == 0:
            return ''

        b_split_key = False
        s_keys = ''
        
        s_script = ''
        if self.isnew:
            s_script += "IF EXISTS (SELECT * FROM dbo.sysobjects WHERE id = object_id(N'%s') AND objectproperty(id, N'IsUserTable') = 1)\n" % self.table_name.upper()
            s_script += "DROP TABLE %s;\n\n" % self.table_name.upper()
            s_script += "CREATE TABLE %s(\n" % self.table_name.upper()


        for field in self.fields:
            if not b_split_key and field.is_key == False:
                b_split_key = True
            
            if field.is_key:
                if len(s_keys)>0:
                    s_keys += ', '
                s_keys += field.field_name.upper()

            if self.isnew:
                s_script += field.get_sql_script()
                s_script += ',\n'
            else:
                s_script += 'alter table %-16s add %s;\n' % (self.table_name.upper(), field.get_sql_script())
            

        if self.isnew:
            s_primary_key = '%-4sPRIMARY KEY (%s)\n' % (' ', s_keys)
            s_script += s_primary_key
            s_script += ");\n"

        return s_script

    def get_table_upgradesql(self):
        '''
        得到表结构的Upgrade语句
        '''

        if len(self.fields) == 0 or self.isnew:
            return ''

        s_upgrade_sql = ''
        
        for field in self.fields:
            s_upgrade_sql += 'UPDATE %s %s;\n' % (self.table_name, field.get_upgrade_sql())
            
        return s_upgrade_sql


    def get_table_dictionary(self):
        '''
        得到HR表结构的数据字典
        '''

        if len(self.fields) == 0:
            return ''

        b_split_key = False 
        s_keys = ''
        i_index = 1
        
        s_script = ''
        if self.isnew:
            s_script += '<?xml version="1.0" encoding="UTF-8"?>'
            s_script += "\n<table>"
            s_script += "\n<description>%s</description><columns>\n" % self.table_desc2

        for field in self.fields:
            if not b_split_key and field.is_key == False:
                b_split_key = True
            
            if field.is_key:
                s_keys += '''<column>
    <colname>%s</colname>
    <ascdesc>ASC</ascdesc>
</column>
''' % field.field_name.upper()

            s_script += field.get_dictionary_script(i_index)
            i_index += 1
           

        if self.isnew:
            s_primary_key = '''</columns><constraint><primarykey>
<pkconstraintname>%s_KEY_0</pkconstraintname><columns>
%s</columns></primarykey></constraint></table>
''' % (self.table_name.upper(), s_keys)
            s_script += s_primary_key

        return s_script


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
    

    def generate_sql_file(self, s_file_path):
        '''
        生成创建表的sql文件
        '''
        s_sql = self.get_table_sqlscript()
        if len(s_sql) == 0:
            return 
        
        with open(s_file_path, 'w', encoding='UTF-8', errors='ignore' ) as f_w:
            f_w.write(s_sql)


class Security(object):
    '''
    定义权限的数据结构
    '''

    def __init__(self, s_name, s_desc='', s_desc2='', s_sequence='', b_created = False):
        '''
        Constructor
        '''
        self.sec_name = s_name
        self.sec_sequence = s_sequence
        self.sec_desc = s_desc
        self.sec_desc2 = s_desc2 #中文描述
        self.b_created = b_created


    def get_initsql(self):
        '''
        得到插入权限表的语句
        '''

        if len(self.sec_name) == 0 or self.b_created:
            return ''

        s_module = self.sec_name[:2]
        s_sql = "INSERT INTO ASSEC(ASSEC_MODULEID,ASSEC_SECID,ASSEC_SEQUENCE,ASSEC_SECDESC) VALUES('%s','%s',%s,'%s');" % (s_module, self.sec_name, self.sec_sequence, self.sec_desc)
            
        return s_sql


    def get_initgroup_sql(self):
        '''
        得到插入权限组的语句, 类似：
        INSERT INTO ASGRPSEC(ASGRPSEC_GRPID,ASGRPSEC_MODULEID,ASGRPSEC_SECID,ASGRPSEC_GRPDESC) VALUES('ADMIN','BK','BK074','Administrator');
        '''

        s_groups = [ 
            ['ADMIN', 'Administrator'], 
            ['HRM', 'HR Manager'], 
            ['FM', 'Financial Manager'], 
            ['GM', 'General Manager'], 
            # ['SALES', 'Sales'] 
        ]

        if len(self.sec_name) == 0 or self.b_created:
            return ''

        s_insert = 'INSERT INTO ASGRPSEC(ASGRPSEC_GRPID,ASGRPSEC_MODULEID,ASGRPSEC_SECID,ASGRPSEC_GRPDESC) VALUES'
        s_module = self.sec_name[:2]
        s_sql = ''
        for grp in s_groups:
            s_sql += "%s('%s','%s','%s','%s');\n" % (s_insert, grp[0], s_module, self.sec_name, grp[1])
            
        return s_sql
