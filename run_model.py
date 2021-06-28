#feature engineering: https://alphascientist.com/feature_engineering.html
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import pickle
from tqdm.notebook import tqdm
import matplotlib.pyplot as plt
import gc
from lightgbm import LGBMClassifier, LGBMRegressor
import lightgbm
from time import time
df = pd.read_feather('/kaggle/input/stonk-size-explosion/features')
from dateutil.relativedelta import relativedelta
import datetime

from pip._internal import main as pipmain
pipmain(['install', 'git+https://github.com/Ottpocket/Helper_Functions.git'])
from Helper_Functions import reduce_mem_usage, get_val_test_increments

df = pd.read_feather('/kaggle/input/create-stonk-data-from-daily-prices/stonk_df')

base = ['day','open','high','low','close','adjclose','volume','ticker']
targets = [target for target in df.columns if 'T_' in target]
final = df[base + targets]
final['preds'] = 0

TEST_DATES = get_val_test_increments(end_date = end_date, test_start = test_start, intervals = intervals)
start_day = TEST_DATES[0][0]
df = df.loc[(df.day >=start_day), FEATURES].copy()
################################################################################
#Backtester: Trains model from set start date to set stop date.  Tests over next
# specified time period.  Does this until specified end date.
#INPUTS:
    #experiment_name: (str) name of experiment
    #data_start_date: ('yyyy-mm-dd') date beginning train data
    #test_start_date: ('yyyy-mm-dd') date beginning test data
    #end_date: ('yyyy-mm-dd') final date in test data
    #intervals: ('2week','month','year') how often to test data
    #model: model that has a fit and predict method
    #val_period: (int) number of days prior to test with which to validate

def get_preds(stonks, experiment_name, data_start_date, test_start, end_date, intervals, model,
             FEATURES, TARGET, val_period = None):
    stonks[experiment_name] = -99
    start_msk = stonks['day'] > data_start_date

    #Gives list of tuples.  Each tuple is start and end dates for test
    TEST_DATES = get_val_test_increments(end_date = end_date, test_start = test_start, intervals = intervals)
    TEST_DATES.reverse()
    for i, (train_start, test_start, test_finish) in tqdm(enumerate(TEST_DATES)):
        print(f'iteration {i} of {len(TEST_DATES)}')
        #Creating temporary train
        msk = (stonks.day < test_start) & (stonks['day'] > train_start)
        train = np.zeros( (np.sum(msk), len(FEATURES)), dtype=np.float32)
        for col_idx, feat in enumerate(FEATURES):
            train[:,col_idx] = stonks.loc[msk, feat].values.astype(np.float32)

        train_TARGET = stonks.loc[msk, TARGET].values
        del msk; gc.collect()
        print('finished train')

        #Creating temporary test
        test_msk = (stonks.day>=test_start) & (stonks.day <= test_finish) & (~stonks[TARGET].isnull())
        test = np.zeros( (np.sum(test_msk), len(FEATURES)), dtype=np.float32)
        for col_idx, feat in enumerate(FEATURES):
            test[:,col_idx] = stonks.loc[test_msk, feat].values.astype(np.float32)
        print('Finished test')


        #Getting preds if test exists
        if test.shape[0] >0:
            #Training model
            model.fit(train, train_TARGET)
            stonks.loc[test_msk, experiment_name] = model.predict(test)
            print(f'Model Finished')

        print(f'Test Start: {test_start}, Test Finish: {test_finish} ,Train: {train.shape}, Test: {test.shape}')
        print()
        del train, test, test_msk; gc.collect()

model = LGBMRegressor()
TARGET = '2_week_high'
FEATURES = list(df.columns.drop([TARGET, 'day', 'ticker']))
start_ = time()
get_preds(df, 'cow_exp', '2000-01-01', '2007-01-01','2021-03-01', 'month', model, FEATURES, TARGET)
print(f'Took {time() - start_ :.2f} seconds')
