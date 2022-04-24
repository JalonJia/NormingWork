import sys

sys.path.append(r'd:\dev\NormingWork\src\Common')
import VB6MakeFiles

'''
TODO: 编译所有的RM VB界面
'''

if __name__ == '__main__':
    s_vb_home = 'C:\Program Files (x86)\Microsoft Visual Studio\VB98'
    s_UICode_home = r'D:\Pluswdev\EN69A\EN69AFRA\VBSource'
    s_out_dir = r'C:\Sage300\EN69A\FRA'
    #VB6MakeFiles.change_vb_projects_compatible(s_UICode_home, "2")
    VB6MakeFiles.make_vb_projects(s_UICode_home, s_vb_home, s_out_dir)

    s_failed = []
    #s_failed.append(r'D:\Pluswdev\EN66A\VBSource\Budget\Budget Maintenance\AccpacEN3505\')
    #s_failed.append(r'D:\Pluswdev\EN66A\VBSource\Budget\Budget Request List\AccpacEN3503')
    #s_failed.append(r'D:\Pluswdev\EN66A\VBSource\Requisitions\CustomRequisitionType\AccpacEN9132')
    #s_failed.append(r'D:\Pluswdev\EN66A\VBSource\Transaction\ExpenseTracking\AccpacEN1056')
    for s in s_failed:
        VB6MakeFiles.make_vb_projects(s, s_vb_home, s_out_dir)
    



