import networkx as nx
import random
import queue as Q
import math
import Greedy

def solver(graph, k, s, rG):
	k = int(k)
	s = int(s)
	graph.remove_edges_from(graph.selfloop_edges())

	def randomized(tries):
		if tries < 0:
			return Greedy.solver(graph, k, s, rG)
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

		def combineEdges():
			counter = len(list(G.nodes)) // 10
			while len(list(G.edges)) != 0 and counter > 0:
				edgeList = list(G.edges)
				randEdge = edgeList[random.randint(0, len(edgeList)-1)] #Find random edge

				v1, v2 = randEdge[0], randEdge[1]
				sizeV1, sizeV2 = len(v1.split(',')), len(v2.split(','))
				subset = False

				for rG_set in rG_sets: #check if a rowdy group is created
					vTot = v1 + v2
					if all(x in (vTot).split(',') for x in rG_set):
						subset = True
					if subset:
						break

				if not (sizeV1 + sizeV2 > s) and not subset: #neither overfull bus nor rowdy group
					createSupernode(v1, v2)
				else:
					counter -= 1

		def placeLeftover():
			if (len(list(G.nodes)) <= k):
				return

			def sizeSecond(lst):
				return lst[1]

			counter = len(list(G.nodes))
			while len(list(G.nodes)) > k and counter > 0:

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

					placed = False
					for i in range(len(superNodes)):
						subset = False
						for rG_set in rG_sets: #check if a rowdy group is created
							temp = superNodes[currStudentCount[i][0]] + "," + boi
							if all(x in (temp).split(',') for x in rG_set):
								subset = True
								break
						if not subset:
							createSupernode(boi, superNodes[currStudentCount[i][0]])
							placed = True
							break
					if not placed:
						for node in superNodes:
							if len(node.split(",")) < s:
								createSupernode(boi, node)
								break
				counter -= 1

		def makeEnoughBuses():
			priorityDict = {}
			adjlist = list(nx.generate_adjlist(graph))
			for lst in adjlist:
				key = lst.split(' ')[0]
				#all of the following are needed to calculate the priority
				friendsInGraph = len(lst.split(' ')) - 1 #total number of friends remaining in the Graph
				priority = friendsInGraph
				priorityDict[key] = priority

			#add dictionary entries to a priority queue
			PQ = Q.PriorityQueue()
			tiebreaker = 0 #arbitrary counter to break ties if entries have the same priority
			for key in priorityDict.keys():
				entry = (priorityDict[key], tiebreaker, key)
				PQ.put(entry)
				tiebreaker += 1

			for bus in buses:
				if len(bus) == 0:
					student = PQ.get()[2]
					for bus in buses:
						if student in bus:
							bus.remove(student)
					bus.append(student)

		if len(list(G.nodes)) > k:

			if len(list(G.edges)) != 0: #try to create supernodes by combining edge members
				combineEdges()

			#if we have leftover nodes after combining edges, we must place them
			placeLeftover()

		buses = [x.split(',') for x in list(G.nodes)]
		while len(buses) < k:
			buses.append([])
		makeEnoughBuses()
		if len(buses) > k or len([x for x in buses if x == []]) != 0 or len([x for x in buses if len(x) > s]) != 0:
			return randomized(tries-1)
		else:
			return buses

	return randomized(10)

#print(solver(G, k, s, rG, filename))
