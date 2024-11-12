'''
TODO: 提供以下功能：
1. 定义数据表结构
2. 将数据表结构输出为格式化的字符串
3. 生成HR的数据字典xml文件
'''
from enum import Enum
from os import replace
from re import split, sub
from datetime import date, datetime
import time
import json


class FieldType(Enum):
    t_string = 1
    t_integer = 2
    t_long = 3
    t_number = 4
    t_date = 5
    t_time = 6
    t_boolean = 7


class TableIndex(object):
    '''
    定义字段
    '''

    def __init__(self, s_index_fields='', b_is_unique=False,
                 s_desc='', s_desc2='', idx_seq=1):
        self.index_fields = s_index_fields.upper()
        self.desc = s_desc
        self.desc2 = s_desc2
        self.is_unique = b_is_unique
        self.seq = idx_seq

    def get_sql_script(self, s_table: str):
        '''
        生成创建此Index的SQL语句，类似于
        CREATE UNIQUE NONCLUSTERED INDEX [index4] ON [dbo].[LVEMPLEAVEY]
(
 	[TEST] ,	[LVEMPLEAVEY_EMPID] 
)  
        '''

        s_unique = ""
        if self.is_unique:
            s_unique = " UNIQUE"

        time.sleep(0.01)
        s_index_name = "IDX_" + str(self.seq) + "_" + s_table

        s_sql = """CREATE%s INDEX %s ON %s (%s);\n""" % (
            s_unique, s_index_name[0:30], s_table, self.index_fields
        )

        return s_sql


class DropdownList(object):
    '''
    定义下拉列表
    '''

    def __init__(self, s_list_name='', s_define=''):
        self.list_name = s_list_name.lower()
        self.list_values = {}

        key_values = s_define.splitlines()
        for element in key_values:
            if '-' in element:
                if element[0] == '-': #下拉列表值为负数，需要从右向左拆
                    self.list_values[element.rsplit('-', 1)[0].strip()] = element.rsplit('-', 1)[1].strip()
                else:
                    self.list_values[element.split('-', 1)[0].strip()] = element.split('-', 1)[1].strip()

        #特殊情况
        if self.list_name == 'yes_no':
            self.list_values["0"] = 'No'
            self.list_values["1"] = 'Yes'

        if self.list_name == 'yes_no_na':
            self.list_values["0"] = 'No'
            self.list_values["1"] = 'Yes'
            self.list_values["2"] = 'NA'


    def get_json_context(self):
        '''生成类似以下的脚本："yes_no": ["0","1"]'''
        key_list = list(self.list_values.keys())
        s_json = (f'"{self.list_name}": {key_list}').replace("'", '"')
        return s_json

    def get_json_res_eng(self):
        '''生成类似以下的脚本：dict.yes_no.0=No '''
        s_json = ''
        for v, s in self.list_values.items():
            s_json += f'dict.{self.list_name}.{v}={s}\n'
        return s_json

    def get_resources_SQL_RMPlus(self):
        '''
        得到表的资源化SQL语句, 类似于
        INSERT INTO SYS_TRANS_NM(RESOURCE_ID, CREATE_BY, UPDATE_BY, RESOURCE_ENG, RESOURCE_CHN, RESOURCE_CHT,
        RESOURCE_FRA, RESOURCE_ESN, MODULE_CODE, CATEGORY, APP_TYPE)
        VALUES ('%s', 'SYSTEM', 'SYSTEM', '%s', '%s', '%s', '%s', '%s', '%s', 'Dict', 0);
        '''

        s_fields_sql = ''
        s_module = ''

        for v, s in self.list_values.items():
            s_drop_key = f"dict.{self.list_name}.{v}"
            s_fmt_desc_en = s.replace("'", "''")
            s_fmt_desc_cn = s_fmt_desc_en
            s_one_sql = (
                            "INSERT INTO SYS_TRANS_NM(RESOURCE_ID, CREATE_BY, UPDATE_BY, RESOURCE_ENG, RESOURCE_CHN, RESOURCE_CHT, "
                            "RESOURCE_FRA, RESOURCE_ESN, MODULE_CODE, CATEGORY, APP_TYPE) "
                            "VALUES ('%s', 'SYSTEM', 'SYSTEM', '%s', '%s', '%s', '%s', '%s', '%s', 'Dict', 0);\n") % (
                            s_drop_key,
                            s_fmt_desc_en, s_fmt_desc_cn, s_fmt_desc_en, s_fmt_desc_en, s_fmt_desc_en,
                            s_module
                        )
            s_fields_sql += s_one_sql

        # print(s_fields_sql)
        return s_fields_sql

class Field(object):
    '''
    定义字段
    '''

    def __init__(self, s_field_name='', s_type='string', i_length=0, i_decimal=0, s_desc='',
                 s_mask_list='', b_is_key=False, s_desc2='', s_default='', b_not_null=False,
                 s_mask='', s_list_name=''):
        self.field_name = s_field_name.upper()
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
        self.not_null = b_not_null
        self.mask = s_mask
        self.list_name = s_list_name

    def __str__(self):
        '''
        生成与以下标题对齐的字符串
        ##___C-name______C-type______name________type_____elements_____________decimals____validator_____presents_____________flags__________attributes_____________
        '''

        str = ''
        ##C-name______C-type______name________type_____
        str += ('%-4s%-12s%-12s%-12s%-9s' % (
        '*', self.field_name.lower(), '-', self.field_name.upper(), self.type.lower()))

        # elements_____________
        if self.type.lower() in 'string|number':
            str += '%-21d' % self.length
        else:
            str += '%-21s' % '-'

        # decimals____
        if self.type.lower() == 'number':
            str += '%-12d' % self.decimal
        else:
            str += '%-12s' % '-'

        if self.mask_or_list > '':
            # validator_____
            str += '%-14s' % '-'
            # presents_____________
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
        elif self.type.lower() == 'bigint':
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
        addr_flag = ''  # &符号
        if self.type.lower() == 'integer' or self.type.lower() == 'long' or self.type.lower() == 'boolean':
            addr_flag = '&'

        get_str = 'Get'
        if self.type.lower() == 'string':
            get_str = 'GetString'

        field_code = '        m_v%s.%s(%s, %sm_%sValues.%s);' % (
        s_table_name, get_str, field_idx, addr_flag, s_table_name, field_varname)
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
        LVLEAVEWF_REQID             		NVARCHAR(36)     	DEFAULT '' NOT NULL     comment '部门id',
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
        if self.type.lower() in 'number|bcd':
            s_type_name = 'DECIMAL(%-d, %-d)' % (self.length, self.decimal)
        elif self.type.lower() in 'string|nvarchar|varchar|text':
            s_type_name = 'NVARCHAR(%-d)' % self.length
        elif self.type.lower() == 'ntext':
            s_type_name = 'NVARCHAR(MAX)'
        elif self.type.lower() == 'blob':
            s_type_name = 'VARBINARY(MAX)'
        elif self.type.lower() in 'int|integer|smallint|boolean':
            s_type_name = 'INT'
        elif self.type.lower() in 'long|bigint':
            s_type_name = 'BIGINT'

        s_default = self.default
        if self.type.lower() == 'datetime':
            s_default = s_default.replace('#', '').replace('-', '')
            if len(s_default) == 0:
                s_default = '0'
        elif self.type.lower() in 'string|nvarchar|ntext|varchar|text':
            if (len(s_default) == 0):
                s_default = "''"
            elif ('#' in s_default) or ('(' in s_default):
                pass
            else:
                s_default = f"'{self.default}'"
        elif self.type.lower() in 'int|integer|long|bigint|smallint|boolean':
            if len(s_default) == 0:
                s_default = '0'
            else:
                s_default = str(self.default.split('.')[0])
        elif len(s_default) == 0:
            s_default = '0'

        s_default_out = 'DEFAULT ' + s_default
        if s_type_name == 'VARBINARY(MAX)':
            s_default_out = ''

        s_allownull = ''
        if self.is_key or self.not_null:
            s_allownull = 'NOT NULL'

        # if self.not_null:
        #     s_default_out = 'NOT NULL'

        s_sql = ('%-4s%-32s%-20s%-24s%-8s' % (' ', self.field_name.upper(), s_type_name, s_default_out, s_allownull))

        return s_sql

    def get_field_desc_script(self, s_table_name):
        '''
        生成字段的备注，类似于
        EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Test ID' , 
        @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'test1', 
        @level2type=N'COLUMN',@level2name=N'test_id';
        '''

        s_sql = ''
        if len(self.desc) > 0:
            s_fmt_desc = self.desc.replace("'", "''")
            s_sql = "EXEC sys.sp_addextendedproperty N'MS_Description', N'%s' , N'SCHEMA', N'dbo', N'TABLE', N'%s', N'COLUMN', N'%s';\n" \
                    % (s_fmt_desc, s_table_name, self.field_name.upper())

        return s_sql

    def get_field_var_name_java(self):
        '''
        生成字段对应的驼峰式Jave变量名，例如"USER_ID"对应userId
        '''
        return sub('_([a-zA-Z])', lambda m: (m.group(1).upper()), self.field_name.lower())

    def get_field_define_java(self):
        '''
        生成字段的java定义，类似于
        public static final String userId = "user_id";
        '''

        s_def = ''
        if len(self.field_name) > 0:
            s_def_name = self.get_field_var_name_java()
            s_def = "        public static final String %s = '%s';\n" \
                    % (s_def_name, self.field_name.upper())

        return s_def

    def get_field_getset_method_java(self, s_table_class_name):
        '''
        生成字段的java Get/Set方法，类似于
        public Long getUserId() {
            return super.getLong(Columns.userId);
        }

        public SysUserEntity setUserId(Long userId) {
            super.set(Columns.userId, userId);
            return this;
        }        
        '''

        s_java_type = self.type.lower()
        if s_java_type == 'bigint':
            s_java_type = 'Long'
        elif s_java_type in 'number|decimal|bcd':
            s_java_type = 'Double'
        elif self.type.lower() in 'date|time|datetime':
            s_java_type = 'Date'
        elif self.type.lower() in 'integer|int':
            s_java_type = 'Integer'
        elif self.type.lower() in 'string|nvarchar|ntext|varchar|text':
            s_java_type = 'String'
        elif s_java_type == 'blob':
            s_java_type = 'byte[]'

        s_java_type = s_java_type[0: 1].upper() + s_java_type[1:]
        s_def_name = self.get_field_var_name_java()
        s_def_name2 = s_def_name[0: 1].upper() + s_def_name[1:]
        s_java_type2 = s_java_type.replace('[', '').replace(']', '')

        s_def = '''\n
    public %s get%s() {
        return super.get%s(Columns.%s);
    }

    public %sEntity set%s(%s %s) {
        super.set(Columns.%s, %s);
        return this;
    }
        ''' % (s_java_type, s_def_name2,
               s_java_type2, s_def_name,
               s_table_class_name, s_def_name2, s_java_type, s_def_name,
               s_def_name, s_def_name)

        return s_def

    def get_field_reources_RMPlus(self, s_table_name, s_language='en'):
        '''
        table.enrqn.xxtablename=采购表
        table.enrqn.docno=单据号
        '''

        if s_language == 'en':
            s_reource = 'table.%s.%s=%s' % (s_table_name.rstrip().lower(), self.field_name.lower(), self.desc)
        elif s_language == 'cn':
            s_reource = 'table.%s.%s=%s' % (s_table_name.rstrip().lower(), self.field_name.lower(), self.desc2)
        else:
            s_reource = 'table.%s.%s=%s' % (s_table_name.rstrip().lower(), self.field_name.lower(), self.desc)

        return s_reource

    def get_dictionary_script(self, iIndex=0):
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
''' % (iIndex, self.field_name.upper(), self.desc.rstrip(), self.desc2.rstrip(), s_type_name, s_size, s_precision,
       s_default, s_allownull)

        return s_dictionary

    def get_dictionary_script_RMPlus(self):
        '''
        生成创建此字段的json结构，类似于
    {
        "type":"datetime",
        "isKey": true,
        "fieldName":"UPDATE_TIME",
        "length":36,
        "precision": 0,
        "initialValue": "",
        "notNull": true,
        "mask": "%-36C",
        "dropdownList": "yes_no",
        "description": "记录创建时间"
    }
        '''

        s_type_name = self.type.upper()
        if self.type.lower() in 'number|bcd':
            s_type_name = 'DECIMAL' # 'DECIMAL(%-d, %-d)' % (self.length, self.decimal)
        elif self.type.lower() in 'string|nvarchar|varchar|text':
            s_type_name = 'NVARCHAR' #'NVARCHAR(%-d)' % self.length
        elif self.type.lower() == 'ntext':
            s_type_name = 'NVARCHAR' #'NVARCHAR(MAX)'
        elif self.type.lower() == 'blob':
            s_type_name = 'VARBINARY' #'VARBINARY(MAX)'
        elif self.type.lower() in 'int|integer|smallint|boolean':
            s_type_name = 'INT'
        elif self.type.lower() in 'long|bigint':
            s_type_name = 'BIGINT'

        s_default = f'"{self.default}"'
        if self.type.lower() == 'datetime':
            s_default = s_default.replace('#', '').replace('-', '')
            if len(self.default) == 0:
                s_default = '"0"'
        elif self.type.lower() in 'string|nvarchar|ntext|varchar|text':
            if (len(self.default) == 0):
                s_default = '""'
            elif ('#' in s_default) or ('(' in s_default):
                pass
            else:
                s_default = f'"{self.default}"'
        elif self.type.lower() in 'int|integer|long|bigint|smallint|boolean':
            if len(self.default) == 0:
                s_default = "0"
            else:
                s_default = '"' + str(self.default.split('.')[0]) + '"'
        elif len(s_default) == 0:
            s_default = '"0"'

        s_allownull = 'true'
        if self.is_key or self.not_null:
            s_allownull = 'false'

        # if self.not_null:
        #     s_default_out = 'NOT NULL'

        s_json = ("""    {
        "type": "%s",
        "isKey": %s,
        "fieldName": "%s",
        "length": %d,
        "precision": %d,
        "initialValue": %s,
        "notNull": %s,
        "mask": "%s",
        "dropdownList": "%s",
        "description": "%s"
    }""" %
                  (s_type_name, str(self.is_key).lower(), self.field_name.upper(),
                   self.length, self.decimal, s_default, s_allownull, self.mask, self.list_name, self.desc))

        return s_json

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

    def get_define_index_sql(self):
        '''
        生成HR中DEFINE_INDEX中字段对应的SQL语句，类似于
        insert into DEFINE_INDEX(MORE1,CAT1,CODE,MORE2,MORE3,DFILE,CAT2,DESCRIPTION,DTYPE,DCLOB,DDATA) 
        values('LVLEAVE','field','LVLEAVE_OPTIONAL','','','','','','s',
        '{"javaclass":"cn.com.norming.custom.define.field.BaseField","captionid":"LV/TAB/LVLEAVE/OPTIONAL",
        "selector":false,"precision":19,"idtype":"NotAId","entitycode":"LVLEAVE","beunique":false,"code":"LVLEAVE_OPTIONAL",
        "decimal":2,"hibcode":"lvleaveOptional","cat1":"field","$$_jc_":"cn.com.norming.custom.define.field.BaseField","cannull":true,
        "dtype":"s","datatype":"integer","datalen":255}'
        ,'');
        '''

        s_table = self.field_name.upper().split('_')[0]
        s_subfield = self.field_name.upper().split('_')[1]
        s_precision = '19'
        s_decimal = '2'
        s_datatype = self.type.lower()
        s_hibcode = s_table.title() + s_subfield.title()
        s_datalen = '255'

        if self.type.lower() == 'datetime':
            s_datatype = 'timestamp'
            s_datalen = 23
        elif self.type.lower() in 'string|nvarchar':
            s_datatype = 'string'
        elif self.type.lower() == 'number':
            s_datatype = 'double'
            s_precision = '18'
            s_decimal = self.decimal
        elif self.type.lower() == 'int':
            s_datatype = 'integer'

        s_define_index = """\
insert into DEFINE_INDEX(MORE1,CAT1,CODE,MORE2,MORE3,DFILE,CAT2,DESCRIPTION,DTYPE,DCLOB,DDATA) \
values('%s','field','%s','','','','','','s',\
'{"javaclass":"cn.com.norming.custom.define.field.BaseField","captionid":"%s/TAB/%s/%s",\
"selector":false,"precision":%s,"idtype":"NotAId","entitycode":"%s","beunique":false,"code":"%s",\
"decimal":%s,"hibcode":"%s","cat1":"field","$$_jc_":"cn.com.norming.custom.define.field.BaseField","cannull":true,\
"dtype":"s","datatype":"%s","datalen":%s}','');
""" % (s_table, self.field_name.upper(),
       self.field_name.upper()[:2], s_table, s_subfield,
       s_precision, s_table, self.field_name.upper(),
       s_decimal, s_hibcode,
       s_datatype, s_datalen
       )

        return s_define_index


class Table(object):
    '''
    定义Table的数据结构
    '''

    def __init__(self, s_table_name: str, s_table_desc='', s_key_desc='', b_created=False, s_table_desc2='',
                 b_new=False, b_setup=False):
        '''
        Constructor
        '''
        self.table_name = s_table_name
        self.table_desc = s_table_desc
        self.table_desc2 = s_table_desc2  # 中文描述
        self.key_desc = s_key_desc
        self.fields = []
        self.b_created = b_created
        self.isnew = b_new
        self.issetup = b_setup
        self.indexes = []

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

    def add_index(self, index: TableIndex):
        '''
        增加Index
        '''
        self.indexes.append(index)

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

        s_ptn = 'CPPVIEW                     ; pattern type (C++ template)\n'
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
            res_str = 'IDS_%s_VIEW_NAME%s,        "%s"\n' % (
            self.table_name, ' ' * (15 - len(self.table_name)), self.table_desc)
            # print(res_str)
            s_fields_desc += res_str
            res_str = 'IDS_%s_VIEW_NOUN%s,        "%s"\n' % (
            self.table_name, ' ' * (15 - len(self.table_name)), self.table_desc)
            # print(res_str)
            s_fields_desc += res_str
            res_str = 'IDS_%s_KEY_NAME%s,        "%s"\n' % (
            self.table_name, ' ' * (16 - len(self.table_name)), self.table_desc)
            # print(res_str)
            s_fields_desc += res_str

        for field in self.fields:
            res_str = 'IDS_%s_%s_FLD%s,        "%s"\n' % (
            self.table_name, field.field_name, ' ' * (20 - len(self.table_name) - len(field.field_name)), field.desc)
            # print(res_str)
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
        得到表结构的SQL语句，不包括字段描述
        '''

        if len(self.fields) == 0:
            return ''

        b_split_key = False
        s_keys = ''

        s_script = '\n'
        if self.isnew:
            s_script += "IF EXISTS (SELECT * FROM dbo.sysobjects WHERE id = object_id(N'%s') AND objectproperty(id, N'IsUserTable') = 1)\n" % self.table_name.upper()
            s_script += "DROP TABLE %s;\n\n" % self.table_name.upper()
            s_script += "CREATE TABLE %-40s-- %s\n" % (f"{self.table_name.upper()}(", self.table_desc)

        for field in self.fields:
            if not b_split_key and field.is_key == False:
                b_split_key = True

            if field.is_key:
                if len(s_keys) > 0:
                    s_keys += ', '
                s_keys += field.field_name.upper()

            s_fmt_mask_list = ""
            if len(field.mask_or_list) > 0:
                s_blanks = "        "[0: 3 - len(field.desc) % 3]
                s_fmt_mask_list = f"{s_blanks}-- {field.mask_or_list}".replace('\n', ', ').replace('ist,', 'ist:')

            if self.isnew:
                s_script += f"{field.get_sql_script()}, -- {field.desc}{s_fmt_mask_list}\n"
            else:
                s_script += 'alter table %-30s add %s;  -- %s%s\n' % (
                self.table_name.upper(), field.get_sql_script(), field.desc, s_fmt_mask_list)

        if self.isnew:
            s_primary_key = '%-4sPRIMARY KEY (%s)\n' % (' ', s_keys)
            s_script += s_primary_key
            s_script += ");\n"

        if len(self.indexes) > 0:
            s_script += '\n'

        for idx in self.indexes:
            s_script += idx.get_sql_script(self.table_name.upper())

        if self.table_name.upper() in ('EXP_REQD'):
            s_script += s_script.replace(self.table_name.upper(), self.table_name.upper()+'P')

        return s_script

    def get_table_upgradesql(self):
        '''
        得到表结构的Upgrade语句
        '''

        if len(self.fields) == 0 or self.isnew:
            return ''

        s_upgrade_sql = ''

        for field in self.fields:
            s_upgrade_sql += 'UPDATE %s %s;\n' % (self.table_name.upper(), field.get_upgrade_sql())

        return s_upgrade_sql

    def get_table_fields_desc_sqlscript(self):
        '''
        得到表结构字段描述的SQL语句
        '''

        if len(self.fields) == 0:
            return ''

        s_script = "\n"
        for field in self.fields:
            s_script += field.get_field_desc_script(self.table_name.upper())

        return s_script

    def get_table_dictionary_RMPlus(self):
        '''
        得到RM Plus表结构的数据字典, json格式
        '''

        if len(self.fields) == 0:
            return ''

        s_script = '''{
"tableName":"%s",
"description":"%s",
"columns": [\n''' % (self.table_name.upper(), self.table_desc)

        s_split1 = ''
        for field in self.fields:
            # 转换为JSON字符串
            # json_str = json.dumps(field.__dict__)

            # 转换为JSON对象
            # json_obj = json.loads(json_str)
            s_script = s_script + s_split1 + field.get_dictionary_script_RMPlus()
            s_split1 = ',\n'

        s_script += ']\n}'

        return s_script

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

    def get_table_define_index_hr(self):
        '''
        得到整个Table HR Define_Index的记录
        '''

        if len(self.fields) == 0:
            return ''

        s_script = ''
        for field in self.fields:
            s_script += field.get_define_index_sql()

        return s_script

    def get_fileds_resources_RMPlus(self, s_language='en'):
        '''
        得到表的资源化定义, 类似于
        table.enrqn=采购表
        table.enrqn.docno=单据号
        '''

        s_fields_desc = ''
        if s_language == 'en' and self.table_desc > '':
            s_reource = 'table.%s=%s\n' % (self.table_name.rstrip().lower(), self.table_desc)
            s_fields_desc += s_reource
        elif s_language == 'cn' and self.table_desc2 > '':
            s_reource = 'table.%s=%s\n' % (self.table_name.rstrip().lower(), self.table_desc2)
            s_fields_desc += s_reource

        for field in self.fields:
            s_fields_desc = s_fields_desc + field.get_field_reources_RMPlus(self.table_name, s_language) + "\n"

        # print(s_fields_desc)
        return s_fields_desc

    def get_fileds_resources_SQL_RMPlus(self):
        '''
        得到表的资源化SQL语句, 类似于
        INSERT INTO SYS_TRANS_NM(RESOURCE_ID, CREATE_BY, UPDATE_BY, RESOURCE_ENG, RESOURCE_CHN, RESOURCE_CHT, 
        RESOURCE_FRA, RESOURCE_ESN, MODULE_CODE, CATEGORY, APP_TYPE)
        VALUES ('%s', 'SYSTEM', 'SYSTEM', '%s', '%s', '%s', '%s', '%s', '%s', 'TABLE', 0);
        '''

        s_fields_sql = ''

        s_fmt_table = f"table.{self.table_name.rstrip().lower()}"
        s_fmt_desc_en = self.table_desc.replace("'", "''")
        s_fmt_desc_cn = self.table_desc2.replace("'", "''")
        s_module = self.table_name[0:3].upper()

        s_one_sql = (
                        "INSERT INTO SYS_TRANS_NM(RESOURCE_ID, CREATE_BY, UPDATE_BY, RESOURCE_ENG, RESOURCE_CHN, RESOURCE_CHT, "
                        "RESOURCE_FRA, RESOURCE_ESN, MODULE_CODE, CATEGORY, APP_TYPE) "
                        "VALUES ('%s', 'SYSTEM', 'SYSTEM', '%s', '%s', '%s', '%s', '%s', '%s', 'TABLE', 0);\n") % (
                        s_fmt_table,
                        s_fmt_desc_en, s_fmt_desc_cn, s_fmt_desc_en, s_fmt_desc_en, s_fmt_desc_en,
                        s_module
                    )

        s_fields_sql += s_one_sql

        for field in self.fields:
            s_fmt_field = f"{s_fmt_table}.{field.field_name.rstrip().lower()}"
            s_fmt_desc_en = field.desc.replace("'", "''")
            s_fmt_desc_cn = field.desc2.replace("'", "''")
            s_one_sql = (
                            "INSERT INTO SYS_TRANS_NM(RESOURCE_ID, CREATE_BY, UPDATE_BY, RESOURCE_ENG, RESOURCE_CHN, RESOURCE_CHT, "
                            "RESOURCE_FRA, RESOURCE_ESN, MODULE_CODE, CATEGORY, APP_TYPE) "
                            "VALUES ('%s', 'SYSTEM', 'SYSTEM', '%s', '%s', '%s', '%s', '%s', '%s', 'TABLE', 0);\n") % (
                            s_fmt_field,
                            s_fmt_desc_en, s_fmt_desc_cn, s_fmt_desc_en, s_fmt_desc_en, s_fmt_desc_en,
                            s_module
                        )
            s_fields_sql += s_one_sql

        # print(s_fields_sql)
        return s_fields_sql

    def get_table_class_name_java(self):
        '''
        生成表名对应的Jave类名，例如"sys_user"对应SysUserEntity
        '''
        s_name = sub('_([a-zA-Z])', lambda m: (m.group(1).upper()), self.table_name.lower())
        s_name = s_name[0: 1].upper() + s_name[1:]

        return s_name

    def get_table_class_define_java(self):
        '''
        生成字段的java类定义        
        '''

        s_class_name = self.get_table_class_name_java()
        s_table_name = self.table_name.upper()

        s_first_field = ''
        if len(self.fields) > 0:
            s_first_field = self.fields[0].get_field_var_name_java()

        s_fields_define = ''
        s_fields_getset_method = ''
        for field in self.fields:
            s_fields_define += field.get_field_define_java()
            s_fields_getset_method += field.get_field_getset_method_java(s_class_name)

        s_def = '''package com.norming.platform.system.entity.sys;

import com.norming.platform.dao.sql.Entity;

import java.io.Serializable;
import java.util.Date;

/**
 * %s %s %s
 */
public class %sEntity extends Entity implements Serializable {

    public static final string table = "%s";

    public %sEntity() {
        super(table, Columns.%s);
    }

    /**
     * 表字段定义
     */
    public static final class Columns {
%s
    }
%s
}
        ''' % (
            s_table_name, self.table_desc, self.table_desc2,
            s_class_name,
            s_table_name,
            s_class_name,
            s_first_field,
            s_fields_define,
            s_fields_getset_method
        )

        return s_def

    def get_table_desc(self):
        '''
        得到表名及描述，不包括字段描述
        '''

        s_def = """-- %-29s%-48s%s""" % (self.table_name.upper(), self.table_desc, self.table_desc2)
        if self.table_name.upper() in ('EXP_REQD'):
            s_def += """\n-- %-29s%-48s%s""" % (self.table_name.upper()+'P', self.table_desc, self.table_desc2)

        return s_def

    def generate_table_clear_sql(self):
        '''
        得到DELETE FROM TABLE_NAME; 的脚本
        '''

        s_def = """DELETE FROM %-29s; -- %-48s%s""" % (self.table_name.upper(), self.table_desc, self.table_desc2)
        if self.table_name.upper() in ('EXP_REQD'):
            s_def += """\nDELETE FROM %-29s; -- %-48s%s""" % (self.table_name.upper() + 'P', self.table_desc, self.table_desc2)

        return s_def

    def generate_tbl_file(self, s_file_path):
        '''
        生成tbl文件
        '''
        s_tbl = self.get_table_define()
        if len(s_tbl) == 0:
            return

        with open(s_file_path, 'w', encoding='UTF-8', errors='ignore') as f_w:
            f_w.write(s_tbl)

    def generate_ptn_file(self, s_file_path):
        '''
        生成ptn文件
        '''
        s_ptn = self.get_table_patten()
        if len(s_ptn) == 0:
            return

        with open(s_file_path, 'w', encoding='UTF-8', errors='ignore') as f_w:
            f_w.write(s_ptn)

    def generate_class_code(self, s_file_path):
        '''
        生成c++ class代码文件
        '''
        s_code = self.get_table_class_code()
        if len(s_code) == 0:
            return

        with open(s_file_path, 'w', encoding='UTF-8', errors='ignore') as f_w:
            f_w.write(s_code)

    def generate_sql_file(self, s_file_path):
        '''
        生成创建表的sql文件
        '''
        s_sql = self.get_table_sqlscript()
        if len(s_sql) == 0:
            return

        with open(s_file_path, 'w', encoding='UTF-8', errors='ignore') as f_w:
            f_w.write(s_sql)

    def generate_class_file_java(self, s_file_path):
        '''
        生成java class文件
        '''
        s_class = self.get_table_class_define_java()
        if len(s_class) == 0:
            return

        with open(s_file_path, 'w', encoding='UTF-8', errors='ignore') as f_w:
            f_w.write(s_class)


class Security(object):
    '''
    定义权限的数据结构
    '''

    def __init__(self, s_name, s_desc='', s_desc2='', s_sequence='', b_created=False):
        '''
        Constructor
        '''
        self.sec_name = s_name
        self.sec_sequence = s_sequence
        self.sec_desc = s_desc
        self.sec_desc2 = s_desc2  # 中文描述
        self.b_created = b_created

    def get_initsql(self):
        '''
        得到插入权限表的语句
        '''

        if len(self.sec_name) == 0 or self.b_created:
            return ''

        s_module = self.sec_name[:2]
        s_sql = "INSERT INTO ASSEC(ASSEC_MODULEID,ASSEC_SECID,ASSEC_SEQUENCE,ASSEC_SECDESC) VALUES('%s','%s',%s,'%s');" % (
        s_module, self.sec_name, self.sec_sequence, self.sec_desc)

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
