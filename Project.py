#!/usr/bin/env python
# coding: utf-8

# In[10]:


import networkx as nx
import numpy as np
import math
from random import choices, randint
from string import ascii_lowercase


# In[3]:


G = nx.Graph()


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


# print(G.nodes, G.edges)
# print(randNames(10))

def addVerticesFromList(lst):
    for i in lst:
        G.add_node(i)

#SmallInput creation: 30 people, k = 3, s = 10
def smallInput(): 
    #initialize buses
    busOne, busTwo, busThree = [], [], []
    for i in range(0, 10):
        busOne += [str(i)]
    for i in range(10, 20):
        busTwo += [str(i)]
    for i in range(20, 30):
        busThree += [str(i)]

    #add vertices to graph
    addVerticesFromList(busOne)
    addVerticesFromList(busTwo)
    addVerticesFromList(busThree)

    #maximally connects students within each bus
    for i in range(0, 9):
        for j in range(1, 10):
            G.add_edge(busOne[i], busOne[j])
            G.add_edge(busTwo[i], busTwo[j])
            G.add_edge(busThree[i], busThree[j])

smallInput();

# In[20]:


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




