# %%
import pandas as pd
import numpy as np
import xgboost as xgb
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, balanced_accuracy_score, roc_auc_score, make_scorer
from sklearn.model_selection import RandomizedSearchCV,  GridSearchCV
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import plot_confusion_matrix
import sys
# %%
emb_csv = sys.argv[1]
essential_csv = sys.argv[2]
X = pd.read_csv(emb_csv) # feature array
X.head()


# %%
y = pd.read_csv(essential_csv) # target array
y.head()

# %%
X.dtypes

# %%
y.dtypes

# %%
print(sum(y['Essentiality'])/len(y['Essentiality'])) # to see the percentage of the essential genes in y.

# %%
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, stratify=y)
# test_size = 0.25, train_size = 0.75

# %%
print(sum(y_train['Essentiality'])/len(y_train['Essentiality'])) # check to see if the percentage of essential genes in training set is the same with y. 

# %%
print(sum(y_test['Essentiality'])/len(y_test['Essentiality'])) # check to see if the percentage of essential genes in testing set is the same with y. 

# %%
# plot_confusion_matrix(clf_xgb,
#                      X_test,
#                      y_test)
xgb_clf = xgb.XGBClassifier(objective='binary:logistic', use_label_encoder=False, seed=42)

xgb_clf.fit(X_train, y_train)

predictions = xgb_clf.predict(X_test)
print("Accuracy: ", accuracy_score(y_test, predictions))
print(balanced_accuracy_score(y_test, predictions))

c_matrix = confusion_matrix(y_test, predictions, labels=xgb_clf.classes_)
disp = ConfusionMatrixDisplay(confusion_matrix=c_matrix,
                              display_labels=xgb_clf.classes_)
disp.plot()
plt.savefig(emb_csv + '_cmatrix.png')
#plt.show()

# %% [markdown]
# ## Hyperparameter Optimization (WIP)

# %% [markdown]
# ## GridSearchCV()

# %%
#GridSearchCV()

## Round 1
    # param_grid = {
    #     'max_depth': [3,4,5], # possible tree levels
    #     'learning_rate': [0.1, 0.01, 0.05],
    #     'gamma': [0, 0.25, 1.0],
    #     'reg_lambda': [0, 1.0, 10.0],
    #     'scale_pos_weight': [1, 3, 5]
    # }

## Results of Round 1
    # XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,
    #               colsample_bynode=1, colsample_bytree=0.5,
    #               enable_categorical=False, gamma=1.0, gpu_id=-1,
    #               importance_type=None, interaction_constraints='',
    #               learning_rate=0.1, max_delta_step=0, max_depth=5,
    #               min_child_weight=1, missing=np.nan, monotone_constraints='()',
    #               n_estimators=100, n_jobs=12, num_parallel_tree=1,
    #               predictor='auto', random_state=42, reg_alpha=0, reg_lambda=10.0,
    #               scale_pos_weight=1, seed=42, subsample=0.9, tree_method='exact',
    #               validate_parameters=1, verbosity=None)
    # {'gamma': 1.0, 'learning_rate': 0.1, 'max_depth': 5, 'reg_lambda': 10.0, 'scale_pos_weight': 1}

## Round 2
    # param_grid = {
    #     'max_depth': [5, 6, 7],
    #     'learning_rate': [0.2, 0.15, 0.1],
    #     'gamma': [1.0, 2.0, 3.0, 4.0],
    #     'reg_lambda': [10.0, 20.0, 100.0],
    #     'scale_pos_weight': [1]
    #}
    
## Results of Round 2
   # XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,
   #            colsample_bynode=1, colsample_bytree=0.5,
   #            enable_categorical=False, gamma=2.0, gpu_id=-1,
   #            importance_type=None, interaction_constraints='',
   #            learning_rate=0.15, max_delta_step=0, max_depth=7,
   #            min_child_weight=1, missing=np.nan, monotone_constraints='()',
   #            n_estimators=100, n_jobs=12, num_parallel_tree=1,
   #            predictor='auto', random_state=42, reg_alpha=0, reg_lambda=20.0,
   #            scale_pos_weight=1, seed=42, subsample=0.9, tree_method='exact',
   #            validate_parameters=1, verbosity=None)
   #  {'gamma': 2.0, 'learning_rate': 0.15, 'max_depth': 7, 'reg_lambda': 20.0, 'scale_pos_weight': 1}

## Round 3
# param_grid= {     
#      'learning_rate'    : [0.15] ,
#      'max_depth'        : [7, 10, 13],
#      'min_child_weight' : [1, 3, 5],
#      'gamma'            : [1.0],
#      'reg_lambda'       : [20.0, 40.0, 60.0],
#      'scale_pos_weight' : [1]
# }

## Results of Round 3
    # XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,
    #               colsample_bynode=1, colsample_bytree=0.5,
    #               enable_categorical=False, gamma=1.0, gpu_id=-1,
    #               importance_type=None, interaction_constraints='',
    #               learning_rate=0.15, max_delta_step=0, max_depth=7,
    #               min_child_weight=5, missing=np.nan, monotone_constraints='()',
    #               n_estimators=100, n_jobs=12, num_parallel_tree=1,
    #               predictor='auto', random_state=42, reg_alpha=0, reg_lambda=40.0,
    #               scale_pos_weight=1, seed=42, subsample=0.9, tree_method='exact',
    #               validate_parameters=1, verbosity=None)
    # {'gamma': 1.0, 'learning_rate': 0.15, 'max_depth': 7, 'min_child_weight': 5, 'reg_lambda': 40.0, 'scale_pos_weight': 1}
    
##Round 4

# param_grid = {
#          'max_depth': [7, 9, 11, 13, 15],
#          'learning_rate': [0.15],
#          'gamma': [2.0],
#          'reg_lambda': [20.0, 40.0, 60.0],
#          'scale_pos_weight': [1]
#     }

## Results of Round 4
    # XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,
    #               colsample_bynode=1, colsample_bytree=0.5,
    #               enable_categorical=False, gamma=2.0, gpu_id=-1,
    #               importance_type=None, interaction_constraints='',
    #               learning_rate=0.15, max_delta_step=0, max_depth=7,
    #               min_child_weight=1, missing=np.nan, monotone_constraints='()',
    #               n_estimators=100, n_jobs=12, num_parallel_tree=1,
    #               predictor='auto', random_state=42, reg_alpha=0, reg_lambda=20.0,
    #               scale_pos_weight=1, seed=42, subsample=0.9, tree_method='exact',
    #               validate_parameters=1, verbosity=None)
    # {'gamma': 2.0, 'learning_rate': 0.15, 'max_depth': 7, 'reg_lambda': 20.0, 'scale_pos_weight': 1}
    
## Round 5
'''
param_grid = {
         'max_depth': [5, 6, 7],
         'learning_rate': [0.2, 0.15, 0.1],
         'min_child_weight' : [1, 3, 5],
         'gamma': [1.0, 2.0, 3.0, 4.0],
         'reg_lambda': [10.0, 20.0, 100.0],
         'scale_pos_weight': [1]
    }

## Results of Round 5
    # XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,
    #              colsample_bynode=1, colsample_bytree=0.5,
    #              enable_categorical=False, gamma=3.0, gpu_id=-1,
    #              importance_type=None, interaction_constraints='',
    #              learning_rate=0.2, max_delta_step=0, max_depth=6,
    #              min_child_weight=3, missing=np.nan, monotone_constraints='()',
    #              n_estimators=100, n_jobs=12, num_parallel_tree=1,
    #              predictor='auto', random_state=42, reg_alpha=0, reg_lambda=10.0,
    #              scale_pos_weight=1, seed=42, subsample=0.9, tree_method='exact',
    #               validate_parameters=1, verbosity=None)
    #{'gamma': 3.0, 'learning_rate': 0.2, 'max_depth': 6, 'min_child_weight': 3, 'reg_lambda': 10.0, 'scale_pos_weight': 1}


## when working with imbalanced data:
## balance the positive and negative weights with scale_pos_weight
## use AUC for evaluation

## to prevent overfitting and to speed up the process, 
## set subsample = 0.9,
## set colsample_bytree = 0.5 so that a random subset (50%) of columns are used
## cv = 3, three-fold cross-validation

optimal_parameters = GridSearchCV(estimator = xgb.XGBClassifier(objective='binary:logistic',
                                                              seed=42,
                                                              subsample=0.9,
                                                              colsample_bytree=0.5
                                                               ),
                                 param_grid = param_grid,
                                 scoring = 'roc_auc',
                                 verbose = 2,
                                 n_jobs = 10,
                                 cv = 4)

optimal_parameters.fit(X_train,
                       y_train,
                       early_stopping_rounds=10,
                       eval_metric='auc',
                       eval_set=[(X_test, y_test)],
                       verbose=True)


# classifier=xgb.XGBClassifier()
# random_search = RandomizedSearchCV(classifier, param_distributions=param_grid, n_iter=5, scoring='roc_auc', n_jobs=-1, cv=5, verbose=3)


# random_search.fit(X_train,y_train)

print(optimal_parameters.best_estimator_)
print(optimal_parameters.best_params_)

# %%
# With GridSearchCV
# Round 3 :{'gamma': 1.0, 'learning_rate': 0.1, 'max_depth': 5, 'reg_lambda': 10.0, 'scale_pos_weight': 1} -> 0.7999746295572515
          # -> 0.7970581714539092
# Round 4: {'gamma': 2.0, 'learning_rate': 0.15, 'max_depth': 7, 'reg_lambda': 20.0, 'scale_pos_weight': 1} -> 0.790582994489357
           # -> 0.790582994489357
    
# Round 5: {'gamma': 3.0, 'learning_rate': 0.2, 'max_depth': 6, 'min_child_weight': 3, 'reg_lambda': 10.0, 'scale_pos_weight': 1} -> 0.8012854357659245
           # Accuracy:  0.926006528835691
           # Balanced Accuracy:  0.8032122180395276
    
clf_grid = xgb.XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,
                  colsample_bynode=1, colsample_bytree=0.5,
                  enable_categorical=False, gamma=3.0, gpu_id=-1,
                  importance_type=None, interaction_constraints='',
                  learning_rate=0.2, max_delta_step=0, max_depth=6,
                  min_child_weight=3, missing=np.nan, monotone_constraints='()',
                  n_estimators=100, n_jobs=12, num_parallel_tree=1,
                  predictor='auto', random_state=42, reg_alpha=0, reg_lambda=10.0,
                  scale_pos_weight=1, seed=42, subsample=0.9, tree_method='exact',
                  validate_parameters=1, verbosity=None)

# y_train.values.ravel()
clf_grid.fit(X_train, 
            y_train,
            verbose=True,
            early_stopping_rounds=10,
            eval_metric='aucpr',
            eval_set=[(X_test, y_test)])

# %%
# with GridSearchCV, 0.7999746295572515 for
# {'gamma': 1.0, 'learning_rate': 0.1, 'max_depth': 5, 'reg_lambda': 10.0, 'scale_pos_weight': 1}
predictions = clf_grid.predict(X_test)
print("Accuracy: ", accuracy_score(y_test, predictions))
print("Balanced Accuracy: ",balanced_accuracy_score(y_test, predictions))

c_matrix = confusion_matrix(y_test, predictions, labels=clf_grid.classes_)
disp = ConfusionMatrixDisplay(confusion_matrix=c_matrix,
                              display_labels=clf_grid.classes_)
disp.plot()
#plt.show()
plt.savefig(emb_csv + '_optimized1.png')

# %% [markdown]
# ## RandomizedSearchCV()

# %%
#RandomizedSearchCV()

#Round 1
# param_grid = {
#     'max_depth': [3,4,5], # possible tree levels
#     'learning_rate': [0.1, 0.01, 0.05],
#     'gamma': [0, 0.25, 1.0],
#     'reg_lambda': [0, 1.0, 10.0],
#     'scale_pos_weight': [1, 3, 5]
# }

# XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,
#               colsample_bynode=1, colsample_bytree=1, enable_categorical=False,
#               gamma=0.25, gpu_id=-1, importance_type=None,
#               interaction_constraints='', learning_rate=0.1, max_delta_step=0,
#               max_depth=4, min_child_weight=1, missing=np.nan,
#               monotone_constraints='()', n_estimators=100, n_jobs=12,
#               num_parallel_tree=1, predictor='auto', random_state=0,
#               reg_alpha=0, reg_lambda=1.0, scale_pos_weight=5, subsample=1,
#               tree_method='exact', validate_parameters=1, verbosity=None)
# {'scale_pos_weight': 5, 'reg_lambda': 1.0, 'max_depth': 4, 'learning_rate': 0.1, 'gamma': 0.25}

## Round 2
# param_grid = {
#     'max_depth': [4],
#     'learning_rate': [0.2, 0.05, 0.1],
#     'gamma': [0.25],
#     'reg_lambda': [1.0],
#     'scale_pos_weight': [5, 6, 7]
#} 

## Round 3
#param_grid = {
#         'max_depth': [5, 6, 7],
#         'learning_rate': [0.1, 0.01, 0.05],
#         'min_child_weight' : [1, 3, 5],
#         'gamma': [1.0, 2.0, 3.0, 4.0],
#         'reg_lambda': [10.0, 20.0, 100.0],
#         'scale_pos_weight': [1, 3, 5]
#    }

## Results of Round 3
#XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,
#              colsample_bynode=1, colsample_bytree=1, enable_categorical=False,
#              gamma=2.0, gpu_id=-1, importance_type=None,
#              interaction_constraints='', learning_rate=0.1, max_delta_step=0,
#              max_depth=5, min_child_weight=1, missing=np.nan,
#              monotone_constraints='()', n_estimators=100, n_jobs=12,
#              num_parallel_tree=1, predictor='auto', random_state=0,
#              reg_alpha=0, reg_lambda=20.0, scale_pos_weight=3, subsample=1,
#              tree_method='exact', validate_parameters=1, verbosity=None)

#{'scale_pos_weight': 3, 'reg_lambda': 20.0, 'min_child_weight': 1, 'max_depth': 5, 'learning_rate': 0.1, 'gamma': 2.0}

## Round 4

param_grid = {
         'max_depth': [3, 4, 5],
         'learning_rate': [0.2, 0.15, 0.1],
         'min_child_weight' : [1, 3, 5],
         'gamma': [1.0, 2.0, 3.0, 4.0],
         'reg_lambda': [0, 1.0, 5.0, 10.0, 20.0, 100.0],
         'scale_pos_weight': [1, 3, 5]
    }

## Round 4 Results
# XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,
#              colsample_bynode=1, colsample_bytree=1, enable_categorical=False,
#              gamma=3.0, gpu_id=-1, importance_type=None,
#              interaction_constraints='', learning_rate=0.2, max_delta_step=0,
#              max_depth=4, min_child_weight=1, missing=np.nan,
#              monotone_constraints='()', n_estimators=100, n_jobs=12,
#              num_parallel_tree=1, predictor='auto', random_state=0,
#              reg_alpha=0, reg_lambda=100.0, scale_pos_weight=3, subsample=1,
#              tree_method='exact', validate_parameters=1, verbosity=None)
#{'scale_pos_weight': 3, 'reg_lambda': 100.0, 'min_child_weight': 1, 'max_depth': 4, 'learning_rate': 0.2, 'gamma': 3.0}

## Round 5
#param_grid = {
#         'max_depth': [3, 4, 5],
#         'learning_rate': [0.2, 0.15, 0.1],
#         'min_child_weight' : [1, 3, 5],
#         'gamma': [1.0, 2.0, 3.0, 4.0, 5.0, 10.0, 20.0],
#         'reg_lambda': [10.0, 20.0, 100.0],
#         'scale_pos_weight': [1, 3, 5]
#    }

classifier=xgb.XGBClassifier()

#random_search = RandomizedSearchCV(classifier, pram_distributions=param_grid,n_iter=5,scoring='roc_auc',n_jobs=-1,cv=5,verbose=3)
random_search = RandomizedSearchCV(classifier, param_distributions=param_grid, n_iter=5, scoring='roc_auc', n_jobs=-1, cv = 5, verbose = 3)

random_search.fit(X_train,y_train)

print(random_search.best_estimator_)
print(random_search.best_params_)

# Fitting 5 folds for each of 5 candidates, totalling 25 fits
# XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,
#               colsample_bynode=1, colsample_bytree=1, enable_categorical=False,
#               gamma=0.25, gpu_id=-1, importance_type=None,
#               interaction_constraints='', learning_rate=0.05, max_delta_step=0,
#               max_depth=4, min_child_weight=1, missing=np.nan,
#               monotone_constraints='()', n_estimators=100, n_jobs=12,
#               num_parallel_tree=1, predictor='auto', random_state=0,
#               reg_alpha=0, reg_lambda=1.0, scale_pos_weight=3, subsample=1,
#               tree_method='exact', validate_parameters=1, verbosity=None)
# {'scale_pos_weight': 3, 'reg_lambda': 1.0, 'max_depth': 4, 'learning_rate': 0.05, 'gamma': 0.25}

# %%
# With RandomizedSearchCV
# {'scale_pos_weight': 3, 'reg_lambda': 0, 'max_depth': 4, 'learning_rate': 0.1, 'gamma': 0.25}

# Round 4 -> Accuracy:  0.9015233949945594
         #-> Balanced Accuracy:  0.8383411387443231
    
clf_rnd = xgb.XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,
              colsample_bynode=1, colsample_bytree=1, enable_categorical=False,
              gamma=3.0, gpu_id=-1, importance_type=None,
              interaction_constraints='', learning_rate=0.2, max_delta_step=0,
              max_depth=4, min_child_weight=1, missing=np.nan,
              monotone_constraints='()', n_estimators=100, n_jobs=12,
              num_parallel_tree=1, predictor='auto', random_state=0,
              reg_alpha=0, reg_lambda=100.0, scale_pos_weight=3, subsample=1,
              tree_method='exact', validate_parameters=1, verbosity=None)

clf_rnd.fit(X_train, 
            y_train,
            verbose=True,
            early_stopping_rounds=10,
            eval_metric='aucpr',
            eval_set=[(X_test, y_test)])

# %%
# With RandomizedSearchCV, 0.8366566327708409 for
# {'scale_pos_weight': 3, 'reg_lambda': 0, 'max_depth': 4, 'learning_rate': 0.1, 'gamma': 0.25}

predictions = clf_rnd.predict(X_test)
print("Accuracy: ", accuracy_score(y_test, predictions))
print("Balanced Accuracy: ", balanced_accuracy_score(y_test, predictions))


c_matrix = confusion_matrix(y_test, predictions, labels=clf_rnd.classes_)
disp = ConfusionMatrixDisplay(confusion_matrix=c_matrix,
                              display_labels=clf_rnd.classes_)
disp.plot()
#plt.show()
plt.savefig(emb_csv + 'optimized2.png')'''