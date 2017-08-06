import community.community_louvain as community
import networkx as nx
import matplotlib.pyplot as plt
import time
from sklearn.cluster import KMeans



Facebook = "facebook/facebook_combined.txt"
WikiVote = "wiki-vote/Wiki-Vote.txt"

G = nx.read_edgelist(Facebook)
print (G)
louvain_method_start_time = time.time()
louvain_communities = community.best_partition(G)
print("Louvain Method Run Time:--- %s seconds ---" % (time.time() - louvain_method_start_time))
values = [louvain_communities.get(node) for node in G.nodes()]
louvain_modularity = community.modularity(louvain_communities,G)
print("Louvain Method Modularity", louvain_modularity)
#print(values)
        

k=nx.to_numpy_matrix(G)
kmeans = KMeans(n_clusters=2).fit(k)
kmeans = kmeans.labels_
print(kmeans)

#nx.draw_spring(G, cmap = plt.get_cmap('jet'), node_color = values, node_size=30, with_labels=False)
