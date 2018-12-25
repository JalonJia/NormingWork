import os
import os.path
from os.path import join #这样引入之后，join就可以直接使用了
import shutil
from ReplaceInFile import replace_infile

'''
TODO: 提供以下功能：
1. 找到指定目录下的VB文件，将Back Color设置为Default
'''

class ChangeColor(object):
    '''
    找到指定目录下的VB文件，将Back Color设置为Default
    '''

    @staticmethod
    def upgrade_files(s_VBCode_path, file_encoding='UTF-8') :
        """
        TODO: 将目录下面.ctl和.frm文件中的SetControlsBackColor ***, Me.BackColor替换为 SetControlsBackColor ***, mDefaultBackColor
        """
        print('----------------------upgrade files------------------------------------')

        #replace from *.ctl and *.frm
        s_from_list = [r'(.*)SetControlsBackColor(.*)Me.BackColor', r'(.*)Let BackColor = Me.BackColor']
        s_to_list = [r'\1SetControlsBackColor\2mDefaultBackColor', r'\1Let BackColor = mDefaultBackColor']

        for root, dirs, files in os.walk(s_VBCode_path): #files会得到目录下的文件（不包括文件夹）；dirs会获取到每个文件夹下面的子目录；root会遍历每个子文件夹
            # print('Current Folder: ', root)
            for file in files:
                s_filename = os.path.splitext(file)[0] #文件名
                s_filetype = os.path.splitext(file)[1] #文件后缀
                
                s_filepath = os.path.join(root, file)
                if not (os.path.exists(s_filepath)):
                    continue

                if (s_filetype == '.ctl') or (s_filetype == '.frm') :
                    #print(f'Current File: {s_filepath}')
                    replace_infile(s_filepath, s_from_list, s_to_list, file_encoding)
                
       

