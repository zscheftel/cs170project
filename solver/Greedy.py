import networkx as nx
import queue as Q
import math

global solution, buses, currBus
solution = []
#initialFriends = []

#calculate how many friends student1 has in the current bus
def findFriendsOnCurrentBus(student1, adjlist, buses, currBus):
	friendsOnBus = 0
	for student2 in buses[currBus]:
		for lst in adjlist:
			if (lst.split(' ')[0] == student1) and (student2 in lst):
				friendsOnBus += 1
	return friendsOnBus

#check if adding student to the current bus giving the current Rowdy lists will form a rowdy group, returns a boolean
def willBeRowdy(student, currRowdy, busNum):
	for rowdy in currRowdy:
		try:
			rowdy.remove(student)
			if len(rowdy) == 0:
				rowdy.append(student)
				return True
		except ValueError:
			continue
	return False

#iterate through priority queue and dictionary and basically update everything whenever
#a student is successfully added to a bus
def updatePriorities(PQ, totalStudents, buses, currBus, s, adjlist, friendsRemaining):
	#remove all entries from PQ and add them into list
	while not PQ.empty():
		entries = []
		entries.append(PQ.get())
	#iterate through list and add back into PQ
	for entry in entries:
		key = entry[2]
		studentIndex = entry[1]
		#all of the following are needed to calculate the priority
		friendsInGraph = friendsRemaining[studentIndex] #total number of friends remaining in the Graph
		# print("KEY")
		# print(key)
		# print("GRAPH")
		# print(adjlist)
		# print("BUSES")
		# print(buses)
		# print("WHICH BUS")
		# print(currBus)
		friendsOnCurrentBus = findFriendsOnCurrentBus(key, adjlist, buses, currBus)
		spotsRemaining = s - len(buses[currBus])
		print(friendsInGraph)
		# #bug in priority stuff but will fix this when building updatePriorities
		# if spotsRemaining == 0:
		# 	break
		priority = friendsOnCurrentBus * (s / spotsRemaining) * math.log(totalStudents, 2) + friendsInGraph
		priority = (-1) * priority #PQ in python sorts by min. priority; since we want max. priority, make negative

		#add new entry
		newEntry = (priority, studentIndex, key)
		PQ.put(newEntry)


#overall solver
def solver(G, k, s, L):
	k = int(k)
	s = int(s)
	G.remove_edges_from(G.selfloop_edges())
	adjlist = list(nx.generate_adjlist(G)) #adjlist is a list of strings
	#initialFriends = adjlist

	#initialize buses list
	buses = []
	currBus = 0 #counter for which bus you're currently trying to add to
	emptyBuses = k
	for i in range(0, k):
		bus = []
		buses.append(bus)
	#initialize priorityDict to be key = name, value = priority heuristic
	priorityDict = {}

	friendsRemaining = []
	#have a list to keep track of how many friends each student has remaining in the graph
	# for i in range(len(adjlist)):
	# 	friendsRemaining.append([])

	# studentIndex = 0
	for lst in adjlist:
		key = lst.split(' ')[0]
		#all of the following are needed to calculate the priority
		friendsInGraph = len(lst.split(' ')) - 1 #total number of friends remaining in the Graph
		#print(friendsInGraph)
		friendsRemaining.append(friendsInGraph)
		# studentIndex += 1
		friendsOnCurrentBus = findFriendsOnCurrentBus(key, adjlist, buses, currBus)
		spotsRemaining = s
		print(friendsRemaining)
		# #bug in priority stuff but will fix this when building updatePriorities
		# if spotsRemaining == 0:
		# 	break
		totalStudents = len(adjlist)
		priority = friendsOnCurrentBus * (s / spotsRemaining) * math.log(totalStudents, 2) + friendsInGraph
		priority = (-1) * priority #PQ in python sorts by min. priority; since we want max. priority, make negative
		priorityDict[key] = priority
	#add dictionary entries to a priority queue
	PQ = Q.PriorityQueue()
	tiebreaker = 0 #arbitrary counter to break ties if entries have the same priority
	for key in priorityDict.keys():
		entry = (priorityDict[key], tiebreaker, key)
		PQ.put(entry)
		tiebreaker += 1

	#make one copy of rowdy groups that corresponds to each bus
	tempRowdies = []
	for i in range(0, k):
		tempRowdies.append(L.copy())

	stillRowdy = []
	while not PQ.empty() and PQ.qsize() > emptyBuses:
		if len(buses[currBus]) < s:
			bus = buses[currBus]
			tempRowdy = tempRowdies[currBus]
			maxStudent = PQ.get()[2]
			inBus = False
			violation = False
			#check if adding will form a rowdy group
			violation = willBeRowdy(maxStudent, tempRowdy, currBus)
			if not violation:
				if len(bus) == 0:
					emptyBuses -= 1
				bus.append(maxStudent)

				# for lst in adjlist:
				# 	if key == lst.split(' ')[0]:
				# 		if maxStudent in lst:
				# 			friendsRemaining[] -= 1


				#actually remove student from graph and reset adjacency list

				updatePriorities(PQ, totalStudents, buses, currBus, s, adjlist, friendsRemaining)
				inBus = True
			else:
				violation = False
				for j in range(currBus, len(buses)):
					violation = willBeRowdy(maxStudent, tempRowdy, j)
					if not violation and len(buses[j]) < s:
						if len(buses[j]) == 0:
							emptyBuses -= 1
						buses[j].append(maxStudent)
						updatePriorities(PQ, totalStudents, buses, currBus, s, adjlist, friendsRemaining)
						inBus = True
						# want to remove from the actual rowdy groups
						for rowdy in L:
							tempRowdy.remove(maxStudent)
				if not inBus:
					stillRowdy.append(maxStudent)
		else:
			currBus += 1

	if PQ.qsize() == emptyBuses:
		for bus in buses:
			if len(bus) == 0:
				bus.append(PQ.get()[2])

	buses.sort() #sorting buses by length, so least capacity is first
	counter = 0
	while len(stillRowdy) != 0:
		if len(buses[counter]) < s:
			buses[counter].append(stillRowdy.pop(0))
		else:
			counter += 1

	return buses














# def solver(G, k, s, L): #k = number of buses, s = capacity of buses, L = list of lists of rowdy groups
#     #adjlist is a list of strings
#     adjlist = nx.generate_adjlist(G)
#     #find kid w/ max # of friends

#     numFriends = {}
#     stillRowdy = []
#     buses = []

#     #initialize buses list
#     for i in range(0, k):
#         bus = []
#         buses.append(bus)

#     #supposed to sort the dictionary by the most number of friends
#     for i in adjlist:
#         key = i[0:3]
#         value = (len[i] - 3)/4
#         numFriends[key] = value
#     numFriendsSorted = sorted(numFriends, key = numFriends.get, reverse = True)

#     #retrieve kid w/ max # of friends and keep adding until first bus full and then next bus
#     #unless adding the max kid creatse a rowdy group: else iterate through next buses, keep trying

#     for i in range(len(buses)):
#         bus = buses[i]
#         while len(bus) < s:
#             inBus = False
#             tempRowdy = L.copy()
#             violation = False
#             maxStudent = numFriendsSorted.getKey(0)
#             #check if adding will form a rowdy group
#             for rowdy in tempRowdy:
#                 rowdy.remove(maxStudent)
#                 if len(rowdy) == 0:
#                     rowdy.add(maxStudent)
#                     violation = True
#                     break
#             if not violation:
#                 bus.append(maxStudent)
# 				numFriendsSorted.remove(maxStudent)
#                 inBus = True
#             else:
#                 violation = False
#                 #for each additional bus, check if forms rowdy group
#                 for j in range(i, len(buses)):
#                     for rowdy in tempRowdy:
#                         rowdy.remove(maxStudent)
#                         if len(rowdy) == 0 or len(bus) == s:
#                             rowdy.add(maxStudent)
#                             violation = True
#                             break
#                     if not violation:
#                         bus.append(maxStudent)
#         				numFriendsSorted.remove(maxStudent)
#                         inBus = True
#                     else:
#                         stillRowdy.append(maxStudent)
#                         continue
#                 if not inBus:
#                     stillRowdy.append(maxStudent)




	#
	# for b in range(0, k):
	#     bus = []
	#     counter = 0
	#     while counter < s:
	#         tempRowdy = L.copy()
	#         violation = false
	#         # unideal, only gets students with most friends, not friends of friends
	#         maxStudent = numFriendsSorted.getKey(0)
	#         for rowdy in tempRowdy:
	#             rowdy.remove(maxStudent)
	#             if len(rowdy) == 0:
	#                 rowdy.add(maxStudent)
	#                 violation = true
	#                 break;
	#         if not violation:
	#             bus.append(maxStudent)
	# 			numFriendsSorted.remove(maxStudent)
	# 			counter++
	# 		else:
	# 			numFriendsSorted.remove(maxStudent)
	# 			stillRowdy.append(maxStudent)
	# 	# when the bus is full, add it to our solution
	#     solution.append(bus)

#figure out what to do if you must make a rowdy group
	# solution.sort()
	# for bus in solution:





	#write solution list to a file
