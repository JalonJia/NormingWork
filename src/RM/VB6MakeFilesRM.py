import sys

sys.path.append(r'd:\dev\NormingWork\src\Common')
import VB6MakeFiles

'''
TODO: 编译所有的RM VB界面
'''

if __name__ == '__main__':
    s_vb_home = 'C:\Program Files (x86)\Microsoft Visual Studio\VB98'
    s_UICode_home = r'D:\Pluswdev2012\EN65A\VBSource'
    #VB6MakeFiles.make_vb_projects(s_UICode_home, s_vb_home)

    s_failed = []
    # s_failed.append(r'D:\Pluswdev2012\EN65A\VBSource\Requisitions\CustomRequisitionType\AccpacEN9132')
    # s_failed.append(r'D:\Pluswdev2012\EN65A\VBSource\Project\Maintenance\AccpacEN8007')
    # s_failed.append(r'D:\Pluswdev2012\EN65A\VBSource\Timesheet\TimesheetEntry\AccpacEN2006')
    # s_failed.append(r'D:\Pluswdev2012\EN65A\VBSource\Requisitions\PJCEstimateInquiry\AccpacEN9106')
    # s_failed.append(r'D:\Pluswdev2012\EN65A\VBSource\Setup\ExpenseSetup\ExpenseOptions\AccpacEN1042')
    # s_failed.append(r'D:\Pluswdev2012\EN65A\VBSource\Requisitions\APInvoiceRequistionEntry\AccpacEN9122')
    # s_failed.append(r'D:\Pluswdev2012\EN65A\VBSource\Requisitions\CustomReportType\AccpacEN9151')
    # s_failed.append(r'D:\Pluswdev2012\EN65A\VBSource\Project\Templates\AccpacEN8006')
    # s_failed.append(r'D:\Pluswdev2012\EN65A\VBSource\Overtime\OvertimeBank')
    # s_failed.append(r'D:\Pluswdev2012\EN65A\VBSource\Overtime\OvertimeCalculate')
    # s_failed.append(r'D:\Pluswdev2012\EN65A\VBSource\Budget\Budget Request List')
    # s_failed.append(r'D:\Pluswdev2012\EN65A\VBSource\Budget\Budget Maintenance')
    # s_failed.append(r'D:\Pluswdev2012\EN65A\VBSource\Leave\LeaveAccount')
    
    for s in s_failed:
        VB6MakeFiles.make_vb_projects(s, s_vb_home)
    



