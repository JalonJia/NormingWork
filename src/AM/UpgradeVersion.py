import os
import re
import os.path
from os.path import join

sPath = r"D:\SAge300\AM66A"
s_vb_home = r'C:\Program Files (x86)\Microsoft Visual Studio\VB98'
s_AMUI_home = r'D:\Pluswdev\AM66A\UISource'
s_AMView_home = r'D:\Pluswdev\AM66A\ViewSource'


def upgrade_and_comple(s_ViewCode_home, s_VBCode_path, s_vbexe_path, s_compile_to) :
    print('----------------------upgrade_and_comple------------------------------------')
    
    upgrade_view_files(s_ViewCode_home)
    #upgrade_files(s_VBCode_path, s_compile_to)
    os.chdir(s_vbexe_path)
    #comple_vb_projects(s_VBCode_path, s_vbexe_path, s_compile_to, "0", "2")



def upgrade_files(s_VBCode_path, s_compile_to) :
    print('----------------------upgrade files------------------------------------')

    #replace from ACCPACUIGlobals.bas
    s_from_list_bas = [r' *"\d\d[A~Z]"']
    s_to_list_bas = ['    "66A"']

    #replace from *.vbp
    s_from_list = [r'MinorVer=.?', r'(.*)AM65A(.*)', r'CompatibleMode=".?"', r'Path32=".*"']
    s_to_list = ['MinorVer=6', r'\1AM66A\2', 'CompatibleMode="0"', f'Path32="{s_compile_to}"']
    s_to_list_eng = ['MinorVer=6', r'\1AM66A\2', 'CompatibleMode="0"', f'Path32="{s_compile_to}\ENG']
    
    for root, dirs, files in os.walk(s_VBCode_path): #files会得到目录下的文件（不包括文件夹）；dirs会获取到每个文件夹下面的子目录；root会遍历每个子文件夹
        # print('Current Folder: ', root)
        for file in files:
            s_filename = os.path.splitext(file)[0] #文件名
            s_filetype = os.path.splitext(file)[1] #文件后缀
            
            s_filepath = os.path.join(root, file)
            if not (os.path.exists(s_filepath)):
                continue

            if (s_filetype == '.bas') and (s_filename == 'ACCPACUIGlobals') :
                #print(f'Current File: {s_filepath}')
                replace_infile(s_filepath, s_from_list_bas, s_to_list_bas)
            
            elif (s_filetype == '.vbp') and (len(s_filename) >= len('ACCPACAM0000')) :                
                #print(f'Current File: {s_filepath}')
                if (s_filename[-3:].lower() == 'eng') :
                    replace_infile(s_filepath, s_from_list, s_to_list_eng)
                else:
                    replace_infile(s_filepath, s_from_list, s_to_list)


def comple_vb_projects(s_VBCode_path, s_vbexe_path, s_compile_to, s_compatible_Mode_before, s_compatible_Mode_after) :           
    print('----------------------Compile files------------------------------------')
    l_count = 0

    #replace CompatibleMode back for *.vbp 
    s_from_list = [r'CompatibleMode=".?"']
    s_to_list_before = [f'CompatibleMode="{s_compatible_Mode_before}"']
    s_to_list_after = [f'CompatibleMode="{s_compatible_Mode_after}"']

    for root, dirs, files in os.walk(s_VBCode_path): #files会得到目录下的文件（不包括文件夹）；dirs会获取到每个文件夹下面的子目录；root会遍历每个子文件夹
        # print('Current Folder: ', root)
        for file in files:
            s_filename = os.path.splitext(file)[0] #文件名
            s_filetype = os.path.splitext(file)[1] #文件后缀
            #print(s_filetype)
            s_filepath = os.path.join(root, file)
            if not (os.path.exists(s_filepath)):
                continue

            if (s_filetype == '.vbp') and (s_filename[-3:] != 'EXE') and (len(s_filename) >= len('ACCPACAM0000')) :                
                #print(f'Current File: {s_filepath}')
                print(f'Compile: {s_filepath}')
                
                replace_infile(s_filepath, s_from_list, s_to_list_before)

                fp = os.popen('vb6.exe /make "%s"' % s_filepath) #路径用""引起来可以避免空格带来的问题
                fpread = fp.read()
                l_count += 1
                print(fpread)

                replace_infile(s_filepath, s_from_list, s_to_list_after)

    print(f'Total {l_count} file Compiled')


def upgrade_view_files(s_viewCode_path) :
    print('----------------------upgrade view files------------------------------------')

    #replace from *.vcproj;*.vcxproj
    s_from_list = [r'(.*)AM65A(.*)']
    s_to_list = [r'\1AM66A\2']
     
    for root, dirs, files in os.walk(s_viewCode_path): #files会得到目录下的文件（不包括文件夹）；dirs会获取到每个文件夹下面的子目录；root会遍历每个子文件夹
        # print('Current Folder: ', root)
        for file in files:
            s_filename = os.path.splitext(file)[0] #文件名
            s_filetype = os.path.splitext(file)[1] #文件后缀
            
            s_filepath = os.path.join(root, file)
            if not (os.path.exists(s_filepath)):
                continue

            if (s_filetype == '.vcproj') or  (s_filetype == '.vcxproj') :
                #print(f'Current File: {s_filepath}')
                replace_infile(s_filepath, s_from_list, s_to_list)
            

def replace_infile(s_file_path, s_from_list, s_to_list) :
    #print(f'Replace {s_file_path}: {s_from_list} to {s_to_list}')

    #打开文件，并替换文件内容
    s_file_lines = []

    with open(s_file_path, 'r', encoding='UTF-8', errors='ignore' ) as f:
        #print(f.read())
        s_file_lines = f.readlines()

    # s_file_path = s_file_path.replace('.vbp', '_new.vbp')
    with open(s_file_path, 'w', encoding='UTF-8', errors='ignore' ) as f_w:
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
    #     #print(f'在{s_text} 中替换字符串{match_result.group()}, 替换之后为：{s_result}')
    
    return s_result





if __name__ == '__main__' :
    upgrade_and_comple(s_AMView_home, s_AMUI_home, s_vb_home, sPath)

