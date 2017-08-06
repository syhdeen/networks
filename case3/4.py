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
cos_sim = {}
shared_products=defaultdict(list)
diff_products=defaultdict(list)
neighbors =defaultdict(list)
predictions = {}
predictions_for_recommendation = {}

def initiation(filename):
        # Create a place holder dictionaries for ratings, products by user and rating by user 
        # retrive the shared products between users

    with open(filename, 'r') as file:
        data = file.readlines()

    for line in data:
        word = line.split(' ')
        for x in range(len(word)):
        	word[x] = int(word[x])

        rating[word[0], word[1]] = word[3]
        ratings_by_user[word[0]].append(word[3])
        products_by_user[word[0]].append(word[1])



    #shared products

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


    
def similarity_matrix(first_user,second_user,shared_products):
	numerator=0
	denominator=0
	denominator1=0
	denominator2=0
	for product in shared_products:
		numerator += rating[first_user, product] * rating[second_user, product]
		denominator1+=math.pow(rating[first_user,product],2)
		denominator2+=math.pow(rating[second_user,product],2)
		cos_sim_u=round(numerator/float(sqrt(denominator1*denominator2)),3)
		cos_sim[first_user,second_user]=cos_sim_u

def sim_neighbors():

    for (first_user,second_user),products in shared_products.items():
    	

    	if(len(products)<1):
    		cos_sim_u=0

    	else:
    		similarity_matrix(first_user,second_user,products)
    		if cos_sim[first_user,second_user]>.5:
       			neighbors[first_user].append(second_user)
       			neighbors[second_user].append(first_user)
    print(cos_sim)


def prediction():

    for user,neighbor in neighbors.items():
    	mean_user_rating=statistics.mean(ratings_by_user[user])

    	if len(neighbor) >0:	
    		for i in range(0,len(neighbor)-1):
    			numerator=0
    			denominator=0
    			

    			stack={}
    			for product in products_by_user[neighbor[i]]:
    				try:
    					denominator = cos_sim[neighbor[i],user]
    				except KeyError :
    					denominator = cos_sim[user,neighbor[i]]
   				 	 
   				 	for j in range(i+1,len(neighbor)):
   				 		if (product in products_by_user[neighbor[j]]):
   				 			try:
   				 				neighbor_sim=cos_sim[neighbor[j],user]
   				 			except KeyError :
   				 				neighbor_sim=cos_sim[user,neighbor[j]]

   				 			numerator = numerator + (neighbor_sim * (rating[neighbor[j],product] - statistics.mean(ratings_by_user[neighbor[i]])))
   				 			denominator =denominator + neighbor_sim
   				 	predicted_rating=mean_user_rating+(numerator/denominator)
   				 	if (product not in products_by_user[user]):
   				 		predictions_for_recommendation[user,product]= predicted_rating
   				 	else:
   				 		predictions[user,product]= predicted_rating


    print(predictions)
    


	
def recommend(user,num_of_recommendation):
  print('Recommend',num_of_recommendation,'products for user',user)
  sim_neighbors()
  prediction()
  #select top rating in predictions_for_recommendation








def main():
  initiation('epinions/rating.txt')
  recommend(1,5)

main()