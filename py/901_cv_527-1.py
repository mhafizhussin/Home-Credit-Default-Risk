#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 27 22:23:57 2018

@author: Kazuki
"""

from glob import glob
from tqdm import tqdm
import pandas as pd
import sys
sys.path.append('/home/kazuki_onodera/Python')
import lgbmextension as ex
import lightgbm as lgb
import utils
utils.start(__file__)
#==============================================================================

SEED = 71

folsers = sorted(glob('../data/*_train'))

X = pd.concat([
#               utils.read_pickles('../data/101_train'), 
#               utils.read_pickles('../data/102_train'), 
#               utils.read_pickles('../data/103_train'), 
#               utils.read_pickles('../data/104_train')
        utils.read_pickles(f) for f in (folsers)
               ], axis=1)
y = utils.read_pickles('../data/label').TARGET

print(f'X.shape {X.shape}')

param = {
         'objective': 'binary',
         'metric': 'auc',
         'learning_rate': 0.05,
         'max_depth': -1,
         'num_leaves': 127,
         'max_bin': 100,
         'colsample_bytree': 0.5,
         'subsample': 0.5,
         'nthread': 64,
         'bagging_freq': 1,
         
         'seed': SEED
         }


categorical_feature = ['NAME_CONTRACT_TYPE',
                     'CODE_GENDER',
                     'FLAG_OWN_CAR',
                     'FLAG_OWN_REALTY',
                     'NAME_TYPE_SUITE',
                     'NAME_INCOME_TYPE',
                     'NAME_EDUCATION_TYPE',
                     'NAME_FAMILY_STATUS',
                     'NAME_HOUSING_TYPE',
                     'OCCUPATION_TYPE',
                     'WEEKDAY_APPR_PROCESS_START',
                     'ORGANIZATION_TYPE',
                     'FONDKAPREMONT_MODE',
                     'HOUSETYPE_MODE',
                     'WALLSMATERIAL_MODE',
                     'EMERGENCYSTATE_MODE']

dtrain = lgb.Dataset(X, y, categorical_feature=categorical_feature)

ret = lgb.cv(param, dtrain, 9999, nfold=5,
             early_stopping_rounds=50, verbose_eval=None,
             seed=SEED)
print(f"CV auc-mean {ret['auc-mean'][-1]}")


yhat, imp, ret = ex.stacking(X, y, param, 9999, esr=50, seed=SEED,
                             categorical_feature=categorical_feature)


imp.to_csv(f'LOG/imp_{__file__}.csv', index=False)


#==============================================================================
utils.end(__file__)


