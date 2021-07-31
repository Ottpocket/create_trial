################################################################################
#In charge of kicking off all python scripts to kaggle
################################################################################
import argparse
import os
import sys
import string
import random
import subprocess

sys.path.append('/home/aott/Documents/python_scripts/Helper_Functions/Helper_Functions')
from __init__ import create_json

######################################
#Get dict of all models to be tested
######################################
all_days = [3, 5, 10, 20, 50, 100, 200]
all_train_months = [1,2,3,6,12]
all_targets = ['T_high_max_5', 'T_openClose_lag_-1']
PARAMETERS_FOR_MODELS = {} #Dict with hash as key and parameters as value
for n_days in range(1, len(all_days)+1):
    days = all_days[:n_days]
    for months in all_train_months:
        for target in all_targets:
            model_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            PARAMETERS_FOR_MODELS[model_name] = {'FEATURES': days,
                                                 'TARGET': months,
                                                  'TRAIN_MONTHS': target}


#put models in queue and run n simultanious models on kaggle
MAX_KAGGLE_KERNELS_RUNNING = 5
active_models_on_kaggle = {}#Model:status either model or backtest
for idx, key in enumerate(PARAMETERS_FOR_MODELS.keys()):

    FEATURES = PARAMETERS_FOR_MODELS[key][FEATURES]
    TARGET = PARAMETERS_FOR_MODELS[key][TARGET]
    TRAIN_MONTHS = PARAMETERS_FOR_MODELS[key][TRAIN_MONTHS]

    #kickoff model in kaggle
    kick_off_model(FEATURES, TARGET, TRAIN_MONTHS)
    active_programs_on_kaggle[key] = 'model'


    if idx == (len(PARAMETERS_FOR_MODELS.keys()) - 1):
        condition = len(active_models_on_kaggle.keys()) > MAX_KAGGLE_KERNELS_RUNNING
    else:
        condition = len(active_models_on_kaggle.keys()) ==0
    while condition:
        for running_key in active_models_on_kaggle.keys():



            #help from https://stackoverflow.com/questions/4760215/running-shell-command-and-capturing-the-output
            if active_models_on_kaggle[running_key] == 'model'
                status = subprocess.run(f'kaggle kernels status Ottpocket/{running_key}'.split(' '), stdout=subprocess.PIPE)
                if 'complete' in status:
                    #Kick off backest for model
                    pass
                    active_models_on_kaggle[running_key] = 'backtest'

            elif active_models_on_kaggle[running_key] == 'backtest':
                status = subprocess.run(f'kaggle kernels status Ottpocket/{running_key}'.split(' '), stdout=subprocess.PIPE)
                 if 'complete' in status:
                     active_models_on_kaggle[running_key] = 'complete'

            #elif check errored status

        #Delete all completed and errored out
        for key in active_models_on_kaggle.keys():
            if active_models_on_kaggle[key].isin(['complete','error']):
                del active_models_on_kaggle[key]

        
        if idx == (len(PARAMETERS_FOR_MODELS.keys()) - 1):
            condition = len(active_models_on_kaggle.keys()) > MAX_KAGGLE_KERNELS_RUNNING
        else:
            condition = len(active_models_on_kaggle.keys()) ==0
