import os
import os.path
from os.path import join #这样引入之后，join就可以直接使用了
import shutil

'''
TODO: 提供以下功能：
1. RES和RC相互转换的工具
2. 提取RES及项目文件到指定的目录
3. 编译
'''

class RESTool(object):
    '''
    RES Tool
    '''
    def __init__(self, s_resource_hacker_home):
        self.s_exe_home = s_resource_hacker_home

    def runCommand(self, s_cmd):
        os.chdir(self.s_exe_home)
        print(f'Command: {s_cmd}')
        fp = os.popen(s_cmd) #路径用""引起来可以避免空格带来的问题
        fpread = fp.read()
        print(fpread)

    def convertRESToRC(self, s_RES_file, s_RC_folder):
        '''
        s_RES_file: RES文件，需要具体的文件名及后缀
        s_RC_folder：存放rc文件的文件夹路径，不需要有后缀
        '''
        s_filename = os.path.splitext(os.path.split(s_RES_file)[1])[0]
        s_RC_filepath = os.path.join(s_RC_folder, s_filename)

        s_cmd = 'ResourceHacker.exe -extract "%s", "%s.rc",  StringTable,,' % (s_RES_file, s_RC_filepath) #路径用""引起来可以避免空格带来的问题
        self.runCommand(s_cmd)

        s_cmd = 'ResourceHacker.exe -extract "%s", "%s_icon.rc",  Icon,,' % (s_RES_file, s_RC_filepath)
        self.runCommand(s_cmd)

        s_cmd = 'type "%s_icon.rc" >> "%s.rc"' % (s_RC_filepath, s_RC_filepath) #路径用""引起来可以避免空格带来的问题
        self.runCommand(s_cmd)

    
    def convertRCToRES(self, s_RC_file, s_RES_folder):
        '''
        s_RC_file: RC文件，需要具体的文件名及后缀
        s_RES_folder：存放res文件的文件夹路径，不需要有后缀
        '''
        s_filename = os.path.splitext(os.path.split(s_RC_file)[1])[0]
        s_RES_filepath = os.path.join(s_RES_folder, s_filename)

        s_cmd = 'ResourceHacker.exe -open "%s" -save "%s.res" -action compile -log NUL' % (s_RC_file, s_RES_filepath) #路径用""引起来可以避免空格带来的问题
        self.runCommand(s_cmd)


       

