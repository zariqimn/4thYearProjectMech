import os
import sys



def get_file_name_path():
    current_path = os.path.dirname(os.path.abspath(__file__))
    model_path = r'D:\Temp\mohdhisham_m\automate\models'
    files_name = [os.path.splitext(filename)[0] for filename in os.listdir(model_path)]
    file_path = []
    for i in os.listdir(model_path):
        file_path.append(model_path + '\\'+ i )

    return file_path, files_name
    