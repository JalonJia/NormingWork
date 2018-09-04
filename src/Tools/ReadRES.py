'''
Created on 2018年5月8日

@author: jalon
'''

import os
import os.path
from os.path import join
import tempfile #文件缓存
import codecs #打开其他编码的文件


s_path = 'C:\\Working\\WeeklyWorking\\20180507'
s_file = join(s_path, "AccpacAM1103ENG.Rc")

#s_vb_home = 'C:\Program Files (x86)\Microsoft Visual Studio\VB98'
os.chdir(s_path)

char_set = []
#with方式打开文件不需要关闭
#with open(s_file, 'r', encoding='UTF-8', errors='ignore' ) as f:
with open(s_file, 'r' ) as f:
    #print(f.read())
    for s_line in f.readlines():        
        print(s_line)
        char_set.append(s_line)
            
print(char_set)

