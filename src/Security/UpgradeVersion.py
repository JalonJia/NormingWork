import os
import re
import os.path
from os.path import join
import sys

sys.path.append(r'd:\dev\NormingWork\src\Common')
import ReplaceInFile
import VB6MakeFiles
import UpgradeVersionUtil


def upgrade_and_comple(s_ViewCode_home, s_VBCode_path, s_vbexe_path, s_compile_to) :
    print('----------------------upgrade_and_comple------------------------------------')
        
    s_modules = ['IS', 'AQ', 'BS', 'VS', 'PS', 'SS']
    for smodule in s_modules:
        s_vbpath = s_VBCode_path + f'\\{smodule}66A\\UISource' 
        UpgradeVersionUtil.upgrade_vb_projects(s_vbpath, s_compile_to, smodule, '66A', True)
        s_viewpath = s_ViewCode_home + f'\\{smodule}66A\\ViewSource' 
        UpgradeVersionUtil.upgrade_view_projects(s_viewpath, smodule, '66A')

    os.chdir(s_vbexe_path)
    VB6MakeFiles.comple_vb_projects_compatible(s_VBCode_path, s_vbexe_path, "0", "2")



if __name__ == '__main__' :
    sPath2 = r"D:\\ACCPAC\\"
    s_vb_home = r'C:\Program Files (x86)\Microsoft Visual Studio\VB98'
    s_UI_home = r'D:\Pluswdev2012\Security\Sec2019'
    s_View_home = r'D:\Pluswdev2012\Security\Sec2019'
    #upgrade_and_comple(s_View_home, s_UI_home, s_vb_home, sPath2)
    #VB6MakeFiles.comple_vb_projects_compatible(s_UI_home, s_vb_home, "0", "2")
    #VB6MakeFiles.make_vb_projects(s_UI_home, s_vb_home)

    s_modules = ['SS'] #, 'IS', 'AQ', 'BS', 'VS', 'PS', 'SS']
    for smodule in s_modules:
        s_viewpath = s_UI_home + f'\\{smodule}66A\\ViewSource' 
        UpgradeVersionUtil.upgrade_view_projects_from2005_security(s_viewpath, smodule, '66A')
        UpgradeVersionUtil.upgrade_view_template(s_viewpath, smodule, '66A')


