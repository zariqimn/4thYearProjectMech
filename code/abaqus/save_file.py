import os
import sys
import csv


folder_directory = os.path.dirname(os.path.realpath('__file__')) + r'\\model_abaqus_files'

folder_name = []
data_list = []
for folders in os.listdir(folder_directory):
    data_directory = folder_directory + '\\' + folders
    folder_name.append(folders)
    text_doc_name = folders + 'data.txt'
    txt_directory = data_directory + '\\' + text_doc_name
    
    with open(txt_directory, 'r') as file:
        temp = file.readlines()
        data = [float(line.strip()) for line in temp]
        data_list.append(data)
        
main_path = os.path.dirname(os.path.realpath('__file__'))
csv_name = r'\\data.csv'
csv_path = main_path + csv_name
csv_foldernames = r'\\folder_order.csv'
folders_name_path_csv = main_path + csv_foldernames

with open(csv_path,'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    for i in data_list:
        writer.writerow(i)

with open(folders_name_path_csv,'w', newline='') as csv_file_folder:
    writer = csv.writer(csv_file_folder)
    for i in folder_name:
        writer.writerow(i)