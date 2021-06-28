###################################################
#Pushes local python script to kaggle to run.
#Specifically, this
#1)  Creates EXPERIMENT_FOLDER in /Documents/python_scripts/create_trial/
#2)  Places json file in above folder
#3)  Places run_model.py in above folder
#4)  calls kaggle api to push script to kaggle


#For help with argparse, https://github.com/somepago/saint/blob/main/train.py
import argparse
import os
import sys
sys.path.append('/home/aott/Documents/python_scripts/Helper_Functions/Helper_Functions')
from __init__ import create_json

parser = argparse.ArgumentParser()
#parser.add_argument('--model_name', required = True) #Now created from features
parser.add_argument('--baseline', default='True', type=bool,
                    choices = ['True','False'])
parser.add_argument('--high_3', default='False', type=bool,
                    choices = ['True','False'])
parser.add_argument('--high_5', default='False', type=bool,
                    choices = ['True','False'])

args = parser.parse_args()


#1) and 2) Create Folder; place json in folder
DIRECTORY = '/home/aott/Documents/python_scripts/kaggle_stonk_directories'
NEW_DIRECTORY = create_json(args.model_name, DIRECTORY=DIRECTORY)

#3) Place .py code in folder
from shutil import copyfile
FILE = 'run_model.py'
SOURCE = '/home/aott/Documents/python_scripts/create_trial'
file_source = os.path.join(SOURCE, FILE)
file_destination = os.path.join(NEW_DIRECTORY, FILE)
copyfile(file_source, file_destination)

#Adding the parameters to the copied file_source Read in the file
#help from https://stackoverflow.com/questions/17140886/how-to-search-and-replace-text-in-a-file
with open(file_destination, 'r') as file :
  filedata = file.read()

filedata = filedata.replace('TO_BE_REPLACED_IN_COPY',
                            'abcd')
with open(file_destination, 'w') as file:
  file.write(filedata)


#4) Call kaggle api
#help from https://janakiev.com/blog/python-shell-commands/
os.system(f'kaggle kernels push -p {NEW_DIRECTORY}')
