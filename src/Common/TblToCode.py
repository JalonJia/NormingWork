'''
Created on January 17, 2019
读取tbl文件，并生成代码
@author: Jalon Jia
'''

from TableClass import Field, Table
from datetime import date,datetime
import ReplaceInFile
import os
import copy


class ReadTblFile(object):
    '''
    读取.tbl文件 
    '''
    def __init__(self, p_file_name):
        '''
        Constructor
        '''
        self.file_name = p_file_name
        self.table_name = os.path.splitext(os.path.split(p_file_name)[1])[0].upper()
        #print(os.path.split(p_file_name)[1])
        #print(os.path.splitext(os.path.split(p_file_name)[1]))
        self.table = Table(self.table_name)
    
    def __read_file(self):
        self.table.fields.clear()
        
        with open(self.file_name, 'r', encoding='UTF-8', errors='ignore' ) as f:
            #print(f.read())            
            s_file_lines = f.readlines()
            for s_line in s_file_lines:
                field_info = s_line.split()
                if len(field_info) < 7:
                    continue
                if field_info[0][0] in '#!/':
                    continue

                field_name = field_info[3]
                field_type = field_info[4]
                field_length = 0
                if field_info[5] != '-':
                    field_length = int(field_info[5])
                field_dec = field_info[6]
                one_field = Field(field_name, field_type, field_length)
                self.table.add_field(copy.deepcopy(one_field))


    def generate_table_code(self, file_path):
        '''
        TODO: 生成C++的代码
        '''

        self.__read_file()

        if not os.path.exists(file_path):
            os.makedirs(file_path, mode=0o777, exist_ok=True)
        
        s_file = os.path.join(file_path, f'{self.table_name.lower()}.h')
        self.table.generate_class_code(s_file)






#Testing
if __name__ == '__main__' :
    gen_list = []
    gen_list.append(ReadTblFile(r'D:\Pluswdev2012\EN65A\Source\Cprogram\ENRCPH\ENRCPH.tbl'))
    gen_list.append(ReadTblFile(r'D:\Pluswdev2012\EN65A\Source\Cprogram\ENRCPL\ENRCPL.tbl'))
    gen_list.append(ReadTblFile(r'D:\Pluswdev2012\EN65A\Source\Cprogram\ENRCPLC\ENRCPLC.tbl'))
    for x in gen_list:
        x.generate_table_code(r'D:\Documents\OEMDocuments\RMDocs\RM65APU2\Temp')



