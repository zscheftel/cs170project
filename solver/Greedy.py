import networkx as nx
solution = []

def solver(G, k, s, L): #k = number of buses, s = capacity of buses, L = list of lists of rowdy groups
    #adjlist is a list of strings
    adjlist = nx.generate_adjlist(G)
    #find kid w/ max # of friends

    numFriends = {}
    stillRowdy = []

    #supposed to sort the dictionary by the most number of friends
    for i in adjlist:
        key = i[0:3]
        value = (len[i] - 3)/4
        numFriends[key] = value
    numFriendsSorted = sorted(numFriends, key = numFriends.get, reverse = True)


    #retrieve kid w/ max # of friends and keep adding until first bus full and then next bus
    for b in range(0, k):
        bus = []
        counter = 0
        while counter < s:
            tempRowdy = L.copy()
            violation = false
            # unideal, only gets students with most friends, not friends of friends
            maxStudent = numFriendsSorted.getKey(0)
            for rowdy in tempRowdy:
                rowdy.remove(maxStudent)
                if len(rowdy) == 0:
                    rowdy.add(maxStudent)
                    violation = true
                    break;
            if not violation:
                bus.append(maxStudent)
				numFriendsSorted.remove(maxStudent)
				counter++
			else:
				numFriendsSorted.remove(maxStudent)
				stillRowdy.append(maxStudent)
		# when the bus is full, add it to our solution
        solution.append(bus)

#figure out what to do if you must make a rowdy group
	solution.sort()
	for bus in solution:





    #write solution list to a file
