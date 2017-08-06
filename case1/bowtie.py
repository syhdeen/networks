
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
import random

WikiVote = "wiki-vote/Wiki-Vote.txt"
G = nx.read_edgelist(WikiVote,create_using=nx.DiGraph())
A = nx.adjacency_matrix(G)
scc=[(len(c),c) for c in sorted( nx.strongly_connected_components(G), key=len, reverse=True)][0][1]


IN_comp=[]
for n in scc :
	for s in G.predecessors(n):
		if s in scc: continue
		if not s in IN_comp:
			IN_comp.append(s)

OUT_comp=[]
for n in scc :
	for s in G.successors(n):
		if s in scc: continue
		if not s in IN_comp:
			OUT_comp.append(s)



sccg=G.subgraph(scc)
bowtie = list(scc)+IN_comp+OUT_comp
G_bowtie = G.subgraph(bowtie)

IN_compg=G.subgraph(IN_comp)
OUT_compg=G.subgraph(OUT_comp)
pos1=nx.spring_layout(IN_compg)
pos2=nx.circular_layout(sccg)
pos3=nx.spring_layout(OUT_compg)

for k,v in pos2.items():
    # Shift the x values of every node by 10 to the right
    v[0] = v[0] +10

for k,v in pos3.items():
	    # Shift the x values of every node by 10 to the right
	v[0] = v[0] +20

pos4 = pos1.copy()
pos4.update(pos2)
pos4.update(pos3)

fig=plt.figure(1,figsize=(18,18))
title = " Bow-Tie Structure for Wiki Vote"
fig.clf()
nx.draw(G_bowtie,pos4,IN_comp,node_size=5, node_color="grey")
nx.draw(G_bowtie,pos4,scc,node_size=5)
nx.draw(G_bowtie,pos4,OUT_comp,node_size=5, node_color="grey")

plt.title(title)

plt.show() # display
plt.waitforbuttonpress()

