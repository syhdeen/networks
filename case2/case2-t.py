#import cairocffi as cairo
from igraph import *
import time
import matplotlib.pyplot as plt


#better with karate_graph() as defined in networkx example.
#erdos renyi don't have true community structure



Facebook = "facebook/facebook_combined.txt"
WikiVote = "wiki-vote/Wiki-Vote.txt"

g = igraph.Graph.Read_Ncol(Facebook, directed=False)

#G1 = nx.Graph(g)

#g1 = igraph.Graph(len(G), zip(*zip(*nx.to_edgelist(G))[:2]))

#g = igraph.Graph.Adjacency(A)
community_walktrap_start_time = time.time()
walktrap_communities=g.community_walktrap()
print("Latapy & Pons random walks Algorithm Run Time:--- %s seconds ---" % (time.time() - community_walktrap_start_time))
print("Latapy & Pons random walks Algorithm Number Of Communities",walktrap_communities.optimal_count)
community_walktrap_clusters = walktrap_communities.as_clustering()
community_walktrap_membership = community_walktrap_clusters.membership
print("Latapy & Pons random walks Algorithm Modularity", g.modularity(community_walktrap_membership))


community_fastgreedy_start_time = time.time()
fastgreedy_communities = g.community_fastgreedy()
print("Fast Greedy Algorithm  Run Time:--- %s seconds ---" % (time.time() - community_fastgreedy_start_time))
print("Fast Greedy Algorithm Number Of Communities",fastgreedy_communities.optimal_count)
community_fastgreedy_clusters = fastgreedy_communities.as_clustering()
community_fastgreedy_membership = community_fastgreedy_clusters.membership
print("Fast Greedy Algorithm Modularity", g.modularity(community_fastgreedy_membership))


community_leading_eigenvector_start_time = time.time()
leading_eigenvector_communities=g.community_leading_eigenvector()
print("Newman's leading eigenvector  Run Time:--- %s seconds ---" % (time.time() - community_leading_eigenvector_start_time))
#print("Community Leading Eigenvector Number Of Communities",com7.optimal_count)
community_leading_eigenvector_membership=leading_eigenvector_communities.membership
print("Newman's leading eigenvector method Modularity", g.modularity(community_leading_eigenvector_membership))


community_leading_eigenvector_start_time = time.time()
leading_eigenvector_communities=g.community_optimal_modularity()
print("Newman's leading eigenvector  Run Time:--- %s seconds ---" % (time.time() - community_leading_eigenvector_start_time))
#print("Community Leading Eigenvector Number Of Communities",com7.optimal_count)
community_leading_eigenvector_membership=leading_eigenvector_communities.membership
print("Newman's leading eigenvector method Modularity", g.modularity(community_leading_eigenvector_membership))












#layout = g.layout("kk")
#igraph.plot(leading_eigenvector_communities, mark_groups = True)
#visual_style = {}        
# Plot the graph
#igraph.plot(g, **visual_style)




#fig=plt.figure(1,figsize=(18,18))
#title = " network" 
#fig.clf()
#nx.draw_networkx(G, cmap = plt.get_cmap('jet'), node_color = values, node_size=30, with_labels=False)
#plt.title(title)
#fig.show()
#plt.waitforbuttonpress()
#plt.close()



#c=list(nx.k_clique_communities(G,4))
#values = [c.get(node) for node in G.nodes()]
#print(c)
#mod = community.modularity(c,G)
#print("modularity:", mod)

