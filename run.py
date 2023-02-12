# Main program
# Input: Graph (as a .txt with according layout)
# (Possibly choice of Geometry)

# Output: Corresponding layout of nodes after applying the force-atlas-2-Algorithm with respective geometry
from graph_tool.all import *
import numpy as np
import edgelist as el
import graphlayout as gl
import fa2general as fa
import euclideanGeometry as eG
import PoincareDiskModel as pdm
import gi.repository 
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
# Takes the filename of the graph, (runs it through the algorithm and returns corresponding graphlayout) -todo
def run(filename):
    graph = el.edglist(filename)
    coords = []
    # Arguments: graph, setup, repulsion const., gravity const., swing const., max. swing, swing tolerance
    for i in range(0,500):
        coords = fa.forceatlas2(graph, coords, 2,30,0.1,10,0.5)
        #gl.layout(filename+str(i)+'result', graph, coords)
        c = pdm.Interface(graph, coords, 1000)
        Gtk.main()
        coords = c.points
        #PDM = pdm.PoincareDiskModel([0,0])
        #PDM.drawGraph(graph, coords, "filename+"result/"+str(i)+".png", 10000)

# Testing cases:
#tests = ["testgraphs/petersen_graph","testgraphs/tree_like","testgraphs/self_loop","testgraphs/disconnected","testgraphs/square_tail","testgraphs/square_complete","testgraphs/single_edge","testgraphs/generic_graph"]
#for x in tests:
#    g = run(x)
#    graph_draw(g, vertex_text=g.vp.name, output="results/"+x+".pdf")
run("testgraphs/petersen_graph")
# Cases that need handling: ,"testgraphs/empty_graph"
