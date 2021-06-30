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

#code from https://www.kaggle.com/ottpocket/create-stonk-data-from-daily-prices
for n_days in [3, 5, 10, 20, 50]:
    for feat in ['high', 'totrange']:
        parser.add_argument(f'--{feat}_{n_days}', default='False', type=str,
                            choices = ['True','False'])


#Getting the name of the model from the features selected
args = vars(parser.parse_args())
keys = sorted(list(args.keys()))
model_name = ''
features_list = []
for key in keys:
    if args[key]=='True':
        model_name += key+'_'
        features_list.append(key)



#1) and 2) Create Folder; place json in folder
DIRECTORY = '/home/aott/Documents/python_scripts/kaggle_stonk_directories'
NEW_DIRECTORY = create_json(model_name, DIRECTORY=DIRECTORY)

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
                            features_list)
with open(file_destination, 'w') as file:
  file.write(filedata)


#4) Call kaggle api
#help from https://janakiev.com/blog/python-shell-commands/
#os.system(f'kaggle kernels push -p {NEW_DIRECTORY}')
