import random
from networkx import read_gml
import os, ast, sys
from pathlib import Path

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
    graph = read_gml(input_folder + "/graph.gml")
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

def randomSolve(G, k, s, rG):
    G.remove_edges_from(G.selfloop_edges())
    k = int(k)
    s = int(s)
    buses = []
    for i in range(k):
        buses.append([])
    openBuses = [bus for bus in buses if len(bus) < s]
    vertices = list(G.nodes)

    for i in range(k):
        index = random.choice(range(len(vertices)))
        randomV = vertices.pop(index)
        buses[i].append(randomV)

    for i in range(len(vertices)):
        random.shuffle(buses)
        j = 0
        while (len(buses[j]) >= s):
            j += 1
        buses[j].append(vertices[i])

    return buses

def isRowdy(bus):
    for rG_set in rG_sets: #check if a rowdy group is created
        if all(x in bus for x in rG_set):
            return list(rG_set)
    return []

p = os.getcwd()

# to test for different input sizes, just set the size you want to True
# eg. if I want to test the medium sized inputs, set only medium = True
small = True
iterations = 100
medium = False
large = False
total = 0
if small:
    inputsSize = "small/"
elif medium:
    inputsSize = "medium/"
elif large:
    inputsSize = "large/"

path = p + "/all_inputs/" + inputsSize
outputPath = p + "/outputs/" + inputsSize

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
            G = read_gml(src)

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
            solution = []
            score = 0

            for i in range(iterations):
                tempSolution = randomSolve(G, k, s, rG)
                createOutputs(outputPath, folder, tempSolution)
                tempScore = score_output(path + folder, outputPath + folder + ".out")[0]

                if tempScore > score:
                    score = tempScore
                    solution = tempSolution

            createOutputs(outputPath, folder, solution)
            print(score)
            total = total + score
print("small avg, ", total / 331)
# ***

small = False
iterations = 25
medium = True
large = False
total = 0
if small:
    inputsSize = "small/"
elif medium:
    inputsSize = "medium/"
elif large:
    inputsSize = "large/"

path = p + "/all_inputs/" + inputsSize
outputPath = p + "/outputs/" + inputsSize

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
            G = read_gml(src)

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
            solution = []
            score = 0

            for i in range(iterations):
                tempSolution = randomSolve(G, k, s, rG)
                createOutputs(outputPath, folder, tempSolution)
                tempScore = score_output(path + folder, outputPath + folder + ".out")[0]

                if tempScore > score:
                    score = tempScore
                    solution = tempSolution

            createOutputs(outputPath, folder, solution)
            print(score)
            total = total + score
print("med avg, ", total / 331)
# ***

small = False
iterations = 5
medium = False
large = True
total = 0
if small:
    inputsSize = "small/"
elif medium:
    inputsSize = "medium/"
elif large:
    inputsSize = "large/"

path = p + "/all_inputs/" + inputsSize
outputPath = p + "/outputs/" + inputsSize

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
            G = read_gml(src)

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
            solution = []
            score = 0

            for i in range(iterations):
                tempSolution = randomSolve(G, k, s, rG)
                createOutputs(outputPath, folder, tempSolution)
                tempScore = score_output(path + folder, outputPath + folder + ".out")[0]

                if tempScore > score:
                    score = tempScore
                    solution = tempSolution

            createOutputs(outputPath, folder, solution)
            print(score)
            total = total + score
print("large avg, ", total / 331)
