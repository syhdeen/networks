from __future__ import division
import community.community_louvain as community
import networkx as nx
from functools import wraps
from itertools import product
import networkx as nx
from networkx import NetworkXError
from networkx.utils import not_implemented_for
from networkx.algorithms.community.community_utils import is_partition
from networkx.algorithms.community import quality
from networkx.algorithms.community import centrality






                
Facebook = "facebook/facebook_combined.txt"
WikiVote = "wiki-vote/Wiki-Vote.txt"

G = nx.path_graph(10)
comp = centrality.girvan_newman(G)
#values = [comp.get(node) for node in G.nodes()]
#mod = community.modularity(comp,G)

#rint("Louvain Method Modularity", mod)

print(comp)