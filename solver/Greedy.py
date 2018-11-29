import networkx as nx
import queue as Q

solution = []
buses = []
currBus #counter for which bus you're currently trying to add to
adjlist = nx.generate_adjlist(G) #adjlist is a list of strings

#calculate how many friends student1 has in the current bus
def findFriendsOnCurrentBus(student1):
    friendsOnBus = 0
    for student2 in buses[currBus]:
        for list in adjlist:
            if (list.split(' ')[0] == student1) and (student2 in list):
                friendsOnBus += 1
    return friendsOnBus

#iterate through priority queue and dictionary and basically update everything whenever
#a student is successfully added to a bus
def updatePriorities():


#overall solver
def solver(G, k, s, L):
    #initialize buses list
    for i in range(0, k):
        bus = []
        buses.append(bus)
    currBus = 0 #initialize currBus counter to start at 0

    #initialize priorityDict to be key = name, value = priority heuristic
    priorityDict = {}
    for list in adjlist:
        key = list.split(' ')[0]
        #all of the following are needed to calculate the priority
        friendsInGraph = len(list.split(' ')) - 1 #total number of friends remaining in the Graph
        friendsOnCurrentBus = findFriendsOnCurrentBus(key)
        spotsRemaining = s - len(buses[currBus])
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

    #iterate through until PQ is empty, each time adding the max student either to a bus or to "stillRowdy"
    while not PQ.empty():
        maxStudent = PQ.get() #retrieve max student from PQ, also removes this student from the PQ

















def solver(G, k, s, L): #k = number of buses, s = capacity of buses, L = list of lists of rowdy groups
    #adjlist is a list of strings
    adjlist = nx.generate_adjlist(G)
    #find kid w/ max # of friends

    numFriends = {}
    stillRowdy = []
    buses = []

    #initialize buses list
    for i in range(0, k):
        bus = []
        buses.append(bus)

    #supposed to sort the dictionary by the most number of friends
    for i in adjlist:
        key = i[0:3]
        value = (len[i] - 3)/4
        numFriends[key] = value
    numFriendsSorted = sorted(numFriends, key = numFriends.get, reverse = True)

    #retrieve kid w/ max # of friends and keep adding until first bus full and then next bus
    #unless adding the max kid creatse a rowdy group: else iterate through next buses, keep trying

    for i in range(len(buses)):
        bus = buses[i]
        while len(bus) < s:
            inBus = False
            tempRowdy = L.copy()
            violation = False
            maxStudent = numFriendsSorted.getKey(0)
            #check if adding will form a rowdy group
            for rowdy in tempRowdy:
                rowdy.remove(maxStudent)
                if len(rowdy) == 0:
                    rowdy.add(maxStudent)
                    violation = True
                    break
            if not violation:
                bus.append(maxStudent)
				numFriendsSorted.remove(maxStudent)
                inBus = True
            else:
                violation = False
                #for each additional bus, check if forms rowdy group
                for j in range(i, len(buses)):
                    for rowdy in tempRowdy:
                        rowdy.remove(maxStudent)
                        if len(rowdy) == 0 or len(bus) == s:
                            rowdy.add(maxStudent)
                            violation = True
                            break
                    if not violation:
                        bus.append(maxStudent)
        				numFriendsSorted.remove(maxStudent)
                        inBus = True
                    else:
                        stillRowdy.append(maxStudent)
                        continue
                if not inBus:
                    stillRowdy.append(maxStudent)




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
	solution.sort()
	for bus in solution:





    #write solution list to a file
