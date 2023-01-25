# Main program
# Input: Graph (as a .txt with according layout)
# (Possibly choice of Geometry)

# Output: Corresponding layout of nodes after applying the force-atlas-2-Algorithm with respective geometry
from graph_tool.all import *
import numpy as np
import edgelist as el
import graphlayout as gl
import forceatlas2 as fa

# Takes the filename of the graph, (runs it through the algorithm and returns corresponding graphlayout) -todo
def run(filename):
    graph = el.edglist(filename)
    coords = fa.forceatlas2(graph,20,10,0.1,10,0.1)
    gl.layout(filename+'result', graph, coords)


# Testing cases:
#tests = ["testgraphs/petersen_graph","testgraphs/tree_like","testgraphs/self_loop","testgraphs/disconnected","testgraphs/square_tail","testgraphs/square_complete","testgraphs/square_empty","testgraphs/single_edge","testgraphs/generic_graph"]
#for x in tests:
#    g = run(x)
#    graph_draw(g, vertex_text=g.vp.name, output="results/"+x+".pdf")
run("testgraphs/single_edge")
# Cases that need handling: ,"testgraphs/empty_graph"
