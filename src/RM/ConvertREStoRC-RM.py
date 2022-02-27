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
然后将ENG文件改成FRA
'''
if __name__ == '__main__' :
    s_UI_home = r'D:\Pluswdev\EN69A\VBSource' 
    s_runner_home = r'D:\Dev\ResourceHacker'
    s_RC_save_home = r'D:\Pluswdev\EN69A\EN69AFRA'
    s_RC_save_home = r'D:\Pluswdev\EN69A\EN69AFRA\VBSource'
    
    #CopyENGProject.CopyENGProject.copyAndChangeLanguage(s_UI_home, s_RC_save_home, 'FRA')
    #CopyENGProject.CopyENGProject.convertRESToRC(s_runner_home, s_UI_home, s_RC_save_home, 'FRA')
    #CopyENGProject.CopyENGProject.translateRCtoLang(s_runner_home, s_RC_save_home, s_RC_save_home, 'fr')
    #CopyENGProject.CopyENGProject.convertRCToRES(s_runner_home, s_RC_save_home, s_RC_save_home)

    s_failed = []
    # s_failed.append(r'D:\Pluswdev\EN69A\EN69AFRA\VBSource\Workflow\SMTPTemp\AccpacEN1201')
    # s_failed.append(r'D:\Pluswdev\EN69A\EN69AFRA\VBSource\Setup\PayCode\AccpacEN1030')
    # s_failed.append(r'D:\Pluswdev\EN69A\EN69AFRA\VBSource\Setup\ExpCode\AccpacEN1010')
    # s_failed.append(r'D:\Pluswdev\EN69A\EN69AFRA\VBSource\Project\ProjectRoles\AccpacEN8004')
    # s_failed.append(r'D:\Pluswdev\EN69A\EN69AFRA\VBSource\Project\Maintenance\AccpacEN8007')
    # s_failed.append(r'D:\Pluswdev\EN69A\EN69AFRA\VBSource\Overtime\OvertimeRules\AccpacEN2021')
    # s_failed.append(r'D:\Pluswdev\EN69A\EN69AFRA\VBSource\Employees\EmployeeTemplate\AccpacEN1011')
    # s_failed.append(r'D:\Pluswdev\EN69A\EN69AFRA\VBSource\Employees\Employee Register\AccpacEN1013')
    # s_failed.append(r'D:\Pluswdev\EN69A\EN69AFRA\VBSource\Activate\AccpacEN0000')
    s_failed.append(r'D:\Pluswdev\EN69A\EN69AFRA\VBSource\Workflow\Workflow\AccpacEN1024')
    for s in s_failed:
        CopyENGProject.CopyENGProject.convertRCToRES(s_runner_home, s, s)

    
