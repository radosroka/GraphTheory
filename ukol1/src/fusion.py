#!/usr/bin/python3

import sys

class Graph:
    nodes = None

    def __init__(self):
        self.nodes = dict()

    def loadNodes(self, nodes):
        for n in nodes:
            self.nodes[n] = set()


    def loadFromRelations(self, relations, oriented=False):
        for e in relations:

            if len(e) is not 2:
                raise Exception("This edge has not 2 nodes", e)

            self.nodes[e[0]].add(e[1])
            if not oriented:
                self.nodes[e[1]].add(e[0])

    def getNodesDegree(self):
        return [ [ name, len(followers) ] for name, followers in self.nodes.items() ]

    def merge(self, graph):
        externalNodes = list(map(lambda x : x.lower(), graph.nodes.keys()))
        externalNodesList = list(graph.nodes.values())
        internalNodes = list(map(lambda x : x.lower(), self.nodes.keys()))
        unused = dict()

        for index, value in enumerate(externalNodes):
            if value not in internalNodes:
                self.nodes[value] = externalNodesList[index]
            else:
                node = None
                for name, content  in self.nodes.items():
                    if name.lower() == value:
                        node = content
                        break

                lowerNodeList = list(map(lambda x : x.lower(), node))

                for name in externalNodesList[index]:
                    if name.lower() not in lowerNodeList:
                        node.add(name)
                    else:
                        g = list(graph.nodes.keys())
                        unused[g[index]] = name
        return unused





##### ----------------------------------------------------------------------------------


def main():

    lines = sys.stdin.read().splitlines()

    lines = [l for l in lines if l != ""]

    relations1 = list()
    relations2 = list()

    if len(lines) < 3:
        raise Exception("Non valid input")

    company1 = lines[0]
    company2 = lines[1]

    company1 = company1.split(", ")
    company2 = company2.split(", ")

    lines = lines[2:]

    for line in lines:
        nodes = line.split(" -> ")

        if len(nodes) is not 2:
            raise Exception("Edge has should have 2 nodes")

        if nodes[0].isupper() and nodes[1].isupper():
            relations1.append(nodes)
        elif nodes[0].islower() and nodes[1].islower():
            relations2.append(nodes)

    g1 = Graph()
    g1.loadNodes(company1)
    g1.loadFromRelations(relations1, oriented=True)

    g2 = Graph()
    g2.loadNodes(company2)
    g2.loadFromRelations(relations2, oriented=True)

    unused = g1.merge(g2);

    nodes = g1.nodes

    for name, content in nodes.items():
        for dest in content:
            print(name + " -> " + dest)

    print("----")

    for name, value in unused.items():
        print(name + " -> " + value)

main()
