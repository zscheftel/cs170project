solution = []
def solver(adjlist, k, s): #k = number of buses, s = capacity of buses
    #find kid w/ max # of friends

    numfriends = {}

    #supposed to sort the dictionary by the most number of friends
    for i in adjlist:
        key = i[0:3]
        value = (len[i] - 3)/4
        numfriends[key] = value
    numfriendssorted = sorted(numfriends, key = numfriends.get, reverse = True)
