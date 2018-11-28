import networkx as nx
import random

def solver(G, k, s, rG, filename):

    def randomized():
        edgeList = list(G.edges)
        nodeList = list(G.nodes)
        buses = [[] for i in range(k)]
        rG_sets = [set(x) for x in rG]

        def createSupernode(v1, v2):
            superName = str(v1) + ", " + str(v2)
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

        while len(list(G.nodes)) > k: #try to create supernodes by combining edge members

            randEdge = edgeList[random.randint(len(edgeList)))] #Find random edge

            v1 = randEdge[0]
            v2 = randEdge[1]
            placed = False

            randomIndices = [i for i in range(len(buses))] #randomize buses to try to add to
            random.shuffle(x)

            for index in randomIndices: #try to add nodes to each bus
                if (len(buses[index]) + 2 > s): #overfull bus
                    continue
                tempBus = buses[index][:].extend([v1, v2])
                subset = False
                for rG_set in rG_sets: #check if a rowdy group is created
                    if all(x in tempBus for x in rG_set):
                        subset = True
                        break
                if subset:
                    continue

                buses[index] = tempBus #add the students
                placed = True
                break
                #score += 1

            if not placed:
                continue

            createSupernode(v1, v2)

        if len(nodeList != 0): #if we have leftover nodes, we must place them



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
