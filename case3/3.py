import sys
import statistics
import math
import itertools
import time
import csv
from collections import defaultdict
from collections import Counter
from numpy import *
from numpy.linalg import norm
import collections

ratings_by_movie = defaultdict(list)
ratings_by_user = defaultdict(list)
products_by_user = defaultdict(list)
rating = {}
sorted_rating={}
mean_user_rating = {}
pearson_scores = {}
cos_sim = defaultdict(list)
shared_products=defaultdict(list)
diff_products=defaultdict(list)
neighbors =defaultdict(list)
predictions = {}
predictions_for_recommendation = {}

def populate():
    '''Populates all dictionaries used in the program from ratings.txt file'''

    with open('epinions/rating.txt', 'r') as f:
        data = f.readlines()

    for line in data:
        column = line.split(' ')
        for x in range(len(column)):
        	
        	column[x] = int(column[x])

        rating[column[0], column[1]] = column[3]

        # Create a place holder matrix for similarities, and fill in the user 

        ratings_by_user[column[0]].append(column[3])
        products_by_user[column[0]].append(column[1])




    comm={}
    sorted_rating = collections.OrderedDict(sorted(rating.items()))
    #print(sorted_rating)
    

    for (i,j),k in sorted_rating.items():
    	#print("**",i)
    	#print("**",j)
    	comm[i,j]=k

    	for (x,y),z in  comm.items():
    		if ((x != i) and j==y):
    			shared_products[i,x].append(j)


    

    		




    for (i,j),k in shared_products.items():
    	numerator=0
    	denominator=0
    	denominator1=0
    	denominator2=0

    	if(len(k)<1):
    		cos_sim_u=0

    	else:
    		for c in k:
    			numerator += rating[i, c] * rating[j, c]
    			denominator1+=math.pow(rating[i,c],2)
    			denominator2+=math.pow(rating[j,c],2)

    		cos_sim_u=round(numerator/float(sqrt(denominator1*denominator2)),3)
    		cos_sim[i,j].append(cos_sim_u)
    		if cos_sim_u>.5:
       			neighbors[i].append(j)
       			neighbors[j].append(i)


    for user,neighbor in neighbors.items():
    	print(neighbors[user])         
    	mean_user_rating=statistics.mean(ratings_by_user[user])
    	print(mean_user_rating)

    	if len(neighbor) >0:	
    		for i in range(0,len(neighbor)-1):
    			numerator=0
    			denominator=0
    			

    			stack={}
    			for product in products_by_user[neighbor[i]]:
   				 	for x in cos_sim[neighbor[i],user]:
   				 		neighbor_sim=x
   				 	denominator = neighbor_sim 
   				 	for j in range(i+1,len(neighbor)):
   				 		if (product in products_by_user[neighbor[j]]):
   				 			print(statistics.mean(ratings_by_user[neighbor[j]]))
   				 			print(rating[neighbor[j],product])
   				 			print(cos_sim[neighbor[j],user])
   				 			for x in cos_sim[neighbor[j],user]:
   				 				neighbor_sim=x

   				 			numerator = numerator + (neighbor_sim * (rating[neighbor[j],product] - statistics.mean(ratings_by_user[neighbor[i]])))
   				 			print(numerator)
   				 			denominator =denominator + neighbor_sim
   				 			print(denominator)
   				 	predicted_rating=mean_user_rating+(numerator/denominator)
   				 	if (product not in products_by_user[user]):
   				 		predictions_for_recommendation[user,product]= predicted_rating
   				 	else:
   				 		predictions[user,product]= predicted_rating


    print(predictions)
    failures=0
    squared_error=0
    for user,product in rating:
    	try:
    		
    		squared_error += ((predictions[user, product] ))
    	except KeyError:
    		failures += 1
    	
    RMSE = math.sqrt(squared_error/1)





    						




    			




    	

    	





    
    				



    	











    






    





        

    
populate()

print (cos_sim)
print("****************")
#print (rating)
print("****************")
print (shared_products)
print("****************")
print (neighbors)

print("****************")
#print (collections.OrderedDict(sorted(diff_products.items())))