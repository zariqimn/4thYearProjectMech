#Imports
import os, subprocess, json, shutil, time, numpy as np, random


#Assuming this script, ntop file, and json files will be in the same folder
Current_Directory = os.path.dirname(os.path.realpath('__file__')) 
exePath = r"D:\ntopology\nTopCL.exe"  #nTopCL path
nTopFilePath = r"26stapril.ntop"   #nTop notebook file name
Input_File_Name = "input_template.json"      #JSON input file name to be saved as
Output_File_Name = "output_template.json"       #JSON output file name to be saved as

#Input variables in JSON structure
Inputs_JSON = {
    "description": "",
    "inputs": [
        {
            "description": "",
            "name": "shell thickness",
            "type": "real",
            "units": "mm",
            "value": 3.0
        },
        {
            "description": "",
            "name": "Approx. thickness",
            "type": "real",
            "units": "mm",
            "value": 1.5
        },
        {
            "description": "",
            "name": "cell size",
            "type": "real",
            "units": "mm",
            "value": 5.0
        }
    ],
    "title": "26stapril"
}

#design variation


#creates data folder to store input and output file
if os.path.isdir('./data_1/'):
    shutil.rmtree('./data_1/')
os.mkdir('./data_1/')
os.mkdir('./fe_model_1/')


#create csv file with summary of run
Header = ['shell thickness', 'lattice thickness', 'cell size', 'mass']
output_file = open('output_1.csv', mode='w')
output_file.write(','.join(Header)+'\n')
output_file.close()


#loop
count = 0
for i in np.arange(4.5,7.0,0.5):
    for j in np.arange(4.0,20.0,0.5):
        start_time =time.time()
         
        Inputs_JSON['inputs'][0]['value'] = i
        Inputs_JSON['inputs'][2]['value'] = j   #cell size
        k = round(random.uniform(1.0,j/4),2)
        Inputs_JSON['inputs'][1]['value'] = k   # thickness
        
        #json and notebook path, multiplied 100 to remove decimal
        l = int(i*100)
        m = int(j*100)
        n = int(k*100)
        os.mkdir('./data_1/'+str(l)+'_'+str(n)+'_'+str(m))
        input_path = './data_1/'+str(l)+'_'+str(n)+'_'+str(m)+'/'+Input_File_Name
        output_path = './data_1/'+str(l)+'_'+str(n)+'_'+str(m)+'/'+Output_File_Name
        notebook_path = nTopFilePath
        shutil.copyfile('./'+Input_File_Name,input_path )
        
        #nTopCL arguments in a list
        Arguments = [exePath]               #nTopCL path
        Arguments.append("-j")              #json input argument
        Arguments.append(input_path)   #json path
        Arguments.append("-o")              #output argument
        Arguments.append(output_path)  #output json path
        Arguments.append(notebook_path)      #.ntop notebook file path
        
        #Creating in.json file
        with open(input_path, 'w') as outfile:
            json.dump(Inputs_JSON, outfile, indent=4)
            
        #nTopCL call with arguments
        print(" ".join(Arguments))
        output,error = subprocess.Popen(Arguments,stdout = subprocess.PIPE, stderr= subprocess.PIPE).communicate()
        
        #Print the return messages
        print(output.decode("utf-8"))
        
        #csv output table
        with open(output_path, 'r') as f:
            data = json.load(f)
            mass = data[0]['value']
        summary = [i, j, k, mass]
        output_file = open('output_1.csv', mode='a')
        output_file.write(','.join([str(count) for count in summary])+'\n')
        output_file.close()
        print(summary)
        print('-- %s seconds --'% (time.time()-start_time))
        count += 1
        