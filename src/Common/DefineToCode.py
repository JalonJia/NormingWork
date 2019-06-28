'''
Created on May 27, 2019
读取C/C++定义，生成初始化代码 
例如: CHAR sTest[SIZEOF_TEST + 1]; -> strCopy(sTest, "");
@author: Jalon Jia
'''

from TableClass import Field, Table
from datetime import date,datetime
import ReplaceInFile
import os
import copy

class CppFieldDefine(object):
    def __init__(self, s_field_type, s_field_name, s_field_len_list):
        '''
        Constructor
        '''
        self.field_name = s_field_name;
        self.field_type = s_field_type;
        self.field_len_array = s_field_len_list;
    
    def get_init_code(self):
        array_deep = len(self.field_len_array)
        s_last_len = '0'
        if self.field_type in ('CHAR', 'DBSSTRING', 'char', 'BYTE', 'DBSNUMBER', 'BCD'):
            array_deep = len(self.field_len_array) - 1
            s_last_len = self.field_len_array[-1]
            
        to_str = ''
        iLoopIndex = 0
        s_tab = ''
        s_for = ''                
        s_for_end = ''
        s_loop = ''
        for iLoopIndex in range(0, array_deep):
            s_for += '{}for (int iLoop{} = 0; iLoop{} < {}; iLoop{}++)\n'.format(s_tab, iLoopIndex, iLoopIndex, self.field_len_array[iLoopIndex], iLoopIndex)
            s_for += s_tab
            s_for += '{\n'
            s_tab += ' ' * 4
            s_loop += '[iLoop{}]'.format(iLoopIndex)
            s_for_end += '\n'
            s_for_end += ' ' * 4 * (array_deep - iLoopIndex - 1)
            s_for_end += '}'

        if self.field_type in ('DBSINT', 'DBSLONG', 'int', 'long', 'short', 'INT', 'INT16', 'BOOL', 'UINT8', 'INT32', 'UINT16', 'UINT32', 'FLOAT64', 'double', 'float', 'DBSREAL', 'REAL'):
            to_str += '{}{}{}{} = 0;{}'.format(s_for, s_tab, self.field_name, s_loop, s_for_end)
        elif self.field_type in ('CHAR', 'DBSSTRING', 'char'):
            to_str = '{}{}strCopy({}{}, "");{}'.format(s_for, s_tab, self.field_name, s_loop, s_for_end)
        elif self.field_type in ('DBSNUMBER', 'BCD'):
            to_str = '{}{}bcdInit({}{}, {});{}'.format(s_for, s_tab, self.field_name, s_loop, s_last_len, s_for_end)
        elif self.field_type in ('MONEY', 'DBSMONEY'):
            to_str = '{}{}moneyInit({}{});{}'.format(s_for, s_tab, self.field_name, s_loop, s_for_end)
        elif self.field_type in ('BYTE'):
            to_str = '{}{}memset({}{}, {}, 0);{}'.format(s_for, s_tab, self.field_name, s_loop, s_last_len, s_for_end)
        elif self.field_type in ('DBSDATE', 'DATE', 'BCDDATE'):
            to_str = '{}{}dateInit({}{});{}'.format(s_for, s_tab, self.field_name, s_loop, s_for_end)
        elif self.field_type in ('DBSTIME', 'TIME', 'BCDTIME'):
            to_str = '{}{}timeInit({}{});{}'.format(s_for, s_tab, self.field_name, s_loop, s_for_end)
        elif self.field_type in ('bool'):
            to_str = '{}{}{}{} = false;{}'.format(s_for, s_tab, self.field_name, s_loop, s_for_end)
        elif self.field_type in ('DBSBOOL'):
            to_str = '{}{}{}{} = FALSE;{}'.format(s_for, s_tab, self.field_name, s_loop, s_for_end)

        print(to_str)
        return to_str

    def get_copy_code(self):
        array_deep = len(self.field_len_array)
        s_last_len = '0'
        if self.field_type in ('CHAR', 'DBSSTRING', 'char', 'BYTE', 'DBSNUMBER', 'BCD'):
            array_deep = len(self.field_len_array) - 1
            s_last_len = self.field_len_array[-1]
            
        to_str = ''
        iLoopIndex = 0
        s_tab = ''
        s_for = ''                
        s_for_end = ''
        s_loop = ''
        for iLoopIndex in range(0, array_deep):
            s_for += '{}for (int iLoop{} = 0; iLoop{} < {}; iLoop{}++)\n'.format(s_tab, iLoopIndex, iLoopIndex, self.field_len_array[iLoopIndex], iLoopIndex)
            s_for += s_tab
            s_for += '{\n'
            s_tab += ' ' * 4
            s_loop += '[iLoop{}]'.format(iLoopIndex)
            s_for_end += '\n'
            s_for_end += ' ' * 4 * (array_deep - iLoopIndex - 1)
            s_for_end += '}'

        if self.field_type in ('DBSINT', 'DBSLONG', 'int', 'long', 'short', 'INT', 'INT16', 'BOOL', 'UINT8', 'INT32', 'UINT16', 'UINT32', 'FLOAT64', 'double', 'float', 'DBSREAL', 'REAL'):
            to_str += '{}{}{}{} = copyFrom.{}{};{}'.format(s_for, s_tab, self.field_name, s_loop, self.field_name, s_loop, s_for_end)
        elif self.field_type in ('CHAR', 'DBSSTRING', 'char'):
            s_last_len = s_last_len.replace("+1",  "").replace("+ 1", "").rstrip()
            to_str = '{}{}NmStringUtil::strCopyNRT({}{}, copyFrom.{}{}, {});{}'.format(s_for, s_tab, self.field_name, s_loop, self.field_name, s_loop, s_last_len, s_for_end)
        elif self.field_type in ('DBSNUMBER', 'BCD'):
            to_str = '{}{}memcpy({}{}, copyFrom.{}{}, {});{}'.format(s_for, s_tab, self.field_name, s_loop, self.field_name, s_loop, s_last_len, s_for_end)
        elif self.field_type in ('MONEY', 'DBSMONEY'):
            to_str = '{}{}moneyAssign({}{}, copyFrom.{}{});{}'.format(s_for, s_tab, self.field_name, s_loop, self.field_name, s_loop, s_for_end)
        elif self.field_type in ('BYTE'):
            to_str = '{}{}memcpy({}{}, copyFrom.{}{}, {});{}'.format(s_for, s_tab, self.field_name, s_loop, self.field_name, s_loop, s_last_len, s_for_end)
        elif self.field_type in ('DBSDATE', 'BCDDATE'):
            to_str = '{}{}dateCopy({}{}, copyFrom.{}{});{}'.format(s_for, s_tab, self.field_name, s_loop, self.field_name, s_loop, s_for_end)
        elif self.field_type in ('DBSTIME', 'BCDTIME'):
            to_str = '{}{}dtBCDTimeAssign({}{}, copyFrom.{}{});{}'.format(s_for, s_tab, self.field_name, s_loop, self.field_name, s_loop, s_for_end)
        elif self.field_type in ('bool'):
            to_str = '{}{}{}{} = copyFrom.{}{};{}'.format(s_for, s_tab, self.field_name, s_loop, self.field_name, s_loop, s_for_end)
        elif self.field_type in ('DBSBOOL'):
            to_str = '{}{}{}{} = copyFrom.{}{};{}'.format(s_for, s_tab, self.field_name, s_loop, self.field_name, s_loop, s_for_end)

        print(to_str)
        return to_str

class CppFieldGroup(object):
    '''
    定义字段列表
    '''

    def __init__(self, s_table_name):
        '''
        Constructor
        '''
        self.table_name = s_table_name
        self.fields = []


    def add_field(self, field):
        '''
        增加字段
        '''
        if len(field.get_init_code()) > 0:
            self.fields.append(field)

    def remove_field(self, field_name):
        '''
        删除字段
        '''
        for f in self.fields[:]:
            if f.field_name == field_name:
                self.fields.remove(f)

    def clear_fields(self):
        '''
        清空字段
        '''
        self.fields = []

    def __get_init_code(self):
        '''
        得到init的代码
        '''
        s_code = 'void initValues()\n{\n'

        for field in self.fields:                
            s_code += field.get_init_code()
            s_code += '\n'

        s_code += '}\n'

        return s_code

    def __get_copy_code(self):
        '''
        得到copy的代码
        '''
        s_code = 'void copyValues(copyFrom)\n{\n'

        for field in self.fields:                
            s_code += field.get_copy_code()
            s_code += '\n'

        s_code += '}\n'

        return s_code


    def generate_cpp_code(self, s_file_path):
        '''
        生成init的cpp文件
        '''
        s_code = self.__get_init_code()
        s_code += self.__get_copy_code()
        if len(s_code) == 0:
            return 
        
        with open(s_file_path, 'w', encoding='UTF-8', errors='ignore' ) as f_w:
            f_w.write(s_code)


class CppDefineToCode(object):
    '''
    读取.h/.cpp文件 
    '''
    def __init__(self, p_file_name):
        '''
        Constructor
        '''
        self.file_name = p_file_name
        self.table_name = os.path.splitext(os.path.split(p_file_name)[1])[0].upper()
        #print(os.path.split(p_file_name)[1])
        #print(os.path.splitext(os.path.split(p_file_name)[1]))
        self.table = CppFieldGroup(self.table_name)
    
    def __read_file(self):
        self.table.clear_fields()
        
        with open(self.file_name, 'r', encoding='UTF-8', errors='ignore' ) as f:
            #print(f.read())            
            s_file_lines = f.readlines()
            for s_line in s_file_lines:
                s_line_temp = s_line.split('//')[0].replace(';', '') #去掉注释及分号
                field_info = s_line_temp.split()
                print(s_line_temp)
                
                if len(field_info) < 2:
                    continue

                field_type = field_info[0]
                field_name = field_info[1].split('[')[0]
                field_length_list = []
                s_len_list = s_line_temp.split('[')
                i_count = len(s_len_list)
                while i_count > 1:
                    field_length = s_len_list[len(s_len_list) - i_count + 1].split(']')[0]
                    field_length_list.append(field_length)
                    i_count -= 1 

                if len(s_line_temp.split('[')) > 1:
                    field_length = s_line_temp.split('[')[1].split(']')[0]

                one_field = CppFieldDefine(field_type, field_name, field_length_list)
                self.table.add_field(copy.deepcopy(one_field))


    def generate_table_code(self, file_path):
        '''
        TODO: 生成C++的代码
        '''

        self.__read_file()

        if not os.path.exists(file_path):
            os.makedirs(file_path, mode=0o777, exist_ok=True)
        
        s_file = os.path.join(file_path, f'{self.table_name.lower()}.gen.cpp')
        self.table.generate_cpp_code(s_file)






#Testing
if __name__ == '__main__' :
    gen_list = []
    gen_list.append(CppDefineToCode(r'D:\Documents\OEMDocuments\RMDocs\RM66A\PU0\Temp\a.h'))
    # gen_list.append(ReadTblFile(r'D:\Pluswdev2012\EN65A\Source\Cprogram\ENRCPH\ENRCPH.tbl'))
    # gen_list.append(ReadTblFile(r'D:\Pluswdev2012\EN65A\Source\Cprogram\ENRCPL\ENRCPL.tbl'))
    # gen_list.append(ReadTblFile(r'D:\Pluswdev2012\EN65A\Source\Cprogram\ENRCPLC\ENRCPLC.tbl'))
    # gen_list.append(ReadTblFile(r'D:\Documents\OEMDocuments\RMDocs\RM65APU2\Temp\PORCPH.tbl'))
    # gen_list.append(ReadTblFile(r'D:\Documents\OEMDocuments\RMDocs\RM65APU2\Temp\PORCPL.tbl'))
    for x in gen_list:
        x.generate_table_code(r'D:\Documents\OEMDocuments\RMDocs\RM66A\PU0\Temp')



