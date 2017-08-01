
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

pos={}
in_y=100

in_step=1.
for in_n in IN_comp:
	pos[in_n]=(100.,in_y)
	in_y=in_y+in_step

out_y=100.
out_step=1.

for out_n in OUT_comp:
	pos[out_n]=(500.,out_y)
	out_y=out_y+out_step



x = [random.randint(0,400) for i in range(0,len(scc))]
y = [random.randint(0,400) for i in range(0,len(scc))]
x = np.array(x)
y = np.array(y)

for i in scc:
	pos[i] =  random.choice(x)+100,random.choice(y)
	print(pos[i])


fig=plt.figure(1,figsize=(18,18))
title = " network"
fig.clf()
IN_compg=G.subgraph(IN_comp)
OUT_compg=G.subgraph(OUT_comp)
pos1=nx.spring_layout(IN_compg)
pos2=nx.spring_layout(sccg)
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
nx.draw(G_bowtie,pos4)
nx.draw_networkx_nodes(G_bowtie,pos4,IN_compg,node_size=30,node_color='grey')
nx.draw_networkx_nodes(G_bowtie,pos4,sccg,node_size=50)
nx.draw_networkx_nodes(G_bowtie,pos4,OUT_compg,node_size=30,node_color='grey')


plt.show() # display
plt.draw()