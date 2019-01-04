import sys

sys.path.append(r'd:\dev\NormingWork\src\Common')
import ModifyVBBackColor
import ReplaceInFile

'''
TODO: 修改子界面的默认颜色
'''

if __name__ == '__main__' :
    s_UI_home = r'D:\Pluswdev2012\NP66A\Source'
#    ModifyVBBackColor.ChangeColor.upgrade_files(s_UI_home, file_encoding='ANSI')

    #替换控件版本号
    # s_from_list = [r'(.*)#1.5#0; a4wPeriodPicker.ocx', r'(.*)#1.1#0; a4wGoBtn.ocx']
    # s_to_list = [r'\1#1.4#0; a4wPeriodPicker.ocx', r'\1#1.0#0; a4wGoBtn.ocx']
    # ReplaceInFile.replace_infolder(s_UI_home, s_from_list, s_to_list, ['.vbp'], file_encoding='UTF-8')
    s_from_list = [r'Path32(.*)Sage300(.*)']
    s_to_list = [r'Path32\1ACCPAC\2']
    ReplaceInFile.replace_infolder(s_UI_home, s_from_list, s_to_list, ['.vbp'], file_encoding='UTF-8')

