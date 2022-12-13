from graph_tool.all import *
import numpy as np


def each_chunk(stream, separator):
    buffer = ''
    while True:  # until EOF
        chunk = stream.read(4096)  # I propose 4096 or so
        if not chunk:  # EOF?
            yield buffer
            break
        buffer += chunk
        while True:  # until no separator is found
            try:
                part, buffer = buffer.split(separator, 1)
            except ValueError:
                break
            else:
                yield part


def edglist(filename):
    '''Takes a .txt file and returns a edgelist out of the textfile, where the graph g has the property g.vp.name'''
    listOfEdges = np.empty(shape=(1, 2))
    # print(listOfEdges)
    with open(filename, 'r') as myFile:
        for chunk in each_chunk(myFile, separator='\n'):
            edge = chunk.split(",")
            try:
                arr = list(map(int, edge))
            except ValueError:
                break
            else:
                edge = np.array([np.asarray(arr)])
            listOfEdges = np.append(listOfEdges, edge, axis=0)
    listOfEdges = np.delete(listOfEdges, 0, 0)
    listOfEdges = np.unique(listOfEdges, axis=0)
    # print(listOfEdges)

    g = Graph(directed=False)
    vertexName = g.new_vertex_property("string")
    # Creating a list of all vertices
    uniqueList = np.unique(listOfEdges)
    dictVertexName = dict()
    # Adding the vertices to the graph
    for x in uniqueList:
        print(x)
        i = g.add_vertex()
        vertexName[i] = str(int(x))
        dictVertexName[x] = g.vertex_index[i]

    for x in listOfEdges:
        e = g.add_edge(g.vertex(dictVertexName[x[0]]), g.vertex(dictVertexName[x[1]]))
    #print(dictVertexName)
    g.vertex_properties["name"] = vertexName
    return g
