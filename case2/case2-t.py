import community.community_louvain as community
import networkx as nx
import matplotlib.pyplot as plt
import igraph
import time


#better with karate_graph() as defined in networkx example.
#erdos renyi don't have true community structure



Facebook = "facebook/facebook_combined.txt"
WikiVote = "wiki-vote/Wiki-Vote.txt"

G = nx.read_edgelist(Facebook)
g = igraph.Graph.Read_Ncol(Facebook, directed=False)
#g1 = igraph.Graph(len(G), zip(*zip(*nx.to_edgelist(G))[:2]))
#g1 = igraph.Graph.Adjacency((nx.to_numpy_matrix(G) > 0).tolist())

#g = igraph.Graph.Adjacency(A)
community_walktrap_start_time = time.time()
com5=g.community_walktrap()
print("--- %s seconds ---" % (time.time() - community_walktrap_start_time))
community_walktrap_clusters=com5.as_clustering()
community_walktrap_membership=community_walktrap_clusters.membership
print("Community Walktrap Modularity", g.modularity(community_walktrap_membership))


community_fastgreedy_start_time = time.time()
com6=g.community_fastgreedy()
print("--- %s seconds ---" % (time.time() - community_fastgreedy_start_time))
community_fastgreedy_clusters=com6.as_clustering()
community_fastgreedy_membership=community_fastgreedy_clusters.membership
print("Community Walktrap Modularity", g.modularity(community_fastgreedy_membership))

community_spinglass_start_time = time.time()
com7=g.community_spinglass()
print("--- %s seconds ---" % (time.time() - community_spinglass_start_time))

community_spinglass_clusters=com7.as_clustering()
community_spinglass_membership=community_spinglass_clusters.membership
print("Community Walktrap Modularity", g.modularity(community_spinglass_membership))
#print(com5.optimal_count)
#print(com5.as_clustering())



#communities = g1.community_edge_betweenness()

# not really sure what to do next
#num_communities = communities.optimal_count
#print(num_communities)
#communities.as_clustering(num_communities)
#igraph.Graph.GraphBase.modularity(g, com7) 
#print(g.modularity(com6))
part = community.best_partition(G)
values = [part.get(node) for node in G.nodes()]
mod = community.modularity(part,G)
print("modularity:", mod)
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

