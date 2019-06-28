import os
import re
import os.path
from os.path import join

def calculate_infolder(s_folder_path, file_type_list, file_encoding='UTF-8') :
    """
    TODO: 将目录下面指定文件类型的文件中符合s_from_list正则表达式的内容，替换成s_to_list中对应的内容
    file_type_list可以指定文件类型列表，如果为空，则检索所有文件。举例：['.ctl', '.frm', '.vbp']
    """
    print('----------------------calculate in folder------------------------------------')

    line_count = 0

    for root, dirs, files in os.walk(s_folder_path): #files会得到目录下的文件（不包括文件夹）；dirs会获取到每个文件夹下面的子目录；root会遍历每个子文件夹
        # print('Current Folder: ', root)
        for file in files:
            s_filename = os.path.splitext(file)[0] #文件名
            s_filetype = os.path.splitext(file)[1] #文件后缀
            
            s_filepath = os.path.join(root, file)
            if not (os.path.exists(s_filepath)):
                continue

            if (len(file_type_list) == 0) or (s_filetype in file_type_list):
                #print(f'Current File: {s_filepath}')
                line_count += calculate_one_file(s_filepath, file_encoding)

    return line_count            

def calculate_one_file(s_file_path, file_encoding='UTF-8') :
    '''
        TODO：打开指定文件，统计行数
    '''
    #print(f'Replace in file: {s_file_path}, repalce from "{s_from_list} to "{s_to_list}"')

    #打开文件，并替换文件内容
    s_file_lines = []

    with open(s_file_path, 'r', encoding=file_encoding, errors='ignore' ) as f:
        #print(f.read())
        s_file_lines = f.readlines()        

    return len(s_file_lines) - s_file_lines.count("")



if __name__ == '__main__' :
    file_types = [ '.c', '.h', '.cpp', '.i', '.ctl', '.frm', '.vbp'] # '.gen', '.rci', '.rc', '.bas', '.cls'

    #s_RM_path = r"D:\Pluswdev2012\EN66A\VBSource\Setup\Options\AccpacEN1003"
    s_RM_path = r'D:\Pluswdev2012\EN66A'
    rm_code_lines = calculate_infolder(s_RM_path, file_types)
    print(f'RM-Backend 源码行数为：{rm_code_lines}')

    s_AM_path = r'D:\Pluswdev2012\AM66A'
    am_code_lines = calculate_infolder(s_AM_path, file_types)
    print(f'AM-Backend 源码行数为：{am_code_lines}')

    s_NP_path = r'D:\Pluswdev2012\NP66A'
    np_code_lines = calculate_infolder(s_NP_path, file_types)
    print(f'NP-Backend 源码行数为：{np_code_lines}')
