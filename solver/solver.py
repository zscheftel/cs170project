import networkx as nx

path = "/../inputs/"
solution = []

for folder in os.listdir(path):
    for filename in os.listdir(folder):
        G = None
        k = None
        s = None
        rG = []

        if filename.endswith(".gml"):
            G = nx.read_gml(filename)
        elif filename.endswith(".txt"):
            file = open(filename, 'r')
            lines = file.readlines()
            k = lines[0]
            s = lines[1]
            rG.extend(lines[2:])
            file.close()

        rG_sets = [set(x) for x in rG]

        #Call solver function to write to solution global var
        solver(G, k, s, rG)

        #Write output files based on solution
        createOuputs(filename)

        #Print score for this solution
        scoreSolution(G, rG_sets)

#writes solution to output files
def createOutputs(filename):
    f = open("small/" + filename + ".out", "w")
    for i in solution:
        f.write(str(i) + "\n")
    f.close()

#computes a score for a particular solution list ()
def scoreSolution(G, rG_sets):
    #initialize score
    score = 0

    #make adjlist in order to reference which kids are friends
    adjlist = nx.generate_adjlist(G)

    for bus in solution:
        rowdy = False
        for rG_set in rG_sets:
            if all(x in bus for x in rG_set):
                rowdy = True
                break
        if rowdy:
            break
        else:
            for i in range(len(bus)):
                for j in range(i, len(bus)):
                    for friends in adjlist:
                        if str(i) in friends and str(j) in friends:
                            score += 1
                            
    print(score)
