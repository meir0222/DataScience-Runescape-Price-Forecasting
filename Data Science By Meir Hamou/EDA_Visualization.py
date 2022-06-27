# %%                       
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt      
import seaborn as sns
from collections import Counter
from data_cleaning import * 


df=pd.read_csv("output.csv")
clean_data(df)

print("Number of rows in data =",df.shape[0])
print("Number of columns in data =",df.shape[1])
print("\n")
print("**Sample data:**")


#Calculating number of items under each label
categories = list(df.columns.values)
categories = categories[12:]
print(categories)

# Calculating number of items in each category
counts = []
for category in categories:
    counts.append((category, df[category].sum()))
df_stats = pd.DataFrame(counts, columns=['category', 'number of comments'])
df_stats

sns.set(font_scale = 2)
plt.figure(figsize=(15,8))
ax= sns.barplot(categories, df.iloc[:,12:].sum().values)
plt.title("Items in each category", fontsize=24)
plt.ylabel('Number of items', fontsize=18)
plt.xlabel('Item Type ', fontsize=18)

#adding the text labels
rects = ax.patches
labels = df.iloc[:,12:].sum().values
for rect, label in zip(rects, labels):
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width()/2, height + 5, label, ha='center', va='bottom', fontsize=18)

plt.show()

# plt.figure(figsize=(20,10))
# c= df.corr()
# sns.heatmap(c,annot=True)
# c
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

    plt.savefig('corr_matrix.png',bbox_inches="tight")
draw_corr_plot(df)




# #Calculating number of comments having multiple labels

# rowSums = df.iloc[:,12:].sum(axis=1)
# multiLabel_counts = rowSums.value_counts()
# multiLabel_counts = multiLabel_counts.iloc[1:]

# sns.set(font_scale = 2)
# plt.figure(figsize=(15,8))

# ax = sns.barplot(multiLabel_counts.index, multiLabel_counts.values)

# plt.title("items having multiple labels ")
# plt.ylabel('Number of items', fontsize=18)
# plt.xlabel('Number of labels', fontsize=18)

# #adding the text labels
# rects = ax.patches
# labels = multiLabel_counts.values
# for rect, label in zip(rects, labels):
#     height = rect.get_height()
#     ax.text(rect.get_x() + rect.get_width()/2, height + 5, label, ha='center', va='bottom')

# plt.show()







# cols=["Combat","Skilling","Food","Untradeable","Quest"]
# df_cols=df.columns
#df[cols].hist()
#plot_high_correlated_scatters(df)









#%%