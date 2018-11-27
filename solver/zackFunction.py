import networkx as nx
import random

def solver(G, k, s, rG, filename):

    def randomized():
        edgeList = list(G.edges)
        nodeList = list(G.nodes)
        buses = [[] for i in range(k)]

        while len(nodeList) != 0:
            edgeList

        # for i in range(len(buses)):
        #     randNode = nodeList.pop(random.randint(range(len(nodeList))))
        #     if randNode != None:
        #         buses[i].append(randNode)
        #         placed.append(randNode)
        #
        # while len(nodeList) != 0:
        #     foundFriend = False
        #     while not foundFriend:
        #         randBus = buses[random.randint(len(buses))]
        #         randStudent = randBus[random.randint(len(randBus))]
        #     randFriendList = list(G.adj[randStudent])
        #     randFriend = randFriendList[random.randint(len(randFriendList))]
        #
        #
        #
        # tempBus = randBus[:].append(randFriend)
        #
        # if (set(randBus) == set(tempBus)):
