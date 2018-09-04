import os
import os.path
from os.path import join #这样引入之后，join就可以直接使用了


sPath = "D:\ACCPAC\AM65A"
#print(os.listdir(sPath))

#Test Funtions
#print(os.path.split(sPath)) #将路径分解成两部分，第一部分从开始到最后一个路径分隔符，最后一个分隔符后面的路径\
#sPath = 'D:\\ACCPAC\\AM65A\\am.ini'
#print(os.path.dirname(sPath)) #路径的第一部分
#print(os.path.basename(sPath)) #路径的第二部分
#print(os.path.splitext(sPath))
#os.makedirs(path) #创建多级目录

s_vb_home = 'C:\Program Files (x86)\Microsoft Visual Studio\VB98'
os.chdir(s_vb_home)

print('----------------------------------------------------------')

s_AMUI_home = 'D:\\Pluswdev2016\\AM65A\\UISource\\'
for root, dirs, files in os.walk(s_AMUI_home): #files会得到目录下的文件（不包括文件夹）；dirs会获取到每个文件夹下面的子目录；root会遍历每个子文件夹
    print('Folder: ', root)
    for file in files:
        s_filename = os.path.splitext(file)[0] #文件名
        s_filetype = os.path.splitext(file)[1] #文件后缀
        #print(s_filetype)
        if (s_filetype == '.vbp') and (s_filename[-3:] != 'EXE') and (len(s_filename) >= len('ACCPACAM0000')) :
            s_filepath = os.path.join(root, file)
            
            if os.path.exists(s_filepath):
                print(s_filepath)
                fp = os.popen('vb6.exe /make "%s"' % s_filepath) #路径用""引起来可以避免空格带来的问题
                fpread = fp.read()
                print(fpread)




