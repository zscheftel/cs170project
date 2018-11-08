solution = []
def solver(adjlist, k, s): #k = number of buses, s = capacity of buses
    #find kid w/ max # of friends
    friends = []
    for i in adjlist:
        friend = lst(i)
        friends.append(friend)

    numfriends = {}
    for i in adjlist:
        key = i[0:3]
        value = (len[i] - 3)/4
        numfriends[key] = value
    numfriendssorted = sorted(numfriends, key = numfriends.get)
