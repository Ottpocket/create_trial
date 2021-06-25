###################################################33
#Pushes local python script to kaggle to run.
#Specifically, this
#1)  Creates EXPERIMENT_FOLDER in /Documents/python_scripts/create_trial/
#2)  Places run_model.py in above folder
#3)  Places json file in above folder
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
print(args.model_name)

#1) and 3)
create_json(args.model_name)
