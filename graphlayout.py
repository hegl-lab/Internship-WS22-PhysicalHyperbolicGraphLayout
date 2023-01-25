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
def layout(filenameoutput, graph, points):
    f = open(filenameoutput, 'w')

    # Iterate over Vertices
    for v in graph.iter_vertices():
        f.write(str(v) + ' ' + str(points[v].euclPoint) + '\n')
    f.write('Edges:\n')

    # Iterate over Edges
#    for e in graph.edges():
#        f.write(str(e.source()) + ' ' + str(e.target()) + '\n')


#gr = el.edglist('testgraph')
#layout('testlayout', gr)
#graph_draw(gr, vertex_text=gr.vp.name, output="testgraph2.pdf")
# Graphlayout concides with the graph drawn, not with the graph specified in testgraph however
	
