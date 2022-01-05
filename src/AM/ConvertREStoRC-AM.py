import os
import os.path
from os.path import join #这样引入之后，join就可以直接使用了
import shutil
import sys

sys.path.append(r'D:\Dev\NormingWork\src\Common')
import RESTool
import CopyENGProject

'''
TODO: 使用Resource Hacker将RES文件中的字符串提取出来生成rc文件
然后将ENG文件改成CHN
'''

s_UI_home = r'C:\Pluswdev\EN67A\VBSource' #\\Activation
s_runner_home = r'D:\Dev\ResourceHacker'
s_RC_save_home = r'C:\Pluswdev\EN67A\EN67ACNT'

#Test Funtions
#sPath = "D:\Pluswdev\AM65A\UISource"
#print(os.listdir(sPath))
#print(os.path.split(sPath)) #将路径分解成两部分，第一部分从开始到最后一个路径分隔符，最后一个分隔符后面的路径\
#sPath = 'D:\\ACCPAC\\AM65A\\am.ini'
#print(os.path.dirname(sPath)) #路径的第一部分
#print(os.path.basename(sPath)) #路径的第二部分
#print(os.path.splitext(sPath))

#os.chdir(s_runner_home)


s_UI_home = r'D:\Documents\OEMDocuments\RMDocs\RM67A\PU1\Temp' #\\Activation
s_runner_home = r'D:\Dev\ResourceHacker'
s_RC_save_home = r'D:\Documents\OEMDocuments\RMDocs\RM67A\PU1\Temp'


CopyENGProject.CopyENGProject.copyFiles(s_UI_home, s_RC_save_home)

CopyENGProject.CopyENGProject.convertRESToRC(s_runner_home, s_UI_home, s_RC_save_home)

