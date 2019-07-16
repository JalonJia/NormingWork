import os
import os.path
from os.path import join #这样引入之后，join就可以直接使用了
import shutil
import xlwt #安装包：pip install xlwt
from datetime import date,datetime
import copy

'''
TODO: 使用Resource Hacker将RES文件中的字符串提取出来生成rc文件
'''



#Test Funtions
#sPath = "D:\Pluswdev\AM65A\UISource"
#print(os.listdir(sPath))
#print(os.path.split(sPath)) #将路径分解成两部分，第一部分从开始到最后一个路径分隔符，最后一个分隔符后面的路径\
#sPath = 'D:\\ACCPAC\\AM65A\\am.ini'
#print(os.path.dirname(sPath)) #路径的第一部分
#print(os.path.basename(sPath)) #路径的第二部分
#print(os.path.splitext(sPath))

#os.chdir(s_runner_home)

class ResourceString:
    '''
    每条资源对应的数据结构，前面是ID，后面是字符串
    '''
    def __init__(self):
        self.res_id = ''
        self.res_string = ''

    def string_to_resource(self, from_string):
        '''
        判断一个字符串是不是合法的资源
        '''
        self.res_id = ''
        self.res_string = ''

        #1. 去掉注释
        temp_str = from_string.split('//')[0].strip().strip()
        #2. 判断有没有双引号, 没有双引号返回错误
        temp_str2 = temp_str.split('"')
        if len(temp_str2) < 3:
            return False

        #3. 判断是不是#include的行
        if '#include' in temp_str:
            return False
        
        #4. 找到第一个双引号的位置
        self.res_id = temp_str.split('"')[0].replace(',', '').strip()
        self.res_string = temp_str[len(temp_str.split('"')[0]) : ].strip()
        if self.res_string[0] == '"':
            self.res_string = self.res_string[1: ]
        if self.res_string[-1] == '"':
            self.res_string = self.res_string[ : -1]
        return True
    



class ResourceCompare:
    '''
    将两个文件夹的dll反编译成rc文件，然后进行比较
    '''
    def __init__(self, res_folder_1, res_folder_2, rc_folder_1, rc_folder_2, result_excel_file, resouce_hacker_path):
        '''
        Constructor
        '''
        self.res_folder_1 = res_folder_1
        self.res_folder_2 = res_folder_2
        self.rc_folder_1 = rc_folder_1
        self.rc_folder_2 = rc_folder_2
        self.result_excel_file = result_excel_file
        self.resouce_hacker_path = resouce_hacker_path
        self.res_1 = {}
        self.res_2 = {}
        os.chdir(self.resouce_hacker_path)
        
    def __generate_rc_files(self, s_res_folder, s_rc_folder):
        '''
        生成rc文件
        '''
        for root, dirs, files in os.walk(s_res_folder): #files会得到目录下的文件（不包括文件夹）；dirs会获取到每个文件夹下面的子目录；root会遍历每个子文件夹
            #print('Folder: ', root)
            #s_relative_path = root[len(s_UI_home): ]
            #print('s_relative_path: ', s_relative_path)
            for file in files:
                s_filename = os.path.splitext(file)[0] #文件名
                s_filetype = os.path.splitext(file)[1].lower() #文件后缀
                #print(s_filetype)
                
                if (s_filetype == '.dll'):
                    s_filepath = os.path.join(root, file)
                    s_to_folderpath = s_rc_folder #+ s_relative_path #os.path.join(s_RC_save_home, s_relative_path)
                    s_to_filepath = os.path.join(s_to_folderpath, os.path.splitext(file)[0])
                    print('s_convert_from: ', s_filepath, '=====> to: ', s_to_filepath, '.rc')
                                                   
                    if not os.path.exists(s_to_folderpath):
                        os.makedirs(s_to_folderpath, mode=0o777, exist_ok=True)
                        
                    #if os.path.exists(s_filepath):                
                    fp = os.popen('ResourceHacker.exe -extract "%s", "%s.rc",  StringTable,,' % (s_filepath, s_to_filepath)) #路径用""引起来可以避免空格带来的问题
                    fpread = fp.read()
                    print(fpread)
                    #shutil.copyfile(s_filepath, s_to_filepath)

    def __read_rc_files(self, s_rc_folder, res_dict):
        '''
        从rc文件生成字典
        '''
        for root, dirs, files in os.walk(s_rc_folder): #files会得到目录下的文件（不包括文件夹）；dirs会获取到每个文件夹下面的子目录；root会遍历每个子文件夹
            #print('Folder: ', root)
            #s_relative_path = root[len(s_UI_home): ]
            #print('s_relative_path: ', s_relative_path)
            for file in files:
                s_filename = os.path.splitext(file)[0] #文件名
                s_filetype = os.path.splitext(file)[1].lower() #文件后缀
                #print(s_filetype)
                if (s_filetype == '.rc'):
                    one_file_res = {}
                    s_filepath = os.path.join(root, file)
                    with open(s_filepath, 'r', encoding='UTF-16 LE', errors='ignore' ) as f:
                    #print(f.read())            
                        s_file_lines = f.readlines()
                        one_res = ResourceString()
                        for s_line in s_file_lines:
                            if one_res.string_to_resource(s_line):
                                one_file_res[one_res.res_id] = one_res.res_string

                    res_dict[s_filename] = one_file_res
                    
            #print(res_dict)

    def create_rc_files(self):
        self.__generate_rc_files(self.res_folder_1, self.rc_folder_1)
        self.__generate_rc_files(self.res_folder_2, self.rc_folder_2)


    def compare_res(self):
        '''
        生成两个目录的rc文件, 然后读取rc文件到数据字典
        '''
        self.__read_rc_files(self.rc_folder_1, self.res_1)
        self.__read_rc_files(self.rc_folder_2, self.res_2)
        print(f"dict1: {self.res_1}")
        print(f"dict2: {self.res_2}")

        #打开Excel，写入比较结果
        excel_file = xlwt.Workbook()
        my_sheet = excel_file.add_sheet('CompareResult')
        my_style = xlwt.easyxf('font: name Times New Roman, color-index red, bold on', num_format_str='#,##0.00')   #数据格式
        row_num = 0
        col_res_file = 0
        col_res_id = 1
        col_res_string = 2
        col_res_string_old = 4

        #my_sheet.write(i, j, 1234.56, myStyle)
        #my_sheet.write(2, 2, xlwt.Formula("A3+B3"))      #写入C3，数值等于2（A3+B3）

        #my_sheet.write(2, 0, 1)                          #写入A3，数值等于1
        #my_sheet.write(2, 1, 1)                          #写入B3，数值等于1
    
        for file_name in self.res_2:
            s_res_id = ''
            s_res_string = ''
            s_res_string_old = ''

            if file_name in self.res_1.keys():
                b_write_file = False
                for s_id in self.res_2[file_name]:
                    s_res_id = ''
                    if s_id in self.res_1[file_name].keys():
                        if self.res_1[file_name][s_id] != self.res_2[file_name][s_id]:
                            s_res_id = s_id
                            s_res_string = self.res_2[file_name][s_id]
                            s_res_string_old = self.res_1[file_name][s_id]

                    else:
                        s_res_id = s_id
                        s_res_string = self.res_2[file_name][s_id]
                        s_res_string_old = ''
                                        
                    #写文件
                    if s_res_id > '':
                        if not b_write_file:
                            row_num += 2
                            my_sheet.write(row_num, col_res_file, file_name)
                            my_sheet.write(row_num, col_res_string, self.res_2[file_name]['101'])
                            row_num += 1
                            b_write_file = True

                        my_sheet.write(row_num, col_res_id, s_res_id)
                        my_sheet.write(row_num, col_res_string, s_res_string)
                        my_sheet.write(row_num, col_res_string_old, s_res_string_old)
                        row_num += 1

            else:
                #新文件，都需要记录
                row_num += 2
                my_sheet.write(row_num, col_res_file, file_name)
                my_sheet.write(row_num, col_res_string, self.res_2[file_name]['101'])
                row_num += 1
                for s_id in self.res_2[file_name]:
                    s_res_id = s_id
                    s_res_string = self.res_2[file_name][s_id]

                    my_sheet.write(row_num, col_res_id, s_res_id)
                    my_sheet.write(row_num, col_res_string, s_res_string)
                    row_num += 1

        excel_file.save(self.result_excel_file)            
                    




#Testing
if __name__ == '__main__' :
    s_runner_home = r'D:\Dev\ResourceHacker'
    res_folder_1 = r'C:\Sage300\EN65A\ENG'
    res_folder_2 = r'C:\Sage300\EN66A\ENG'
    res_folder_save_1 = r'C:\Working\WeeklyWorking\ThisWeek\EN65ARC'
    res_folder_save_2 = r'C:\Working\WeeklyWorking\ThisWeek\EN66ARC'
    result_excel_file = r'C:\Working\WeeklyWorking\ThisWeek\diff_res.xls'
    
    res_compare = ResourceCompare(res_folder_1, res_folder_2, res_folder_save_1, res_folder_save_2, result_excel_file, s_runner_home)
    res_compare.compare_res()




