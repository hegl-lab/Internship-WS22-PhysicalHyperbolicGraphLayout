# Adapted implementation of Force Atlas 2 Algorithm
# Source: https://doi.org/10.1371/journal.pone.0098679, Jacomy et al.
# Used under Creative Commons Attributions License

# Input: Graph objects consisting of nodes with respective coordinates in given geometry, abstract edges

# Now: used geometry hardcoded (euclidean geometry)
# Goal: give choice of geometry


# TODO TODO TODO TODO Caution: Addition of directions might cause problems!

#### Settings

import numpy as np
import euclideanGeometry as eg
import Geometry as pt
import random as rd


# functions for ForceAtlasAlgorithm


# Creates Instance of chosen geometry with the argument "centerpoint"
geo = eg.EuclideanGeometry([0,0])



# Assigns random coordinates to each vertex and gives them back as list
# The coordinates are stored as point objects
def initlayout(vcount):
    points = []
    for i in range(0,vcount):
        points += [geo.randomPoint(1000)]
    return points

def getoutdegs(graph):
    degs = []
    for v in graph.vertices():
        degs += [v.out_degree()]
    return degs

# Quick way to get normed distance
def normdir(r,d):
    if (geo.getDistance(r,d) != 0):
        return geo.direction(r,d) * 1/geo.getDistance(r,d)
    else:
        return geo.getOrigin()


### Functions to calculate Forces
# Determines attraction force between two nodes
# Takes two points as arguments
def attForce(p1, p2):
    att = normdir(p1,p2) * geo.getDistance(p1,p2)
    return att

# Determines the repulsion force between two nodes
# Takes the degree and points of two vertices, as well as the repulsion co
def repForce(d1,d2,p1,p2,kr):
    rep = normdir(p1,p2)* (kr*(d1+1)+(d2+1)/geo.getDistance(p1,p2))
    return rep


# Determines the force for strong gravity for each node (keeps graph pulled to the center)
# F(n) = kg(deg(n)+1)disttoorigin(n)
# Takes the degree and point associated to a vertex and the gravity coefficient
def sgravForce(d, p, kg):
    grav = normdir(p,geo.getOrigin())* (kg*(d+1)*geo.getDistance(geo.getOrigin(),p))
    return grav






### Iteration
# kr is the repulsion constant, kg the gravity constant, kg the swing constant,ksmax and kstol being the maximal swinging and the swinging tolerance. Example values: kr = 2, kg = 3, ks = 0.1, ksmax = 10
def forceatlas2(graph,kr,kg,ks,ksmax,kstol):
    # Initial settings: Mapping of the graph to coordinates, setting of global speed
    vcount = len(graph.get_vertices())
    points = initlayout(vcount)
    degs = getoutdegs(graph)
    orig = geo.getOrigin()

    # Keep track of force on previous and current step for each vertex, as well as swing
    fprev = [orig] * vcount
    direc = [orig] * vcount
    swing = [0.0] * vcount

    # Iteration - TODO: Termination condition currently a set number of steps. Rather express it through swing?
    for step in range(0,10000):
        # Reset all values that need to be recalculated
        gspeed = 0.0
        gswing = 0.0
        gtract = 0.0
        for v in graph.iter_vertices():
            # Compute attraction forces along all edges
            for s, t in graph.iter_out_edges(v): # gets source and target of all the edges containing v (as graph is undirected, and iter_edges doesn't work as intended)
                if s != t:
                    direc[v] += attForce(points[s], points[t])

            # Compute repulsion forces for all pairs of vertices
            for w in graph.iter_vertices():
                if(v != w):
                    direc[v] += repForce(degs[v],degs[w],points[v],points[w],kr)
            # Compute gravity forces and total forces for current step for each vertex
            direc[v] += sgravForce(degs[v], points[v], kg)

            # Compute swing and traction for each vertex and add to global swing/traction TODO Is the distance the correct measure here?
            swing[v] = abs(geo.getDistance(orig,direc[v])-geo.getDistance(orig,fprev[v]))
            tract = abs(geo.getDistance(orig,direc[v])+geo.getDistance(orig,fprev[v])) # Not needed later on
            gswing += swing[v]*(degs[v]+1)
            gtract += tract*(degs[v]+1)


        # Compute global speed TODO limit increase of speed?  
        if gswing != 0.0:
            gspeed = kstol *(gtract/gswing)
        else:
            break

        # Compute speed and new coordinates for each vertex
        for v in graph.iter_vertices():
            speed = ks*gspeed/(1+gspeed*np.sqrt(swing[v]))
            while speed >= ksmax/abs(geo.getDistance(orig,direc[v])+0.00001):
               speed = speed/2 # TODO Is this a useful strategy?
            points[v] = geo.translate(points[v],direc[v]*speed)
            
            # Update previous force and reset current force for each vertex TODO
            fprev[v] = direc[v]
            direc[v] = geo.getOrigin()

    return points


