import os
import re
import os.path
from os.path import join

def replace_infolder(s_folder_path, s_from_list, s_to_list, file_type_list, file_encoding='UTF-8') :
    """
    TODO: 将目录下面指定文件类型的文件中符合s_from_list正则表达式的内容，替换成s_to_list中对应的内容
    file_type_list可以指定文件类型列表，如果为空，则检索所有文件。举例：['.ctl', '.frm', '.vbp']
    """
    print('----------------------upgrade folder------------------------------------')

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
                replace_infile(s_filepath, s_from_list, s_to_list, file_encoding)
                

def replace_infile(s_file_path, s_from_list, s_to_list, file_encoding='UTF-8') :
    '''
        TODO：打开指定文件，并替换文件内容
    '''
    #print(f'Replace in file: {s_file_path}, repalce from "{s_from_list} to "{s_to_list}"')

    #打开文件，并替换文件内容
    s_file_lines = []

    with open(s_file_path, 'r', encoding=file_encoding, errors='ignore' ) as f:
        #print(f.read())
        s_file_lines = f.readlines()

    # s_file_path = s_file_path.replace('.vbp', '_new.vbp')
    with open(s_file_path, 'w', encoding=file_encoding, errors='ignore' ) as f_w:
        for s_line in s_file_lines:
            i = 0
            for sfrom in s_from_list:
                s_line = replace_re(s_line, sfrom, s_to_list[i])
                i += 1

            f_w.write(s_line)


def replace_re(s_text, s_from, s_to) :
    s_result = s_text
    pattern = re.compile(s_from)    
    match_result = re.match(pattern, s_text)
    if match_result:
        s_result = re.sub(pattern, s_to, s_text)
    #     s_result = s_result.replace(match_result.group(), s_to)
        print(f'将字符串{match_result.group()} 替换为：{s_result}')
        # for g in match_result.groups():
        #     print(g)
    
    return s_result



if __name__ == '__main__' :
    #upgrade_and_comple(s_AMView_home, s_AMUI_home, s_vb_home, sPath)
    #[.\n]不能表示所有字符
    #使用(.|\s)来表示所有字符
    #使用[\s\S]来表示所有字符
    # s_mask_or_list = 'RateOperList\n1 - Multiply\n2 - Divide'
    # s_from = r'(.*)List([\S\s]*)'
    # s_to = r'\1List'
    # s_mask_or_list = replace_re(s_mask_or_list, s_from, s_to) 
    # print(s_mask_or_list)

    # s_mask_or_list = 'RateOperList\n1 - Multiply\n2 - Divide'
    # s_from = r'(.*)List((.|\s)*)'
    # s_to = r'\1List'
    # s_mask_or_list = replace_re(s_mask_or_list, s_from, s_to) 
    # print(s_mask_or_list)

    s_mask_or_list = '%-12N'
    s_from = r'(.*)%[-](.*?)([\)]?)$'
    s_to = r'Key\2Mask'
    s_mask_or_list = replace_re(s_mask_or_list, s_from, s_to) 
    print(s_mask_or_list)

    #使用非贪婪模式匹配括号之前的字符
    s_mask_or_list = '(%-12N)'
    s_from = r'(.*)%[-](.*?)([\)]?)$'
    s_to = r'Key\2Mask'
    s_mask_or_list = replace_re(s_mask_or_list, s_from, s_to) 
    print(s_mask_or_list)
