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
    listOfEdges = np.empty(shape=(1, 2))
    with open('testgraph') as myFile:
        for chunk in each_chunk(myFile, separator='\n'):
            edge = chunk.split(",")
            try:
                arr = list(map(int, edge))
            except ValueError:
                break
            else:
                edge = np.array([np.asarray(arr)])
            listOfEdges = np.append(listOfEdges, edge, axis=0)
    listOfEdges = np.unique(listOfEdges, axis=0)

    g = Graph(directed=False)

    # Creating a list of all vertices
    uniqueList = np.unique(listOfEdges)

    # Adding the vertices to the graph
    for x in uniqueList:
        globals()[f"v{int(x)}"] = g.add_vertex()

    for x in listOfEdges:
        e = g.add_edge(globals()[f"v{int(x[0])}"], globals()[f"v{int(x[1])}"])
    return g


a = edglist("testgraph")
graph_draw(a, vertex_text=a.vertex_index, output="testgraph.pdf")
