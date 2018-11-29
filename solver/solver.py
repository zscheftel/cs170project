import networkx as nx
from Greedy import solver
import os, ast, sys
from pathlib import Path
import matplotlib.pyplot as plt

p = os.getcwd()

# to test for different input sizes, just set the size you want to True
# eg. if I want to test the medium sized inputs, set only medium = True
small = False
medium = False
large = True

global counter
counter = 1

if small:
    inputsSize = "small/"
elif medium:
    inputsSize = "medium/"
elif large:
    inputsSize = "large/"

path = p + "/all_inputs/" + inputsSize
outputPath = p + "/outputs/" + inputsSize
# for testing purposes
# path = p + "/all_inputs/small/1/"

solution = []

#writes solution to output files
def createOutputs(filename, num, solution):
    f = open(filename + num + ".out", "w")
    for i in solution:
        f.write(str(i) + "\n")
    f.close()

def score_output(input_folder, output_file):
    '''
        Takes an input and an output and returns the score of the output on that input if valid
        
        Inputs:
            input_folder - a string representing the path to the input folder
            output_file - a string representing the path to the output file

        Outputs:
            (score, msg)
            score - a number between 0 and 1 which represents what fraction of friendships were maintained
            msg - a string which stores error messages in case the output file is not valid for the given input
    '''
    graph = nx.read_gml(input_folder + "/graph.gml")
    parameters = open(input_folder + "/parameters.txt")
    num_buses = int(parameters.readline())
    size_bus = int(parameters.readline())
    constraints = []

    for line in parameters:
        line = line[1: -2]
        curr_constraint = [node.replace("'","") for node in line.split(", ")]
        constraints.append(curr_constraint)

    output = open(output_file)
    assignments = []
    for line in output:
        line = line[1: -2]
        curr_assignment = [node.replace("'","") for node in line.split(", ")]
        assignments.append(curr_assignment)

    if len(assignments) != num_buses:
        return -1, "Must assign students to exactly {} buses, found {} buses".format(num_buses, len(assignments))
    
    # make sure no bus is empty or above capacity
    for i in range(len(assignments)):
        if len(assignments[i]) > size_bus:
            return -1, "Bus {} is above capacity".format(i)
        if len(assignments[i]) <= 0:
            return -1, "Bus {} is empty".format(i)
        
    bus_assignments = {}
    attendance_count = 0
        
    # make sure each student is in exactly one bus
    attendance = {student:False for student in graph.nodes()}
    for i in range(len(assignments)):
        if not all([student in graph for student in assignments[i]]):
            return -1, "Bus {} references a non-existant student: {}".format(i, assignments[i])

        for student in assignments[i]:
            # if a student appears more than once
            if attendance[student] == True:
                print(assignments[i])
                return -1, "{0} appears more than once in the bus assignments".format(student)
                
            attendance[student] = True
            bus_assignments[student] = i
    
    # make sure each student is accounted for
    if not all(attendance.values()):
        return -1, "Not all students have been assigned a bus"
    
    total_edges = graph.number_of_edges()
    # Remove nodes for rowdy groups which were not broken up
    for i in range(len(constraints)):
        busses = set()
        for student in constraints[i]:
            busses.add(bus_assignments[student])
        if len(busses) <= 1:
            for student in constraints[i]:
                if student in graph:
                    graph.remove_node(student)

    # score output
    score = 0
    for edge in graph.edges():
        if bus_assignments[edge[0]] == bus_assignments[edge[1]]:
            score += 1
    score = score / total_edges


    return score, "Valid output submitted with score: {}".format(score)

# if __name__ == '__main__':
#     score, msg = score_output(sys.argv[1], sys.argv[2])
#     print(msg)


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
            createOutputs(outputPath, folder, solution)

            #Print score for this solution
            # print(score_output(path + folder, outputPath + folder + ".out"))

            #Print counter of how many we've processed
            print(counter)
            counter += 1


# # FOR TESTING A SINGLE INPUT
# G = None
# k = None
# s = None
# rG = []
# for filename in os.listdir(path):
#     src = path + filename
#     if src.endswith(".gml"):
#         G = nx.read_gml(src)

#     if src.endswith(".txt"):
#         file = open(src, 'r')
#         lines = file.readlines()
#         k = lines[0]
#         s = lines[1]
#         # lines[2:] is a list of strings where the strings look like lists
#         # eg. ["[1, 2]", "[3, 4"]]
#         for group in lines[2:]:
#             # the below converts a string that looks like a list into an actual list
#             # eg. "[1, 2]" -> [1, 2]
#             group = ast.literal_eval(group)
#             rG.append(group)
#         file.close()
#     if G is not None and k is not None:
#         rG_sets = [set(x) for x in rG]

#         #Call solver function to write to solution global var
#         solution = solver(G, k, s, rG)

#         #Write output files based on solution
#         createOutputs(p + "/outputs", "1", solution, G)

#         #Print score for this solution
        # print(scoreSolution(G, rG_sets))
