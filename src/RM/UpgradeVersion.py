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
        
    smodule = 'EN'
    #UpgradeVersionUtil.upgrade_vb_projects(s_VBCode_path, s_compile_to, smodule, '66A', True)
    #UpgradeVersionUtil.upgrade_view_projects(s_ViewCode_home, smodule, '66A', '65')

    os.chdir(s_vbexe_path)
    VB6MakeFiles.comple_vb_projects_compatible(s_VBCode_path, s_vbexe_path, "0", "2")



if __name__ == '__main__' :
    sToPath = r"D:\\ACCPAC\\"
    s_vb_home = r'C:\Program Files (x86)\Microsoft Visual Studio\VB98'
    s_UI_home = r'D:\Pluswdev2012\EN66A\VBSource'
    s_View_home = r'D:\Pluswdev2012\EN66A\Source\Cprogram'
    upgrade_and_comple(s_View_home, s_UI_home, s_vb_home, sToPath)
    #VB6MakeFiles.comple_vb_projects_compatible(s_UI_home, s_vb_home, "0", "2")
    #VB6MakeFiles.make_vb_projects(s_UI_home, s_vb_home)

    s_failed = []
    s_failed.append('D:\Pluswdev2012\EN66A\VBSource\Budget\Budget Maintenance\AccpacEN3505\AccpacEN3505.vbp')
    s_failed.append('D:\Pluswdev2012\EN66A\VBSource\ESS Portal\DatabaseSetup\AccpacEN1026\AccpacEN1026.vbp')
    s_failed.append('D:\Pluswdev2012\EN66A\VBSource\ESS Portal\Ess Groups\AccpacEN1020\AccpacEN1020.vbp')
    s_failed.append('D:\Pluswdev2012\EN66A\VBSource\Requisitions\PurchaseRequisitionEntry\AccpacEN9102\ENPORequesition.vbp')
    s_failed.append('')
    s_failed.append('')
    s_failed.append('')
    s_failed.append('')
    s_failed.append('')
    s_failed.append('')
    s_failed.append('')
    s_failed.append('')
        

