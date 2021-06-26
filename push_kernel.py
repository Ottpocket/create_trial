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
parser.add_argument('--model_name')
parser.add_argument('--cont_embeddings', default='MLP', type=str,choices = ['MLP','Noemb','pos_singleMLP'])
args = parser.parse_args()


#1) and 2)
DIRECTORY = '/home/aott/Documents/python_scripts/kaggle_stonk_directories'
create_json(args.model_name, DIRECTORY=DIRECTORY)

#3)
from shutil import copyfile
FILE = 'run_model.py'
SOURCE = '/home/aott/Documents/python_scripts/create_trial'
copyfile(os.path.join(SOURCE, FILE), os.path.join(DIRECTORY, FILE))
