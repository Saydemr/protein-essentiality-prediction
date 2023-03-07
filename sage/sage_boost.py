# %%
import os
import pandas as pd
import numpy as np
import xgboost as xgb
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import *
import sys

def booster(x_name, y_name):

    X = pd.read_csv(x_name)
    X.drop(columns=X.columns[0], axis=1, inplace=True)
    y = pd.read_csv(y_name)

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, stratify=y)


    xgb_clf = xgb.XGBClassifier(objective='binary:logistic', use_label_encoder=False, seed=519, verbosity=0)
    xgb_clf.fit(X_train, y_train)

    predictions = xgb_clf.predict(X_test)

    return accuracy_score(y_test, predictions), f1_score(y_test, predictions), roc_auc_score(y_test, predictions), precision_score(y_test, predictions), recall_score(y_test, predictions)

if os.path.isfile(sys.argv[1]):
    a,f1,roc,p,rec = booster(sys.argv[1], sys.argv[2])
    print(a,f1,roc,p,rec, sep=',', end='\n')
