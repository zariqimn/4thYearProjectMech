import os
import subprocess

def sub_run1(argument, directory):
    os.chdir(directory)
    #print(argument)
    subprocess.Popen(argument, shell=True)
    
    
def sub_run2(argument, directory):
    os.chdir(directory)
    #print(argument)
    subprocess.run(argument, shell=True)
    