import os
import re
import os.path
from os.path import join
import sys

sys.path.append(r'd:\dev\NormingWork\src\Common')
import ReplaceInFile
import VB6MakeFiles



def upgrade_vb_projects(s_VBCode_path, s_compile_to, s_module, s_version, b_comp_with_Sage60 = False, s_compatible_mode = '0') :
    '''
    s_module: 模块名，例如AQ，BS等
    s_version: 要升级到的版本, 例如66A
    '''
    print('----------------------upgrade files------------------------------------')

    #replace from ACCPACUIGlobals.bas
    s_from_list_bas = [r' *"\d\d[A~Z]"']
    s_to_list_bas = [f'    "{s_version}"']

    #replace from *.vbp
    s_from_list = [r'MinorVer=.?', r'(.*)\\\d\d[A~Z]\\(.*)', r'(.*)%s\d\dA(.*)' % (s_module),  r'CompatibleMode=".?"',
         r'Path32="(.*)', r'(.*)#2\.1#0; MSCOMCTL.OCX', r'(.*)#2\.1#0; mscomctl.ocx', r'(.*)#2\.1#0; mscomctl.OCX']
    s_to_list = ['MinorVer=%s' % (s_version[1:2]), r'\1\\%s\\\2' % (s_version), r'\1%s%s\2' % (s_module, s_version), f'CompatibleMode="{s_compatible_mode}"', 
        f'Path32="{s_compile_to}{s_module}{s_version}"', r'\1#2.0#0; MSCOMCTL.OCX', r'\1#2.0#0; MSCOMCTL.OCX', r'\1#2.0#0; MSCOMCTL.OCX']
    s_to_list_eng = ['MinorVer=%s' % (s_version[1:2]), r'\1\\%s\\\2' % (s_version), r'\1%s%s\2' % (s_module, s_version),  f'CompatibleMode="{s_compatible_mode}"', 
        f'Path32="{s_compile_to}{s_module}{s_version}\\\\ENG"', r'\1#2.0#0; MSCOMCTL.OCX', r'\1#2.0#0; MSCOMCTL.OCX', r'\1#2.0#0; MSCOMCTL.OCX']

    if b_comp_with_Sage60:
        s_from_list.append(r'(.*)#\d\.\d#0; a4wPeriodPicker.ocx')
        s_from_list.append(r'(.*)#\d\.\d#0; a4wGoBtn.ocx')
        s_to_list.append(r'\1#1.4#0; a4wPeriodPicker.ocx')
        s_to_list.append(r'\1#1.0#0; a4wGoBtn.ocx')
        s_to_list_eng.append(r'\1#1.4#0; a4wPeriodPicker.ocx')
        s_to_list_eng.append(r'\1#1.0#0; a4wGoBtn.ocx')



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
                ReplaceInFile.replace_infile(s_filepath, s_from_list_bas, s_to_list_bas)
            
            elif (s_filetype == '.vbp') and ((len(s_filename) == len('ACCPACXX0000')) or (len(s_filename) == len('ACCPACXX0000ENG')) or (len(s_filename) == len('XX66AENGClient'))) :                
                #print(f'Current File: {s_filepath}')
                if (s_filename[-3:].lower() == 'eng') or (s_filename[-6:].lower() == 'client'):
                    ReplaceInFile.replace_infile(s_filepath, s_from_list, s_to_list_eng)
                else:
                    ReplaceInFile.replace_infile(s_filepath, s_from_list, s_to_list)




def upgrade_view_projects(s_viewCode_path, s_module, s_version, s_from_ver = '\d\d') :
    '''
    修改View的项目文件，如果指定s_from_ver, 则需要指定为版本的数字部分，如'65'
    '''
    print('----------------------upgrade view projects------------------------------------')

    #replace from *.vcproj;*.vcxproj
    s_from_list = [r'(.*)%s%s[A~Z](.*)' % (s_module, s_from_ver)]
    s_to_list = [r'\1%s%s\2' % (s_module, s_version)]
     
    for root, dirs, files in os.walk(s_viewCode_path): #files会得到目录下的文件（不包括文件夹）；dirs会获取到每个文件夹下面的子目录；root会遍历每个子文件夹
        # print('Current Folder: ', root)
        for file in files:
            s_filename = os.path.splitext(file)[0] #文件名
            s_filetype = os.path.splitext(file)[1] #文件后缀
            
            s_filepath = os.path.join(root, file)
            if not (os.path.exists(s_filepath)):
                continue

            if (s_filetype == '.vcproj'):
                #print(f'Current File: {s_filepath}')
                ReplaceInFile.replace_infile(s_filepath, s_from_list, s_to_list)
            elif s_filetype == '.vcxproj': #需要替换3次
                ReplaceInFile.replace_infile(s_filepath, s_from_list, s_to_list)
                ReplaceInFile.replace_infile(s_filepath, s_from_list, s_to_list)
                ReplaceInFile.replace_infile(s_filepath, s_from_list, s_to_list)
            
def upgrade_view_projects_from2005_security(s_viewCode_path, s_module, s_version) :
    '''
    将升级的C++项目修复，增加include和lib路径
    '''
    print('----------------------upgrade view projects------------------------------------')

    #replace from *.vcproj;*.vcxproj
    s_from_list = [r'(.*)%s\d\d[A~Z](.*)' % (s_module),
        '    <Keyword>Win32Proj</Keyword>',
        '    <GenerateManifest>true</GenerateManifest>',
        '      <TargetMachine>MachineX86</TargetMachine>'
        ]
    s_to_list = [r'\1%s%s\2' % (s_module, s_version),
        r'    <Keyword>Win32Proj</Keyword>\n    <WindowsTargetPlatformVersion>10.0.17763.0</WindowsTargetPlatformVersion>',
        r'    <GenerateManifest>true</GenerateManifest>\n    <LibraryPath>$(DEV_HOME)\lib;$(LibraryPath)</LibraryPath>\n    <IncludePath>$(DEV_HOME)\Security\Sec2019\%s%s\ViewSource\classes;$(DEV_HOME)\Security\Sec2019\%s%s\ViewSource\include;$(DEV_HOME)\include;$(IncludePath)</IncludePath>' % (s_module, s_version, s_module, s_version),
        r'      <TargetMachine>MachineX86</TargetMachine>\n      <ImageHasSafeExceptionHandlers>false</ImageHasSafeExceptionHandlers>'
        ]
     
    for root, dirs, files in os.walk(s_viewCode_path): #files会得到目录下的文件（不包括文件夹）；dirs会获取到每个文件夹下面的子目录；root会遍历每个子文件夹
        # print('Current Folder: ', root)
        for file in files:
            s_filename = os.path.splitext(file)[0] #文件名
            s_filetype = os.path.splitext(file)[1] #文件后缀
            
            s_filepath = os.path.join(root, file)
            if not (os.path.exists(s_filepath)):
                continue

            if s_filetype == '.vcxproj':
                #print(f'Current File: {s_filepath}')
                ReplaceInFile.replace_infile(s_filepath, s_from_list, s_to_list)


def upgrade_view_template(s_viewCode_path, s_module, s_version) :
    '''
    对目录下面的View执行mkinst命令
    '''
    for root, dirs, files in os.walk(s_viewCode_path): #files会得到目录下的文件（不包括文件夹）；dirs会获取到每个文件夹下面的子目录；root会遍历每个子文件夹
        for dir in dirs:            
            s_dirname = os.path.split(dir)[1].upper()
            if s_dirname[:2].lower() == s_module.lower():
                s_cmd = f'mkinst @{s_dirname}.ptn'
                s_path = os.path.join(root, dir)
                os.chdir(s_path)
                fp = os.popen(s_cmd) #路径用""引起来可以避免空格带来的问题
                fpread = fp.read()
                print(fpread)

            


if __name__ == '__main__' :
    sPath2 = r"D:\\Sage300\\"
    s_vb_home = r'C:\Program Files (x86)\Microsoft Visual Studio\VB98'
    s_UI_home = r'D:\Pluswdev2012\Security\Sec2019'
    s_View_home = r'D:\Pluswdev2012\Security\Sec2019'
    
    
