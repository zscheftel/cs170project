import networkx as nx
solution = []
def solver(G, k, s, L): #k = number of buses, s = capacity of buses
    adjlist = nx.generate_adjlist(G)
    #find kid w/ max # of friends

    numfriends = {}

    #supposed to sort the dictionary by the most number of friends
    for i in adjlist:
        key = i[0:3]
        value = (len[i] - 3)/4
        numfriends[key] = value
    numfriendssorted = sorted(numfriends, key = numfriends.get, reverse = True)

    #retrieve kid w/ max # of friends and keep adding until first bus full and then next bus
    for k in range(0, k):
        for s in range(0, s):
            if numfriendssorted is not empty and



    #write solution list to a file
