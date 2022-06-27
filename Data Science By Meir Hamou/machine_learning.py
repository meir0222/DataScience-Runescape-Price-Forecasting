#%%
import os
from pyexpat import model                       
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from data_cleaning import *
from EDA_Visualization import*
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (10, 6)
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from sklearn import linear_model,ensemble

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import accuracy_score, r2_score



df=pd.read_csv("output.csv")
df = clean_data(df)
df

def split_model(df):
    df_copy=df.copy()
    y=df_copy[["Price"]]
    X=df_copy.drop(["Price","Quest","Value","Untradeable"],axis=1)
    return train_test_split(X,y,random_state=0)

def dec_tree(df):
    dec_tree_model=DecisionTreeRegressor(max_depth=7)
    X_train,X_test,y_train,y_test = split_model(df) #split train and test
    dec_tree_model.fit(X_train,np.ravel(y_train)) #train
    dec_tree_model=dec_tree_model
    y_pred = dec_tree_model.predict(X_test)
    return r2_score(y_test,y_pred)

def random_forest(df):
    X_train, X_test, y_train, y_test = split_model(df)
    random_forest_model = ensemble.RandomForestRegressor(n_estimators=100)
    random_forest_model.fit(X_train, np.ravel(y_train)) #train
    y_pred = random_forest_model.predict(X_test)

    return r2_score(y_test,y_pred)

def gb(df):
    X_train, X_test, y_train, y_test = split_model(df)

    model = ensemble.GradientBoostingRegressor(n_estimators=40)
    model.fit(X_train, np.ravel(y_train)) #train
    model.score(X_test, y_test)

    y_pred = model.predict(X_test)
        
    #print(model.feature_importances_)
    return r2_score(y_test,y_pred)

def linear(df):
    X_train, X_test, y_train, y_test = split_model(df)
        
    model = linear_model.LinearRegression()
    model.fit(X_train, np.ravel(y_train)) #train
    model.score(X_test, y_test)
        
    y_pred = model.predict(X_test)

    #print(model.feature_importances_)
    return r2_score(y_test,y_pred)

print("dec_tree:",dec_tree(df))
print("random forest:",random_forest(df))
print("gb:",gb(df))
print("linear regression:",linear(df))


    



        





#%%