numerator+ = rating[i,k] * rating[j,k]
    	denominator1+=math.pow(rating[i,k],2)
    	denominator2+=math.pow(rating[j,k],2)

    round(numerator/float(numpy.sqrt(denominator1*denominator2)),3)




def cos_similarities(user1,user2,product):
	numerator=0
	denominator=0
	denominator1=0
	denominator2=0   
	for c in k:
		
		numerator += rating[i, c] * rating[j, c]
		denominator1+=math.pow(rating[i,c],2)
		denominator2+=math.pow(rating[j,c],2)

	return round(numerator/float(sqrt(denominator1*denominator2)),3)

	




	for (i,j),k in sorted_cos_sim.items():
    	cos_sub[i,j]=k
    	for (x,y),z in cos_sub.items():
    		if(i == x) and (j==k):
    			cotinue
    		else if(i==x) or (i==y):
    			neighbors[i].append()

    		else if (j==x) or (j==y):

    			for (i,j),k in rating.items():
    	for x in k:
    		for (a,b),c in collections.OrderedDict(sorted(diff_products.items())).items():
    			if ((i!=a or i!=b) and (x!=a or x!=b)):
    				print(i)
    			else :
    				continue











    				if ((neighbor[i],neighbor[j]) in shared_products) or ((neighbor[j],neighbor[i]) in shared_products):
    							if (neighbor[i],neighbor[j]) in shared_products:
    						##print(shared_products[neighbor[i],neighbor[j]])

    								for k in shared_products[neighbor[i],neighbor[j]]:
    									if (k) in stack:
    										stack[k] = stack[k]+1
    									else:
    										stack[k]=1
    							else:
    								for k in shared_products[neighbor[j],neighbor[i]]:
    		
    									if (k)in stack:
    										stack[k] = stack[k]+1
    									else:
    										stack[k]=1
    										
    				
    					
    				
    print(stack)
    					