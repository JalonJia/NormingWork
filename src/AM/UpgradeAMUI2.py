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
    UpgradeVersionUtil.upgrade_vb_projects(s_vbpath, s_compile_to, "AM", '66A', True, '2')

    os.chdir(s_vbexe_path)
    VB6MakeFiles.make_vb_projects(s_VBCode_path, s_vbexe_path)


if __name__ == '__main__' :
    sPath2 = r"D:\\ACCPAC\\"
    s_vb_home = r'C:\Program Files (x86)\Microsoft Visual Studio\VB98'
    s_UI_home = r'D:\Pluswdev2012\AM66A\UISource'
    #s_View_home = r'D:\Pluswdev2012\Security\Sec2019'
    
    upgrade_and_comple(s_UI_home, s_vb_home, sPath2)
    #VB6MakeFiles.comple_vb_projects_compatible(s_UI_home, s_vb_home, "0", "2")
    #VB6MakeFiles.make_vb_projects(s_UI_home, s_vb_home)


    s = []
    s.append('D:\Pluswdev2012\AM66A\UISource\Accounting\Adjustment\AdjustEntry\AccpacAM1020\AccpacAM1020.vbp')
    #s.append('D:\Pluswdev2012\AM66A\UISource\Accounting\Aquisition\AcquistionEntry\AccpacAM1013\AccpacAM1013.vbp')
    #s.append('D:\Pluswdev2012\AM66A\UISource\Reports\Setup\Category\AccpacAM1052\AccpacAM1052.vbp')
    #s.append('D:\Pluswdev2012\AM66A\UISource\Setup\CapitalizationBudgets\AccpacAM1084\AccpacAM1084.vbp')
    #s.append('D:\Pluswdev2012\AM66A\UISource\Setup\Responsibilities\AccpacAM1096\AccpacAM1096.vbp')
    s.append('D:\Pluswdev2012\AM66A\UISource\Tracking\AssetTrackingBatch\AccpacAM1100\AccpacAM1100.vbp')
    s.append('D:\Pluswdev2012\AM66A\UISource\Tracking\LocationDownload\AccpacAM1112\AccpacAM1112.vbp')
