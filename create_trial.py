################################################################################
#Script to send a trial to kaggle to run
# Creates
    #1) a directory for kaggle kernel in specified location
    #2) a kernel.py file in the directory
    #3) a kernel-metadata.json in the directory
################################################################################

import os
import sys
import json

DIRECTORY =  '/home/aott/Documents/python_scripts/kaggle_stonk_directories'
TRIAL_NAME = sys.argv[1]
KAGGLE_NAME = 'Ottpocket'



path = os.path.join(DIRECTORY, TRIAL_NAME)
if os.path.exists(path):
    raise Exception('f{path} exists')
else:
    os.mkdir(path)


#Creating a json file from dictionary
#help from https://pythonexamples.org/python-write-json-to-file/
json_dict = {
  "id": f"{KAGGLE_NAME}/{TRIAL_NAME}",
  "title": f"{TRIAL_NAME}",
  "code_file": f"{TRIAL_NAME}.py",
  "language": "python",
  "kernel_type": "script",
  "is_private": "true",
  "enable_gpu": "false",
  "enable_internet": "true",
  "dataset_sources": ["ottpocket/daily-stonk-database"],
  "competition_sources": [],
  "kernel_sources": ["ottpocket/create-stonk-data-from-daily-prices"]
}

json_path = os.path.join(path, "kernel-metadata.json")
jsonString = json.dumps(json_dict)
jsonFile = open(json_path, "w")
jsonFile.write(jsonString)
jsonFile.close()
