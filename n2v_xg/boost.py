# %%
import os
from typing import NamedTuple
import pandas as pd
import numpy as np
from pandas.io.parsers import read_csv
import xgboost as xgb
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, balanced_accuracy_score, roc_auc_score, make_scorer, f1_score, matthews_corrcoef, precision_score, recall_score
from sklearn.model_selection import RandomizedSearchCV,  GridSearchCV
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import plot_confusion_matrix
import sys

# X = read_csv('./csv_imp/sc_ppi_emb_d64_e3_l120_w20_k20_p2.emb.csv')

# print(X.head())

# exit()
def booster(x_name, y_name):

    X = pd.read_csv(x_name) # feature array
    y = pd.read_csv(y_name) # target array
    X.drop(columns=['Protein_ID'], inplace=True)

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, stratify=y)

    xgb_clf = xgb.XGBClassifier(objective='binary:logistic', use_label_encoder=False, seed=42,verbosity=0)
    xgb_clf.fit(X_train, y_train)

    predictions = xgb_clf.predict(X_test)
 
    # c_matrix = confusion_matrix(y_test, predictions, labels=xgb_clf.classes_)
    # disp = ConfusionMatrixDisplay(confusion_matrix=c_matrix,
    #                             display_labels=xgb_clf.classes_)
    # disp.plot()
    # plt.savefig(x_name + '_cmatrix.png')

    return  accuracy_score(y_test, predictions), balanced_accuracy_score(y_test, predictions), f1_score(y_test, predictions), matthews_corrcoef(y_test, predictions), roc_auc_score(y_test, predictions), precision_score(y_test, predictions), recall_score(y_test, predictions)

if os.path.isfile(sys.argv[1]):
    a,b_a,f1,mc,roc,p,rec = booster(sys.argv[1], sys.argv[2])
    print(a,b_a,f1,mc,roc,p,rec, sep=',', end='\n')