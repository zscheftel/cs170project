import networkx as nx
from Greedy import solver
import os
from pathlib import Path

path = "/Users/maxyun/Documents/cs170/project/all_inputs/small/"
solution = []


#writes solution to output files
def createOutputs(filename, num, solution):
    f = open(filename + "/" + num + ".out", "w")
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

for folder in os.listdir(path):
    if folder.endswith(".DS_Store"):
        continue
    for filename in os.listdir(path + folder):
        G = None
        k = None
        s = None
        rG = []

        src = path + folder + "/" + filename

        if src.endswith(".gml"):
            G = nx.read_gml(src)
        elif src.endswith(".txt"):
            file = open(src, 'r')
            lines = file.readlines()
            k = lines[0]
            s = lines[1]
            rG.extend(lines[2:])
            file.close()

        if G is not None and k is not None:
            print("hi")
            rG_sets = [set(x) for x in rG]

            #Call solver function to write to solution global var
            solution = solver(G, k, s, rG)

            #Write output files based on solution
            createOutputs(os.getcwd() + "/outputs", folder, solution)

            #Print score for this solution
            scoreSolution(G, rG_sets)
