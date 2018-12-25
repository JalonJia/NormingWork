import sys

sys.path.append(r'd:\dev\NormingWork\src\Common')
import ModifyVBBackColor

'''
TODO: 修改子界面的默认颜色
'''

if __name__ == '__main__' :
    s_UI_home = r'D:\Pluswdev2012\EN65A\VBSource'
    ModifyVBBackColor.ChangeColor.upgrade_files(s_UI_home, file_encoding='ANSI')

