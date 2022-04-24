import os
import re
import os.path
from os.path import join
import sys

sys.path.append(r'd:\dev\NormingWork\src\Common')

import ReplaceInFile
import VB6MakeFiles
import UpgradeVersionUtil


def upgrade_and_comple(s_VBCode_path, s_vbexe_path, s_compile_to) :
    print('----------------------upgrade_and_comple------------------------------------')
        
    s_vbpath = s_VBCode_path
    #UpgradeVersionUtil.upgrade_vb_projects(s_vbpath, s_compile_to, "AM", '69A', True, '0')

    os.chdir(s_vbexe_path)
    VB6MakeFiles.make_vb_projects(s_VBCode_path, s_vbexe_path, s_compile_to + r'AM69A\CHN')


if __name__ == '__main__' :
    s_compile_to = r'C:\\Sage300\\' #必须使用两个反斜线，否则字符串中包含\S会报错
    s_vb_home = r'C:\Program Files (x86)\Microsoft Visual Studio\VB98'
    s_UI_home = r'D:\Working\WeeklyWorking\0ThisWeek\AM69ACHN'
    s_View_home = r'D:\Pluswdev\AM67A\ViewSource'
    
    #upgrade_and_comple(s_UI_home, s_vb_home, s_compile_to)
    VB6MakeFiles.change_vb_projects_compatible(s_UI_home, "2")
    #VB6MakeFiles.make_vb_projects(s_UI_home, s_vb_home)

    #UpgradeVersionUtil.upgrade_view_projects(s_View_home, 'AM', '67A', '66')
    #UpgradeVersionUtil.upgrade_view_template(s_View_home, 'AM', '67A')

    #s = []
    #s.append('D:\Pluswdev2012\AM66A\UISource\Accounting\Adjustment\AdjustEntry\AccpacAM1020\AccpacAM1020.vbp')
    #s.append('D:\Pluswdev2012\AM66A\UISource\Accounting\Aquisition\AcquistionEntry\AccpacAM1013\AccpacAM1013.vbp')
    #s.append('D:\Pluswdev2012\AM66A\UISource\Reports\Setup\Category\AccpacAM1052\AccpacAM1052.vbp')
    #s.append('D:\Pluswdev2012\AM66A\UISource\Setup\CapitalizationBudgets\AccpacAM1084\AccpacAM1084.vbp')
    #s.append('D:\Pluswdev2012\AM66A\UISource\Setup\Responsibilities\AccpacAM1096\AccpacAM1096.vbp')
    #s.append('D:\Pluswdev2012\AM66A\UISource\Tracking\AssetTrackingBatch\AccpacAM1100\AccpacAM1100.vbp')
    #s.append('D:\Pluswdev2012\AM66A\UISource\Tracking\LocationDownload\AccpacAM1112\AccpacAM1112.vbp')
