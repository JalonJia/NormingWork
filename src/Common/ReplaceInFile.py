import os
import re
import os.path
from os.path import join


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
    
    return s_result



if __name__ == '__main__' :
    #upgrade_and_comple(s_AMView_home, s_AMUI_home, s_vb_home, sPath)
    pass
