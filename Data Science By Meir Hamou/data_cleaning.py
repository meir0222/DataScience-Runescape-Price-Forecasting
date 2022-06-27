# %%
from multiprocessing.sharedctypes import Value                     
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt  
import seaborn as sns
import sys
import warnings
if not sys.warnoptions:
    warnings.simplefilter("ignore")


df=pd.read_csv("output.csv")

def draw_corr_plot(df):
    corr_mat = df.corr()
    columns = df.columns

    f, ax = plt.subplots(figsize=(25,25))

    heatmap = sns.heatmap(corr_mat,square=True, linewidths=.5, cmap='coolwarm',cbar_kws =
    {'shrink': .4,'ticks' : [-1, -.5, 0, 0.5, 1]},
    vmin = -1,
    vmax = 1,
    annot = True,
    annot_kws = {"size": 22})
        
    ax.set_yticklabels(corr_mat.columns, rotation = 0, size=23)
    ax.set_xticklabels(corr_mat.columns, size=23)
    ax.set_title('Correlation Matrix', fontsize=32)
    sns.set_style({'xtick.bottom':True},{'ytick.left':True})

    plt.savefig('corr_matrix_before_clean.png',bbox_inches="tight")

def remove_duplicates(df):
    df.drop_duplicates(keep='first',inplace=True) 

def remove_corrupt_rows(df):
    numOfCols=len(df.columns)
    df.dropna(axis=0, thresh=numOfCols, inplace=True)

def replace_missing_values(df):
    numeric_columns = df.select_dtypes(include=['number']).columns
    print(numeric_columns)
    df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].median())
    for col in df.columns:
        df[col] = df[col].fillna(df[col].mode()[0])
    return df

def stripString(df):
    df['Weight'] = df['Weight'].apply(lambda x: x.replace("kg",""))

def drop_columns(df):
    df.drop(labels=["Released","Options","Destory","Examine"],axis=1,inplace=True)
    # df.drop(labels=["Released"],axis=1,inplace=True)
def change_to_numeric(df):
    df['Members'] = df['Members'].apply(lambda x: 0 if x == 'No' else 1)
    df['Quest item'] = df['Quest item'].apply(lambda x: 0 if x == 'No' else 1)
    df['Tradeable'] = df['Tradeable'].apply(lambda x: 0 if x == 'No' else 1)
    df['Untradeable'] = df['Tradeable'].apply(lambda x: 0 if x == 1 else 1)
    df['Quest'] = df['Quest item'].apply(lambda x: 0 if x == 0 else 1)
    df['Equipable'] = df['Equipable'].apply(lambda x: 0 if x == 'No' else 1)
    df['Stackable'] = df['Stackable'].apply(lambda x: 0 if x == 'No' else 1)
    df['Price']=df['Price'].apply(lambda x: x.replace("(info)",""))
    df['Price'] = df['Price'].apply(lambda x: 0 if x == 'None' else x)
    df['Buy limit'] = df['Buy limit'].apply(lambda x: 0 if x == 'None' else x)
    df['Daily volume'] = df['Daily volume'].apply(lambda x: 0 if x == 'None' else x)
    stripString(df)  

def outlier_detection_iqr(df):
    numeric_columns = df.select_dtypes(include=['number']).columns
    for col in df[numeric_columns]:
        Q1= np.percentile(df[col], 25)
        Q3= np.percentile(df[col], 75)
        IQR=Q3-Q1
        IQR_range = 1.5 * IQR
        df[col][(df[col] < Q1-IQR_range) | (df[col] > Q3 + IQR_range)]=np.nan
    return df

def get_frequent_elements(df):
    col_names=df.columns
    for col in col_names[-5:]:
        series=pd.Series(data=df[col])
        freq=series.value_counts()
        print(freq)
    return freq[:5].sort_index()

def changeNoneToZero(df):
    for i in df.columns:
        for iz,j in enumerate(i):
            if j==None:
                df[i][iz]=0

def clean_data(df):
    remove_duplicates(df)
    remove_corrupt_rows(df)
    drop_columns(df)
    df = replace_missing_values(df)
    change_to_numeric(df)
    df["Value"] = df["Value"].astype(str).astype(float)
    df["High alch"] = df["High alch"].astype(str).astype(float)
    df["Low alch"] = df["Low alch"].astype(str).astype(float)
    df["Weight"] = df["Weight"].astype(str).astype(float)
    df["Price"] = df["Price"].astype(str).astype(float)
    df["Buy limit"] = df["Buy limit"].astype(str).astype(float)
    df["Daily volume"] = df["Daily volume"].astype(str).astype(float)
    return df

draw_corr_plot(df)
df = clean_data(df)
df


###############################outlier_detection_iqr(df)
#df[cols].hist()




# %%