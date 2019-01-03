import sys

sys.path.append(r'd:\dev\NormingWork\src\Common')
import VB6MakeFiles

'''
TODO: 编译所有的NP VB界面
'''

if __name__ == '__main__':
    s_vb_home = 'C:\Program Files (x86)\Microsoft Visual Studio\VB98'
    s_UICode_home = r'D:\Pluswdev\NP66A\Source'
    #VB6MakeFiles.make_vb_projects(s_UICode_home, s_vb_home)

    s_failed = []
    s_failed.append(r'D:\Pluswdev\NP66A\Source\Employees\IndividualRepaySchedule\AccpacNP1102')
    s_failed.append(r'D:\Pluswdev\NP66A\Source\Setup\GLInte\AccpacNP1023')
    
    for s in s_failed:
        VB6MakeFiles.make_vb_projects(s, s_vb_home)
    



