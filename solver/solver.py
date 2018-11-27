import networkx as nx

path = "/../inputs/"

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

            #Call function, write output


def solver(G, k, s, rG):
