import sys
import os
from pathname import get_file_name_path
#from explicitsim import dynamic_explicit
#import abaqus
import subprocess
import shutil
from sub_process_run import *
import time

current_directory = os.path.dirname(os.path.realpath('__file__'))

# get the file names
# get file path
file_path, files_name = get_file_name_path()

#make new file
os.mkdir(r'./model_abaqus_files/')

# open cae
c = len(files_name)
count =0
for i in range(0,c,4):
    
    
    new_directory1 = current_directory+ '\\'+r'model_abaqus_files\\'+ files_name[i]
    new_directory2 = current_directory+ '\\'+r'model_abaqus_files\\'+ files_name[i+1]
    new_directory3 = current_directory+ '\\' + r'model_abaqus_files\\' +files_name[i+2]
    new_directory4 = current_directory+ '\\' + r'model_abaqus_files\\' +files_name[i+3]
    
    os.mkdir(new_directory1)
    os.mkdir(new_directory2)
    os.mkdir(new_directory3)
    os.mkdir(new_directory4)
    
    
    shutil.copyfile(current_directory+r'/new1.py', new_directory1+r'/new1.py')
    shutil.copyfile(current_directory+r'/explicitsim.py', new_directory1+r'/explicitsim.py')
    shutil.copyfile(current_directory+r'/abaqus_v6.env', new_directory1+r'/abaqus_v6.env')
    
    shutil.copyfile(current_directory+r'/new1.py', new_directory2+r'/new1.py')
    shutil.copyfile(current_directory+r'/explicitsim.py', new_directory2+r'/explicitsim.py')
    shutil.copyfile(current_directory+r'/abaqus_v6.env', new_directory2+r'/abaqus_v6.env')
    
    shutil.copyfile(current_directory+r'/new1.py', new_directory3+r'/new1.py')
    shutil.copyfile(current_directory+r'/explicitsim.py', new_directory3 +r'/explicitsim.py')
    shutil.copyfile(current_directory+r'/abaqus_v6.env',new_directory3 +r'/abaqus_v6.env')
    
    shutil.copyfile(current_directory+r'/new1.py', new_directory4+r'/new1.py')
    shutil.copyfile(current_directory+r'/explicitsim.py', new_directory4 +r'/explicitsim.py')
    shutil.copyfile(current_directory+r'/abaqus_v6.env',new_directory4 +r'/abaqus_v6.env')

    


    Arguments1 = 'abaqus cae noGUI=' + 'new1.py -- ' + file_path[i] +' ' +files_name[i] + ' ' +new_directory1
    Arguments2 = 'abaqus cae noGUI=' + 'new1.py -- ' + file_path[i+1] +' ' +files_name[i+1] + ' ' +new_directory2
    Arguments3 = 'abaqus cae noGUI=' +'new1.py -- ' + file_path[i+2] + ' ' +files_name[i+2] + ' ' + new_directory3
    Arguments4 = 'abaqus cae noGUI=' +'new1.py -- ' + file_path[i+3] + ' ' +files_name[i+3] + ' ' + new_directory4
    
    
    sub_run1(Arguments1,new_directory1)
    sub_run1(Arguments2,new_directory2)
    sub_run1(Arguments3,new_directory3)
    sub_run2(Arguments4,new_directory4)
    
    txt_path1 = new_directory1 + '\\'+files_name[i]+'data.txt'
    txt_path2 = new_directory2 + '\\'+files_name[i+1]+'data.txt'
    txt_path3 = new_directory3 +  '\\' +files_name[i+2]+'data.txt'
    txt_path4 = new_directory4 +  '\\' +files_name[i+3]+'data.txt'
    
    while not (os.path.isfile(txt_path1) and os.path.isfile(txt_path2) and os.path.isfile(txt_path3) and os.path.isfile(txt_path4)):
        time.sleep(100)
        
    print(f'iteration {count} complete')
    count +=1
        


print('operation finished')  