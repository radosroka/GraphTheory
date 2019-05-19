#!/usr/bin/python3

import sys

class Graph:
    nodes = None
    edges = None

    def __init__(self):
        self.nodes = dict()

    def loadNodes(self, nodes):
        for n in nodes:
            self.nodes[n] = set()


    def loadFromRelations(self, relations):
        for e in relations:

            if len(e) is not 2:
                raise Exception("This edge has not 2 nodes", e)

            self.nodes[e[0]].add(e[1])
            self.nodes[e[1]].add(e[0])

    def getNodesDegree(self):
        return [ [name, len(followers) ] for name, followers in self.nodes.items() ]


##### ----------------------------------------------------------------------------------


names = list()
relations = list()

def main():

    lines = sys.stdin.read().splitlines()

    lines = [l for l in lines if l != ""]

    first = lines[0]
    names = first.split(", ")

    lines = lines[1:]

    for line in lines:
        relations.append(line.split(" - "))

    g = Graph()
    g.loadNodes(names)
    g.loadFromRelations(relations)
    nodes = g.getNodesDegree()

    nodes.sort(reverse = True, key = lambda x : x[1] )

    print("Task 1:")

    for n in nodes:
        print(n[0], "(" + str(n[1]) + ")")

    print()
    print("Task 2:")

    if len(nodes):
        maxx = nodes[0][1]
        l = [ n[0] for n in nodes if n[1] == maxx ]
        print(", ".join(l), "(" + str(maxx) + ")")


main()
