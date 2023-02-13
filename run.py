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
#from PIL import Image  #Uncomment for GIF - needs package
import gi.repository 
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

# Takes the filename of the graph, (runs it through the algorithm and returns corresponding graphlayout) -todo
def run(filename, it,  kr, kg, ks, ksmax, kstol):
    graph = el.edglist(filename)
    coords = []
    # Arguments: graph, setup, repulsion const., gravity const., swing const., max. swing, swing tolerance
        # Repulsion Constant: Integers for eG, <<<1 for pdm
        # The more vertices in the graph, The higher the total energy in the graph; one has to compensate this by decreasing the repulsion for higher vertex counts
        # Be aware that the graphs react *very* sensitive to changes in the constants
        
    for i in range(0,it):
        coords = fa.forceatlas2(graph, coords, kr, kg, ks, ksmax, kstol)
        #gl.layout(filename+str(i)+'result', graph, coords)
        c = pdm.Interface(graph, coords, 1000,  kr, kg, ks, ksmax, kstol)
        #PDM = pdm.PoincareDiskModel([0,0]) # Uncomment for GIF
        #PDM.drawGraph(graph, coords, "filename+"result/"+str(i)+".png", 1000) #Uncomment for GIF
        Gtk.main()
        coords = c.points
    #toGif(filename, it) # Takes A LOT of time - uncomment for GIF

# Uncomment for GIF   
#def toGif(filename, it):
#    imagelist = []

#    for i in range(0,it):
#        img = Image.open(filename+"result/"+str(i)+".png", mode='r', formats=None)
#        img.save(filename+"result/"+str(i)+".jpg")
#        imagelist += [filename+"result/"+str(i)+".jpg"]
#    clip = ImageSequenceClip(imagelist, fps=5)
#    clip.write_gif(filename+'.gif', fps=5)
        
        

# Testing cases:
#tests = ["testgraphs/petersen_graph","testgraphs/tree_like","testgraphs/self_loop","testgraphs/disconnected","testgraphs/square_tail","testgraphs/square_complete","testgraphs/single_edge","testgraphs/generic_graph"]
#for x in tests:
#    g = run(x)
#    graph_draw(g, vertex_text=g.vp.name, output="results/"+x+".pdf")
run("testgraphs/petersen_graph", 50)
# Cases that need handling: ,"testgraphs/empty_graph"
