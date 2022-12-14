# Adapted implementation of Force Atlas 2 Algorithm
# Source: https://doi.org/10.1371/journal.pone.0098679, Jacomy et al.
# Used under Creative Commons Attributions License

# Input: Graph objects consisting of nodes with respective coordinates in given geometry, abstract edges

# Now: used geometry hardcoded (euclidean geometry)
# Goal: give choice of geometry


#### Settings

import numpy as np
import euclideanGeometry as eg
import random as rd


# functions for ForceAtlasAlgorithm

# Creates Instance of chosen geometry with the argument "centerpoint"
geo = eg.EuclideanGeometry([0,0])


# Assigns random coordinates to each vertex as internal property (general points? range?)
# Could be used in form "direction, distance"
def initlayout(graph):
    graph.vp.x = graph.new_vertex_property("float")
    graph.vp.y = graph.new_vertex_property("float")
    # Generates random x- and y-Coordinates for each point
    for v in graph.vertices():
        graph.vp.x[v] = rd.randrange(1000)
        graph.vp.y[v] = rd.randrange(1000)
    return graph
        


### Functions to calculate Forces
# Determines attraction force between two nodes
# Takes coorinates from two points
def attForce(c1, c2):
    att = geo.getDistance(n1,n2)
    return att

# Determines the repulsion force between two nodes
# Takes two nodes and two coordinates (is there a way to access the vertex properties directly?)
def repForce(n1,n2,c1,c2,kr):
    rep = kr*(n1.out_degree()+1)+(n2.out_degree()+1)/geo.getDistance(c1,c2)
    return rep


# Determines the force for strong gravity for each node (keeps graph pulled to the center)
# F(n) = kg(deg(n)+1)disttoorigin(n)
def sgravForce(n, cn, kg):
    grav = kg*(n.out_degree()+1)*geo.getDistance(geo.getOrigin(),cn)
    return grav






### Iteration
# kr is the repulsion constant, kg the gravity constant. Example values: kr = 2, kg = 3
def forceatlas2(graph,kr,kg):
    # Initial settings: Mapping of the graph to coordinates, setting of global speed
    graph = initlayout(graph)
    gswing = 0.0 # TODO: Initial value?
    # Keep track of force on previous and current step for each vertex, as well as swing
    graph.vp.fprev = graph.new_vertex_property("float")
    graph.vp.fcurr = graph.new_vertex_property("float")
    graph.vp.fcurr = graph.new_vertex_property("float")

    # Iteration
    while # TODO: What is the termination condition
        # Compute attraction forces along all edges

        # Compute repulsion forces for all pairs of vertices

        # Compute gravity forces and total forces for current step for each vertex

        # Compute swing, speed and direction (i.e. new coordinates) for each vertex

        # Update previous force and reset current force for each vertex

        # Update global swing




