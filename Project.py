#!/usr/bin/env python
# coding: utf-8

# In[10]:


import networkx as nx
import numpy as np
import math
import random
from random import choices, randint, shuffle
from string import ascii_lowercase


# In[3]:


G = nx.Graph()
smallG = nx.Graph()
smallBuses = []

mediumG = nx.Graph()
mediumBuses = []

largeG = nx.Graph()
largeBuses = []

# In[11]:


def addVertices(G, V):
    G.add_nodes_from(V)
    
def addEdges(G, V):
    for i in range(math.floor(np.random.random()*len(V)*len(V))):
        addEdge(G)
        
def addEdge(G):
    gNodes = list(G.nodes)
    lenNodes = len(gNodes)
    indexOne = math.floor(np.random.random() * lenNodes)
    indexTwo = math.floor(np.random.random() * lenNodes)
    while indexOne == indexTwo:
        indexTwo = math.floor(np.random.random() * lenNodes)
    vertexOne = gNodes[indexOne]
    vertexTwo = gNodes[indexTwo]
    G.add_edge(vertexOne, vertexTwo)

def randNames(n):
    return ["".join(choices(ascii_lowercase, k=3)) for _ in range(n)]

def chooseSK(n):
    k = np.randint[0, n]
    s = math.floor(n / k) + 1
    return k, s

def rowdyL(size):
    L = []
    for i in range(np.random.randint(range(size))):
        l = []
        # for j in range(skewedProb(size)):
            
def skewedProb(size):
    prob = [0]*size
    for i in range(len(prob)):
        prob[i] = (1 / i + 1)
    prob /= np.sum(prob)
    number = np.random.choice(size, 1, p=prob)
    return number


# In[7]:

def randNum(i):
    return ["".join()]
vertices = ["Alice", "Bob", "Carol"]
addVertices(G, vertices)
addEdges(G, vertices)


# In[14]:


def addVerticesFromList(lst):
    for i in lst:
        G.add_node(i)

#adds friendships from the ith student in bus one to the (i + 3)nd student in bus two
def addDiagonalFriendships(graph, buses):
    busCapacity = len(buses[1])
    for i in range(0, busCapacity - 1):
        graph.add_edge(buses[1][i], buses[2][i + 1])
    graph.add_edge(buses[1][busCapacity - 1], buses[2][0])


def makeRowdyAB(busList):
    rowdy = []
    f = open("inputs/small/parameters.txt", "w")

    for i in busList[0]:
        for j in range(1, len(busList)):
            for k in busList[j]:
                f.write("{}".format([i, k]) + "\n")
    return rowdy


def smallInput(buses):
    #initialize input file
    f = open("inputs/small/parameters.txt", "w")
    k = 3
    s = 12
    f.write(str(k) + "\n" + str(s) + "\n")

    rowdy = []

    for i in buses[0]:
        for j in buses[1]:
            rowdy += [[i, j]]
        for k in buses[2]:
            rowdy += [[i, k]]
    # rowdy += [makeRowdyAB(buses)]

    #horizontal and diagonal rowdyness
    for i in range(0, len(buses[1])):
        #for horizontal rowdy groups
        rowdy += [[buses[1][i], buses[2][i]]]
        #if don't have to make rowdy from end of one list to start of another
        if (i < len(buses) - 1):
            rowdy += [[buses[2][i], buses[1][i + 1]]]
        #otherwise do it
        else:
            rowdy += [[buses[2][i], buses[1][0]]]

    random.shuffle(rowdy)

    for group in rowdy:
        f.write("{}".format(group) + "\n")

    f.close()

#SmallInput creation: 26 people, k = 3, s = 10
def smallInputSolution(): 
    
    #initialize buses, one bus has two people, rest have 12 each of invalid vertices
    busOne, busTwo, busThree = [], [], []
    for i in range(0, 2):
        busOne += [str(i)]
    for i in range(2, 14):
        busTwo += [str(i)]
    for i in range(14, 26):
        busThree += [str(i)]

    smallBuses = [busOne, busTwo, busThree]

    #add vertices to graph
    addVerticesFromList(busOne)
    addVerticesFromList(busTwo)
    addVerticesFromList(busThree)

    #adds friendship between the two vertices in first bus
    smallG.add_edge(busOne[0], busOne[1])

    #adds diagonal friendships between buses two and three
    addDiagonalFriendships(smallG, smallBuses)

    f = open("outputs/small.out", "w")
    f.write("{} \n".format(busOne))
    f.write("{} \n".format(busTwo))
    f.write("{} \n".format(busThree))

    smallInput(smallBuses)
    nx.write_gml(smallG, "inputs/small/graph.gml")

    f.close()




def mediumInput(buses):
    f = open("inputs/medium/parameters.txt", "w")
    k = 3
    s = 124
    f.write(str(k) + "\n" + str(s) + "\n")

    rowdy = []

    for i in buses[0]:
        for j in buses[1]:
            rowdy += [[i, j]]
        for k in buses[2]:
            rowdy += [[i, k]]
    # rowdy += [makeRowdyAB(buses)]

    #horizontal and diagonal rowdyness
    for i in range(0, len(buses[1])):
        #for horizontal rowdy groups
        rowdy += [[buses[1][i], buses[2][i]]]
        #if don't have to make rowdy from end of one list to start of another
        if (i < len(buses) - 1):
            rowdy += [[buses[2][i], buses[1][i + 1]]]
        #otherwise do it
        else:
            rowdy += [[buses[2][i], buses[1][0]]]
    random.shuffle(rowdy)

    for group in rowdy:
        f.write("{}".format(group) + "\n")

    f.close()

def mediumInputSolution():
    busOne, busTwo, busThree = [], [], []
    for i in range(0, 2):
        busOne += [str(i)]
    for i in range(2, 126):
        busTwo += [str(i)]
    for i in range(126, 250):
        busThree += [str(i)]

    mediumBuses = [busOne, busTwo, busThree]

    #add vertices to graph
    addVerticesFromList(busOne)
    addVerticesFromList(busTwo)
    addVerticesFromList(busThree)

    #adds friendship between the two vertices in first bus
    mediumG.add_edge(busOne[0], busOne[1])

    #adds diagonal friendships between buses two and three
    addDiagonalFriendships(mediumG, mediumBuses)

    f = open("outputs/medium.out", "w")
    f.write("{} \n".format(busOne))
    f.write("{} \n".format(busTwo))
    f.write("{} \n".format(busThree))

    mediumInput(mediumBuses)
    nx.write_gml(mediumG, "inputs/medium/graph.gml")

    f.close()

def largeInput(buses):
    f = open("inputs/large/parameters.txt", "w")
    k = 3
    s = 249
    f.write(str(k) + "\n" + str(s) + "\n")

    rowdy = []

    for i in buses[0]:
        for j in buses[1]:
            rowdy += [[i, j]]
        for k in buses[2]:
            rowdy += [[i, k]]
    # rowdy += [makeRowdyAB(buses)]

    #horizontal and diagonal rowdyness
    for i in range(0, len(buses[1])):
        #for horizontal rowdy groups
        rowdy += [[buses[1][i], buses[2][i]]]
        #if don't have to make rowdy from end of one list to start of another
        if (i < len(buses) - 1):
            rowdy += [[buses[2][i], buses[1][i + 1]]]
        #otherwise do it
        else:
            rowdy += [[buses[2][i], buses[1][0]]]

    random.shuffle(rowdy)

    for group in rowdy:
        f.write("{}".format(group) + "\n")

    f.close()


def largeInputSolution():
    busOne, busTwo, busThree = [], [], []
    for i in range(0, 2):
        busOne += [str(i)]
    for i in range(2, 251):
        busTwo += [str(i)]
    for i in range(251, 500):
        busThree += [str(i)]

    largeBuses = [busOne, busTwo, busThree]

    #add vertices to graph
    addVerticesFromList(busOne)
    addVerticesFromList(busTwo)
    addVerticesFromList(busThree)

    #adds friendship between the two vertices in first bus
    largeG.add_edge(busOne[0], busOne[1])

    #adds diagonal friendships between buses two and three
    addDiagonalFriendships(largeG, largeBuses)

    f = open("outputs/large.out", "w")
    f.write("{} \n".format(busOne))
    f.write("{} \n".format(busTwo))
    f.write("{} \n".format(busThree))

    largeInput(largeBuses)
    nx.write_gml(largeG, "inputs/large/graph.gml")

    f.close()
# In[20]:

smallInputSolution()
mediumInputSolution()
largeInputSolution()


def createInput(n, size):
    G = nx.Graph()
    vertices = randNames(n)
    addVertices(G, vertices)
    addEdges(G, vertices)
    k, s = chooseSK(n)
    L = rowdyL(size)
    return G
# H = createInput(50)


# In[ ]:





# In[ ]:





# In[ ]:




