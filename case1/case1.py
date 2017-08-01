import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
import random




Facebook = "facebook/facebook_combined.txt"
WikiVote = "wiki-vote/Wiki-Vote.txt"


def network_real_world_analysis(graph,network_name):
	print("\n \n ***************",network_name, " analysis ******************\n\n")
	num_nodes = graph.number_of_nodes()
	print("Number of nodes in", network_name, " = ", num_nodes)
	r = nx.degree_assortativity_coefficient(graph)
	print("Degree Assortativity Coefficient  of ", network_name, " = ", r)
	connected_components= nx.number_strongly_connected_components(graph)
	print("Number of strongly connected components  in ", network_name, " = ", connected_components)
	degree_correlations = nx.degree_pearson_correlation_coefficient(graph)
	print("Degree Correlations of ", network_name, " = ", degree_correlations)
	

	neighbor_degree = nx.average_neighbor_degree(graph)
	#print("Average neighbor degree  = ", neighbor_degree)



def largest_component(graph):
	largest = max(nx.strongly_connected_components(graph), key=len)
	k = graph.subgraph(largest)
	scc=[(len(c),c) for c in sorted( nx.strongly_connected_components(graph), key=len, reverse=True)][0][1]
	return k


def in_degree_loglog(graph,network_name):
	in_degrees = graph.in_degree() # dictionary node:degree
	in_values = sorted(set(in_degrees.values()))
	in_hist = [list(in_degrees.values()).count(x) for x in in_values]

	fig2 = plt.figure()
	plt.loglog(in_values, in_hist, 'ro-') # in-degree
	plt.xlabel('Degree')
	plt.ylabel('Number of nodes')
	title = "%s network log log plot \n PLease press Enter To Continue" % (network_name)

	plt.title(title)
	fig2.show()
	plt.waitforbuttonpress()
	plt.close()


def Kroneker_network(num_nodes, initiator=np.random.randint(2, size=(2, 2))):
	k = initiator
	while len(k) < num_nodes:
		k=np.kron(k,k)
	nodes = np.random.choice(len(k),num_nodes,replace=False)
	nodes=sorted(nodes)
	kroneker = k[nodes,:][:,nodes]
	G = nx.to_networkx_graph(kroneker,create_using=nx.DiGraph())
	return G



def Price_Model(num_nodes):
	dendogram={}
	citations=0 
	a = 1
	for i in range(num_nodes):
		dendogram[i] = []  
		for node in dendogram.values():
			qi=len(node)
			current_num_nodes=i
			pref_attach_prob =  (qi + a) / (current_num_nodes  +(citations+a ))
			if(random.random() <= pref_attach_prob):
				node.append(i)
				citations += 1

	G = nx.DiGraph(dendogram)
	return G



def plot_graph(G,pos,fignum,network_name):


    label = dict()
    labelpos=dict()
    

    for i in range(G.number_of_nodes()):
        label[i] = i
        labelpos[i] = pos[i][0]+0.02, pos[i][1]+0.02



    fig=plt.figure(fignum,figsize=(10,10))
    title = "%s network \n PLease press Enter To Continue" % (network_name)
    fig.clf()

    nx.draw_networkx_nodes(G,
                            pos,
                            node_size=40,
                            hold=False,
                        )

    nx.draw_networkx_edges(G,pos, hold=True, arrows=True)
    nx.draw_networkx_labels(G,
                            labelpos,
                            
                            font_size=10,
                            hold=True,
                        )

    plt.title(title)

    fig.show()
    plt.waitforbuttonpress(timeout=-1)
    plt.close()









def network_analysis(G,network_name):

	network_real_world_analysis(G,network_name)
	

	A = nx.adjacency_matrix(G)
	Gp = nx.to_networkx_graph(A, create_using=nx.DiGraph())
	num_nodes = G.number_of_nodes()
	x = [random.random() for i in range(num_nodes)]
	y = [random.random() for i in range(num_nodes)]
	x = np.array(x)
	y = np.array(y)
	pos = dict()
	for i in range(0,num_nodes):
		pos[i] = x[i],y[i]

	plot_graph(Gp, pos, 1, network_name)




	LC=largest_component(G)
	LCA = nx.adjacency_matrix(LC)
	LCp = nx.to_networkx_graph(LCA, create_using=nx.DiGraph())
	LC_num_nodes = LC.number_of_nodes()
	x = [random.random() for i in range(num_nodes)]
	y = [random.random() for i in range(num_nodes)]
	x = np.array(x)
	y = np.array(y)
	pos = dict()
	for i in range(0,LC_num_nodes):
		pos[i] = x[i],y[i]
	LC_name=network_name + " largest component"


	plot_graph(LCp,pos,2, LC_name)


	in_degree_loglog(G, network_name)


def main():
	
	initiator =  np.matrix('1 1; 1 0')

	Kroneker_G = Kroneker_network(100,initiator)
	kron="Kroneker"
	network_analysis(Kroneker_G, kron)


	Price_G = Price_Model(1000)
	network_analysis(Price_G, "Price")



	G = nx.read_edgelist(WikiVote,create_using=nx.DiGraph())
	wiki="Wiki_Vote"
	network_analysis(G, wiki)

main()

