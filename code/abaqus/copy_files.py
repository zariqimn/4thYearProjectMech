import shutil
import os

current_dir = os.path.dirname(os.path.realpath('__file__'))
folder_directory = current_dir + r'\\model_abaqus_files'
new_file_dir = current_dir + r'\\backup_abaqus_file'
os.mkdir(new_file_dir)
for folders in os.listdir(folder_directory):
    data_dir = folder_directory + r'\\' + folders
    odb = '\\'+folders+'.odb'
    jnl = '\\'+folders +'.jnl'
    cae = '\\'+folders + '.cae'
    data_txt = '\\'+folders+'data.txt'
    shutil.move((data_dir+odb),(new_file_dir+odb))
    shutil.move((data_dir+jnl),(new_file_dir+jnl))
    shutil.move((data_dir+cae),(new_file_dir+cae))
    shutil.move((data_dir+data_txt),(new_file_dir+data_txt))
    shutil.rmtree(data_dir)
    