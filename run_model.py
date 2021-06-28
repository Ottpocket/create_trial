#from https://www.kaggle.com/ottpocket/model-predictions v21

#Base line predictions for a model.
#feature engineering: https://alphascientist.com/feature_engineering.html
import numpy as np
import pandas as pd
import os
import gc
from lightgbm import LGBMClassifier, LGBMRegressor
from time import time
from sklearn.metrics import roc_auc_score
from sklearn.linear_model import LogisticRegression
from catboost import CatBoostClassifier
import sys
os.system('git clone https://github.com/Ottpocket/Helper_Functions')
sys.path.append('/kaggle/working/Helper_Functions')
from Helper_Functions.__init__ import reduce_mem_usage, get_val_test_increments, get_preds


import wandb
HYPERPARAMS = dict( #Params
                    model = 'lgbm', #lgbm, catboost, logistic
                    tags = [TO_BE_REPLACED_IN_COPY], #declares the features for the model. DELETE is just a filter for WandB
                    TARGET = 'T_5day_2p',
                    test_start = '2018-01-01',
                    end_date = '2021-03-01',
                    train_months = 3,
                    intervals = 'year'
                    )
if HYPERPARAMS['model'] == 'lgbm': #tested and works
    model = LGBMClassifier(objective='binary')
elif HYPERPARAMS['model'] == 'catboost':
    model = CatBoostClassifier()
else:
    model =LogisticRegression(n_jobs=-1) #tested and works

df = pd.read_feather('/kaggle/input/create-stonk-data-from-daily-prices/stonk_df')

#Selecting the Features to be used
FEATURES = []
TARGET = HYPERPARAMS['TARGET']

if 'baseline' in HYPERPARAMS['tags']:
    FEATURES += ['open', 'high', 'low', 'close', 'volume']

if 'high_3' in HYPERPARAMS['tags']:
    FEATURES+= [ 'r_high_mean_3', 'r_high_var_3',
       'r_high_min_3', 'r_high_max_3']

if 'high_5' in HYPERPARAMS['tags']:
    FEATURES+= [ 'r_high_mean_5', 'r_high_var_5',
       'r_high_min_5', 'r_high_max_5']

FEATURES = list(set(FEATURES))



df['T_10day_10p'] = df['T_high_max_10'] >= 1.1 * df['close']
df['T_10day_5p'] = df['T_high_max_10'] >= 1.05 * df['close']
df['T_10day_2p'] = df['T_high_max_10'] >= 1.02 * df['close']

df['T_5day_10p'] = df['T_high_max_5'] >= 1.1 * df['close']
df['T_5day_5p'] = df['T_high_max_5'] >= 1.05 * df['close']
df['T_5day_2p'] = df['T_high_max_5'] >= 1.02 * df['close']
df['T_10day_closeratio'] = df.groupby('ticker', sort=False)['close'].shift(-10).reset_index(drop=True) / df['close']
df['T_5day_closeratio'] = df.groupby('ticker', sort=False)['close'].shift(-5).reset_index(drop=True) / df['close']

#Initializing WandB
os.system('wandb login 139a106845d441074259f3d8b48ab85719b377cf')

#See https://docs.wandb.com/library/init for more details
run = wandb.init(project='Week_2p', config=HYPERPARAMS, tags = HYPERPARAMS['tags'])
config = wandb.config

#model
start_ = time()
get_preds(stonks = df, test_start = HYPERPARAMS['test_start'],
          end_date = HYPERPARAMS['end_date'],
          train_months = HYPERPARAMS['train_months'],
          intervals = HYPERPARAMS['intervals'],
          model = model,
          FEATURES = FEATURES,
          TARGET = HYPERPARAMS['TARGET'])
print(f'Took {time() - start_ :.2f} seconds')

#Saving the predictions
df = df[df.day >= HYPERPARAMS['test_start']].reset_index(drop=True).copy()
df.to_feather('stonk_df')
df.sort_values(['day','preds'], ascending=[True, False], inplace = True)
#Expected return on a preds >=.8
df['return'] = np.nan
df.loc[df[TARGET], 'return'] = 2
df.loc[~df[TARGET], 'return'] = df.loc[~df[TARGET], 'T_10day_closeratio']
Expected_Return_5 = df.loc[(df['preds'] >= .8), 'return'].mean()
print(f'Expected Return with selling bad at 5 day close: {Expected_Return_5}')
wandb.run.summary["Expected_Return_5"] = Expected_Return_5

#days w/ >= 1 prediction greater than .8
perc = .8
df['ge_perc'] = df['preds'] >= perc
agg = df.groupby('day').agg({'ge_perc':'sum'})
Perc_Predict_Days = np.mean(agg['ge_perc'] > 0)
print(f'A prediction of .8 confidence made in {Perc_Predict_Days :.3f}% of days')
wandb.run.summary["Perc_Predict_Days"] = Perc_Predict_Days

#Correlation between prediction and TARGET
Correlation = df[[TARGET, 'preds']].corr().values[0,1]
print(f'Correlation: {Correlation :.3f}')
wandb.run.summary["Correlation"] = Correlation

# Accuracy of predictions at >=.8 confidence
Acc = df.loc[df.preds >=.8, [TARGET]].mean().values[0]
print(f'Accuracy of preds >=80%: {Acc :.3f}')
wandb.run.summary["Acc"] = Acc

#AUC
AUC = roc_auc_score(df[TARGET], df['preds'])
print(f'AUC: {AUC :.3f}')
wandb.run.summary["AUC"] = AUC

#ACC pf top 10 preds each day >=.8
df2 = df.groupby('day').head(10)
Top_10_ACC = df2.loc[df2.preds >=.8, TARGET].mean()
print(f'Top 10 Acc: {Top_10_ACC :.3f}')
wandb.run.summary["Top_10_ACC"] = Top_10_ACC

#Return of top 10 preds each day >=.8
Top_10_Return= df2.loc[df2.preds >=.8, 'return'].mean()
print(f'Top 10 Return: {Top_10_Return :.3f}')
wandb.run.summary["Top_10_Return"] = Top_10_Return
