import os
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import KFold, StratifiedKFold, cross_validate, RepeatedStratifiedKFold, RepeatedKFold
import sys

def booster(x_name, y_name):

    X = pd.read_csv(x_name)
    X.drop(columns=X.columns[0], axis=1, inplace=True)
    y = pd.read_csv(y_name)


    kfold = KFold(n_splits=5, shuffle=True, random_state=519)
    xgb_clf = xgb.XGBClassifier(objective='binary:logistic', use_label_encoder=False, seed=42, verbosity=0)
    scores = cross_validate(xgb_clf, X, y, cv=kfold, scoring=['accuracy','f1', 'roc_auc', 'precision', 'recall'] ,n_jobs=5)

    return np.average(scores['test_accuracy']), np.std(scores['test_accuracy']), np.average(scores['test_f1']), np.std(scores['test_f1']), np.average(scores['test_roc_auc']), np.std(scores['test_roc_auc']), np.average(scores['test_precision']), np.std(scores['test_precision']), np.average(scores['test_recall']), np.std(scores['test_recall'])

if os.path.isfile(sys.argv[1]):
    a, a_std, f1, f1_std, roc, roc_std, p, p_std, rec, rec_std = booster(sys.argv[1], sys.argv[2])
    print(a, a_std, f1, f1_std, roc, roc_std, p, p_std, rec, rec_std, sep=',', end='\n')
