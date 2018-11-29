import networkx as nx
import random

G = nx.read_gml("../inputs/small/graph.gml")
k = 3
s = 12
rG = [['1', '5'],
['0', '12'],
['1', '9'],
['0', '13'],
['2', '14'],
['0', '4'],
['22', '2'],
['1', '4'],
['0', '11'],
['0', '14'],
['0', '24'],
['1', '12'],
['23', '2'],
['0', '2'],
['0', '16'],
['24', '2'],
['1', '6'],
['11', '23'],
['12', '24'],
['20', '2'],
['1', '20'],
['1', '2'],
['14', '3'],
['0', '25'],
['21', '2'],
['18', '2'],
['0', '10'],
['1', '23'],
['17', '2'],
['0', '21'],
['5', '17'],
['8', '20'],
['1', '10'],
['9', '21'],
['1', '8'],
['0', '8'],
['16', '2'],
['0', '17'],
['0', '15'],
['13', '25'],
['1', '11'],
['0', '18'],
['0', '5'],
['0', '20'],
['7', '19'],
['19', '2'],
['1', '16'],
['10', '22'],
['1', '25'],
['25', '2'],
['0', '9'],
['1', '24'],
['1', '14'],
['1', '22'],
['4', '16'],
['6', '18'],
['1', '7'],
['1', '3'],
['0', '6'],
['1', '15'],
['1', '13'],
['0', '3'],
['0', '23'],
['1', '21'],
['1', '18'],
['0', '7'],
['0', '22'],
['0', '19'],
['1', '17'],
['15', '4'],
['1', '19'],
['3', '15']
]
filename = 'small'

# def createSupernode(v1, v2):
#     superName = str(v1) + "," + str(v2)
#     G.add_node(superName)
#     friendsToAdd = set([])
#     for friend in G.adj[v1]:
#         friendsToAdd.add((superName, friend))
#     for friend in G.adj[v2]:
#         friendsToAdd.add((superName, friend))
#     G.add_edges_from(friendsToAdd)
#     G.remove_node(v1)
#     G.remove_node(v2)
#     return superName
#
# def splitSupernode(v):
#     nodeStrings = v.split(",")
#     for node in nodeStrings:
#         G.add_node(node)
#     G.remove_node(v)
#     for node in nodeStrings:
#         for neighbor in graph.adj[node]:
#             G.add_edge(node, findNeighbor(neighbor))
#
# def findNeighbor(v):
#     for node in list(G.nodes):
#         if v in node.split(','):
#             return node
#
# G = nx.Graph()
# G.add_nodes_from(['1', '2', '3', '4'])
# G.add_edges_from([('1','2'), ('2','3'), ('1', '4')])
# graph = G.copy()
# createSupernode('1', '2')
# createSupernode('1,2', '3')
# splitSupernode("1,2,3")
# print(G.nodes, G.edges)

def solver(graph, k, s, rG, filename):

    def randomized():
        buses = [[] for i in range(k)]
        rG_sets = [set(x) for x in rG]
        G = graph.copy()

        def createSupernode(v1, v2):
            superName = str(v1) + "," + str(v2)
            G.add_node(superName)
            friendsToAdd = set([])
            for friend in G.adj[v1]:
                friendsToAdd.add((superName, friend))
            for friend in G.adj[v2]:
                friendsToAdd.add((superName, friend))
            G.add_edges_from(friendsToAdd)
            G.remove_node(v1)
            G.remove_node(v2)
            return superName

        def splitSupernode(v):
            nodeStrings = v.split(",")
            for node in nodeStrings:
                G.add_node(node)
            G.remove_node(v)
            for node in nodeStrings:
                for neighbor in graph.adj[node]:
                    G.add_edge(node, findNeighbor(neighbor))

        def findNeighbor(v):
            for node in list(G.nodes):
                if v in node.split(','):
                    return node

        def placeLeftover():
            if (len(list(G.nodes)) <= k):
                return

            def sizeSecond(lst):
                return lst[1]

            while len(list(G.nodes)) > k:

                lonelyBoiz = [x for x in list(G.nodes) if len(x.split(',')) == 1]
                superNodes = [x for x in list(G.nodes) if len(x.split(',')) > 1]
                currStudentCount = [[i, len(superNodes[i].split(","))] for i in range(len(superNodes))]
                currStudentCount.sort(key=sizeSecond)

                if len(lonelyBoiz) == 0:
                    splitSupernode(superNodes[currStudentCount[0][0]])

                lonelyBoiz = [x for x in list(G.nodes) if len(x.split(',')) == 1]
                superNodes = [x for x in list(G.nodes) if len(x.split(',')) > 1]
                currStudentCount = [[i, len(superNodes[i].split(","))] for i in range(len(superNodes))]
                currStudentCount.sort(key=sizeSecond)

                for boi in lonelyBoiz:
                    superNodes = [x for x in list(G.nodes) if len(x.split(',')) > 1]
                    currStudentCount = [[i, len(superNodes[i].split(","))] for i in range(len(superNodes))]
                    currStudentCount.sort(key=sizeSecond)
                    createSupernode(boi, superNodes[currStudentCount[0][0]])

        while len(list(G.nodes)) > k: #try to create supernodes by combining edge members

            if len(list(G.edges)) != 0:
                edgeList = list(G.edges)
                randEdge = edgeList[random.randint(0, len(edgeList)-1)] #Find random edge

                v1 = randEdge[0]
                sizeV1 = len(v1.split(','))
                v2 = randEdge[1]
                sizeV2 = len(v2.split(','))

                #try to add nodes to each bus
                if (sizeV1 + sizeV2 > s): #overfull bus
                    continue

                subset = False

                for rG_set in rG_sets: #check if a rowdy group is created
                    vTot = v1 + v2
                    if all(x in (vTot).split(',') for x in rG_set):
                        subset = True
                        break
                if subset:
                    continue

                createSupernode(v1, v2)

            else: #if we have leftover nodes after combining edges, we must place them
                placeLeftover()

        buses = [x.split(',') for x in list(G.nodes)]
        return buses

    return randomized()

print(solver(G, k, s, rG, filename))

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
