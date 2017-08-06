import networkx as nx
import community as c
import matplotlib.pyplot as plt
import sys
import pylab
import copy
import random


def get_community_partitions(graph):
    partitions = community.best_partition(graph)
    communities = [partitions.get(node) for node in graph.nodes()]
    community_count = set(communities)
    # components = sorted(communities, key=len, reverse=True)
    print("====================")
    print("Community detected the following number of partitions: ", len(community_count))
    print("====================")
    for i in community_count:
        print("Count for community {} is {}.".format(i, communities.count(i)))
    return communities


def girvan_newman(G):

    if len(G.nodes()) == 1:
        return [G.nodes()]

    def find_best_edge(G0):
        """
        Networkx implementation of edge_betweenness
        returns a dictionary. Make this into a list,
        sort it and return the edge with highest betweenness.
        """
        eb = nx.edge_betweenness_centrality(G0)
        eb_il = eb.items()
        # eb_il.sort(key=lambda x: x[1], reverse=True)
        eb_il_sorted = sorted(eb_il, key=lambda x: x[1], reverse=True)
        return eb_il_sorted[0][0]

    components = list(nx.community.k_clique_communities(G, 3))
    print(components)

    while len(components) == 1:
        G.remove_edge(*find_best_edge(G))
        components = list(nx.community.k_clique_communities(G, 3))

    result = [c.nodes() for c in components]

    looper = 0
    for c in components:
        print("Call number: ", looper)
        looper += 1
        result.extend(girvan_newman(c))

    return result


def get_girvan_newman_communities(G):
    comp = girvan_newman(G)
    print("====================")
    print("girvan_newman detected the following number of partitions: ", len(comp))
    print("====================")
    return comp



Facebook = "facebook/facebook_combined.txt"
WikiVote = "wiki-vote/Wiki-Vote.txt"

def Price_Model(num_nodes):
    dendrogram={}
    citations=0 
    a = 1
    for i in range(num_nodes):
        dendrogram[i] = []  
        for node in dendrogram.values():
            qi=len(node)
            current_num_nodes=i
            pref_attach_prob =  (qi + a) / (current_num_nodes  +(citations+a ))
            if(random.random() <= pref_attach_prob):
                node.append(i)
                citations += 1

    G = nx.Graph(dendrogram)
    return G
G = Price_G = Price_Model(40)

nx.community.k_clique_communities(G, 3)

print(girvan_newman(G))