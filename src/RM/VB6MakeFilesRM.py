import sys

sys.path.append(r'd:\dev\NormingWork\src\Common')
import VB6MakeFiles

'''
TODO: 编译所有的RM VB界面
'''

if __name__ == '__main__':
    s_vb_home = 'C:\Program Files (x86)\Microsoft Visual Studio\VB98'
    s_UICode_home = r'D:\Pluswdev2012\EN66A\VBSource'
    #VB6MakeFiles.make_vb_projects(s_UICode_home, s_vb_home)

    s_failed = []
    #s_failed.append(r'D:\Pluswdev2012\EN66A\VBSource\Requisitions\APInvoiceRequisitionList\AccpacEN9121')
    #s_failed.append(r'D:\Pluswdev2012\EN66A\VBSource\Requisitions\APInvoiceRequistionEntry\AccpacEN9122')
    #s_failed.append(r'D:\Pluswdev2012\EN66A\VBSource\Requisitions\PurchaseRequisitionEntry\AccpacEN9102')
    s_failed.append(r'D:\Pluswdev2012\EN66A\VBSource\Requisitions\CustomRequisitionType\AccpacEN9132')
    
    for s in s_failed:
        VB6MakeFiles.make_vb_projects(s, s_vb_home)
    



