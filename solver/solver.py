import networkx as nx
from zackFunction import solver
import os
from pathlib import Path
import ast

path = "/Users/Gabrielle/Documents/cs170/all_inputs/small/"
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

for folder in os.listdir(path):
    if folder.endswith(".DS_Store"):
        continue
    G = None
    k = None
    s = None
    rG = []
    for filename in os.listdir(path + folder):
        src = path + folder + "/" + filename
        if src.endswith(".gml"):
            G = nx.read_gml(src)

        if src.endswith(".txt"):
            file = open(src, 'r')
            lines = file.readlines()
            k = lines[0]
            s = lines[1]
            # lines[2:] is a list of strings where the strings look like lists
            # eg. ["[1, 2]", "[3, 4"]]
            for group in lines[2:]:
                # the below converts a string that looks like a list into an actual list
                # eg. "[1, 2]" -> [1, 2]
                group = ast.literal_eval(group)
                rG.append(group)
            file.close()
        if G is not None and k is not None:
            rG_sets = [set(x) for x in rG]

            #Call solver function to write to solution global var
            solution = solver(G, k, s, rG)

            #Write output files based on solution
            createOutputs(os.getcwd() + "/outputs", folder, solution)

            #Print score for this solution
            scoreSolution(G, rG_sets)
