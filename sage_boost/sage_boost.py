# %%
from os import sep
import pandas as pd
import numpy as np
import xgboost as xgb
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, matthews_corrcoef
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import sys

def booster(x_name, y_name):
# %%
    X = pd.read_csv(x_name) # feature array
    X.head()


    # %%
    y = pd.read_csv(y_name) # target array
    y.head()

    # %%
    X.dtypes

    # %%
    y.dtypes

    # %%
    sum(y['Essentiality'])/len(y['Essentiality'])

    # %%
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, stratify=y)


    # %%
    sum(y_train['Essentiality'])/len(y_train['Essentiality'])

    # %%
    sum(y_test['Essentiality'])/len(y_test['Essentiality']) 

    # %%
    xgb_clf = xgb.XGBClassifier(objective='binary:logistic', use_label_encoder=False, seed=42,verbosity=0)

    xgb_clf.fit(X_train, y_train)

    predictions = xgb_clf.predict(X_test)
    c_matrix = confusion_matrix(y_test, predictions, labels=xgb_clf.classes_)
    disp = ConfusionMatrixDisplay(confusion_matrix=c_matrix,
                                display_labels=xgb_clf.classes_)
    disp.plot()
    plt.savefig(x_name + '_cmatrix.png')

    return  accuracy_score(y_test, predictions), balanced_accuracy_score(y_test, predictions), f1_score(y_test, predictions), matthews_corrcoef(y_test, predictions)


a,b_a,f1,mc = booster(sys.argv[1], sys.argv[2])
print(a,b_a,f1,mc, sep=',', end='\n')