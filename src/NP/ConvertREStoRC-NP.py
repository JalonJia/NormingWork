import os
import os.path
from os.path import join #这样引入之后，join就可以直接使用了
import shutil
import sys

sys.path.append(r'd:\NormingWork\src\Common')
import RESTool
import CopyENGProject

'''
TODO: 使用Resource Hacker将RES文件中的字符串提取出来生成rc文件
然后将ENG文件改成CHN
'''

s_UI_home = 'D:\\Pluswdev\\NP60A\\Source' #\\Activation
s_runner_home = 'D:\\Software\\ResourceHacker'
s_RC_save_home = 'D:\\NP60AENG'

#Test Funtions
#sPath = "D:\Pluswdev\AM65A\UISource"
#print(os.listdir(sPath))
#print(os.path.split(sPath)) #将路径分解成两部分，第一部分从开始到最后一个路径分隔符，最后一个分隔符后面的路径\
#sPath = 'D:\\ACCPAC\\AM65A\\am.ini'
#print(os.path.dirname(sPath)) #路径的第一部分
#print(os.path.basename(sPath)) #路径的第二部分
#print(os.path.splitext(sPath))

#os.chdir(s_runner_home)


CopyENGProject.CopyENGProject.copyFiles(s_UI_home, s_RC_save_home)

CopyENGProject.CopyENGProject.convertRESToRC(s_runner_home, s_UI_home, s_RC_save_home)


