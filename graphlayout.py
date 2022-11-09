from graph_tool.all import *
import numpy as np
import random as rd
import edgelist as el

# Takes a graph and outputs a .txt file at filenameoutput
# Assumption: Graph uses unique vertex identifiers
# Output format:
# Vertices:
# identifier xcoordinate ycoordinate\n 
# Edges:
# identifier1 identifier 2


# Randomly assings coordinates to vertices and outputs to a text file 
def layout(filenameoutput, graph):
    f = open(filenameoutput, 'w')
    f.write('Vertices:\n')

    # Iterate over Vertices
    for v in graph.vertices():
        f.write(str(v) + ' ' + str(rd.randint(0,100)) + ' ' + str(rd.randint(0,100)) + '\n')
    f.write('Edges:\n')

    # Iterate over Edges
    for e in graph.edges():
        f.write(str(e.source()) + ' ' + str(e.target()) + '\n')


gr = el.edglist('testgraph')
layout('testlayout', gr)
graph_draw(gr, vertex_text=gr.vertex_index, output="testgraph2.pdf")

# Graphlayout concides with the graph drawn, not with the graph specified in testgraph however
	
