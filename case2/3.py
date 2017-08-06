import community.community_louvain as community
import networkx as nx
import matplotlib.pyplot as plt
import time
from sklearn.cluster import KMeans

import sys
from operator import gt, lt

import random

import numpy as np
import scipy as sp
import scipy.sparse
from scipy.cluster.vq import vq, kmeans
from scipy.spatial import Delaunay
import igraph





Facebook = "facebook/facebook_combined.txt"
WikiVote = "wiki-vote/Wiki-Vote.txt"

G = nx.read_edgelist(Facebook)
c=nx.connected_components(G)
print(c)