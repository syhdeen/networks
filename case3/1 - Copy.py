import numpy as np
import pandas as pd
from sklearn import cross_validation as cv









header = ['userid', 'productid', 'categoryid', 'rating', 'helpfulness', 'timestamp']
data = pd.read_csv('epinions/rating.txt', delim_whitespace=True , names=header)



num_users = data.userid.unique().shape[0]
num_items = data.productid.unique().shape[0]
print ('Number of users = ' + str(num_users) + ' | Number of movies = ' + str(num_items))

def getScore(history, similarities):
   return sum(history*similarities)/sum(similarities)

data_sims = pd.DataFrame(index=data.index,columns=data.columns)
data_sims.ix[:,:1] = data.ix[:,:1]


data_germany = data.drop('timestamp', 1)
data_germany = data_germany.drop('helpfulness', 1)
data_germany = data_germany.drop('helpfulness', 1)
print(data.userid.unique())


data_ibs = pd.DataFrame(index=data_germany.index,columns=data_germany.columns)

for i in range(0,len(data_ibs.columns)) :
    # Loop through the columns for each column
      # Fill in placeholder with cosine similarities
      data_ibs.ix[i,3] = 1-cosine(data_germany.ix[:,i],data_germany.ix[:,j])

      