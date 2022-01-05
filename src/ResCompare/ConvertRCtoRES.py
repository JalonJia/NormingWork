import os
import os.path
from os.path import join #这样引入之后，join就可以直接使用了
import shutil
import sys

sys.path.append(r'D:\Dev\NormingWork\src\Common')
import RESTool
import CopyENGProject

'''
TODO: 使用Resource Hacker将rc文件转成RES文件
'''

s_runner_home = r'D:\Dev\ResourceHacker'
#s_UI_home = r'C:\Pluswdev\EN67A\EN67ACHT\VBSource\Transaction\ExpEntry\AccpacEN1016' 
#s_UI_home = r'C:\Pluswdev\EN67A\EN67ACHT\VBSource\Requisitions\PORequisitionList\AccpacEN9101' 
#s_UI_home = r'C:\Pluswdev\EN67A\EN67ACHT\VBSource\Requisitions\PurchaseRequisitionEntry\AccpacEN9102'
#s_UI_home = r'C:\Pluswdev\EN67A\EN67ACHT\VBSource\Transaction\ExpenseReportList\AccpacEN1057'
s_UI_home = r'C:\Pluswdev\EN67A\EN67ACHT\VBSource\Transaction\ExpBatch\AccpacEN1015'

s_RES_save_home = s_UI_home

CopyENGProject.CopyENGProject.convertRCToRES(s_runner_home, s_UI_home, s_RES_save_home)

