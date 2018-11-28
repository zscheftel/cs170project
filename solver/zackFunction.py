import networkx as nx
import random

def solver(G, k, s, rG, filename):

    def randomized():
        buses = [[] for i in range(k)]
        rG_sets = [set(x) for x in rG]
        counter = len(nodeList) // 10

        def createSupernode(v1, v2):
            superName = str(v1) + "," + str(v2)
            G.add_node(superName)
            friendsToAdd = {}
            for friend in G.adj[v1]:
                friendsToAdd.add((superName, friend))
            for friend in G.adj[v2]:
                friendsToAdd.add((superName, friend))
            G.add_edges_from(friendsToAdd)
            G.remove_node(v1)
            G.remove_node(v2)
            return superName

        while counter > 0: #try to create supernodes by combining edge members

            edgeList = list(G.edges)
            randEdge = edgeList[random.randint(len(edgeList)))] #Find random edge

            v1 = randEdge[0]
            sizeV1 = len(",".split(v1))
            v2 = randEdge[1]
            sizeV2 = len(",".split(v2))

            #try to add nodes to each bus
            if (sizeV1 + sizeV2 > s): #overfull bus
                counter -= 1
                continue

            subset = False

            for rG_set in rG_sets: #check if a rowdy group is created
                if all(x in ",".split(v1+v2) for x in rG_set):
                    subset = True
                    break
            if subset:
                counter -= 1
                continue

            counter = len(nodeList) // 10
            createSupernode(v1, v2)

        if len(nodeList) != k: #if we have leftover nodes, we must place them
            lonelyBoiz = [x for x in list(G.nodes) if len(",".split(x)) == 1]
            superNodes = [x for x in list(G.nodes) if len(",".split(x)) > 1]

            currStudentCount = [[i, len(",".split(superNodes[i]))] for i in len(superNodes)]

            def sizeSecond(lst):
                return lst[1]
            currStudentCount.sort(key=sizeSecond)

            currNode = 0
            for boi in lonelyBoiz:
                if len(",".split(superNodes[currNode])) > s:
                    currNode += 1
                else:
                    createSupernode(boi, superNodes[currNode])

        buses = [",".split(x) for x in list(G.nodes)]
        return buses




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
