#!/usr/bin/python3

import sys
from itertools import permutations

class Graph:
    nodes = None

    def __init__(self):
        self.nodes = dict()

    def loadNodes(self, nodes):
        for n in nodes:
            self.nodes[n] = list()

    def calcEdges(self):
        count = 0
        for l in self.nodes.items():
            count += len(l[1])
        return count


    def loadFromRelations(self, relations, oriented=False):
        for e in relations:

            if len(e) is not 2:
                raise Exception("This edge has not 2 nodes", e)

            self.nodes[e[0]].append(e[1])
            if not oriented:
                self.nodes[e[1]].append(e[0])

    def getNodesDegree(self):
        return [ [name, len(followers) ] for name, followers in self.nodes.items() ]

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

    def compareNodes(self, graph):
        return len(self.nodes) == len(graph.nodes)

    def compareEdges(self, graph):
        return self.calcEdges() == graph.calcEdges()

    def compareNodesDegrees(self, graph):
        x = [ num[1] for num in self.getNodesDegree() ]
        y = [ num[1] for num in graph.getNodesDegree() ]
        return sorted(x, reverse=True) == sorted(y, reverse=True)

    def findPossibleAlignments(self, graph):
        perms = list(permutations(list(graph.nodes.keys())))
        flags = [ True for _ in range(len(perms)) ]

        for idx_perms,perm in enumerate(perms):
            translate = dict(zip(self.nodes.keys(), perm))
            for idx,item in enumerate(self.nodes.items()):
                for node in item[1]:
                    if translate[node] not in graph.nodes[perm[idx]]:
                        flags[idx_perms] = False
                        break
                if not flags[idx_perms]:
                    break

        return [ perm for idx,perm in enumerate(perms) if flags[idx] ]

    def checkNodeDegreesForAlign(self, graph):
        perms = list(permutations(list(graph.nodes.keys())))
        flags = [ True for _ in range(len(perms)) ]

        for idx_perms,perm in enumerate(perms):
            for idx,item in enumerate(self.nodes.items()):
                if len(item[1]) is not len(graph.nodes[perm[idx]]):
                    flags[idx_perms] = False
                    break

        return [ perm for idx,perm in enumerate(perms) if flags[idx] ]

    def checkNeighboursForAlign(self, graph):
        perms = list(permutations(list(graph.nodes.keys())))
        flags = [ True for _ in range(len(perms)) ]

        for idx_perms,perm in enumerate(perms):
            translate = dict(zip(self.nodes.keys(), perm))
            for idx,item in enumerate(self.nodes.items()):
                translated = list(map(lambda x : translate[x], item[1]))
                if translated != graph.nodes[perm[idx]]:
#                    print(item[1])
#                    print(translated)
#                    print(graph.nodes[perm[idx]])
#                    print("")
                    flags[idx_perms] = False
                    break

        return [ perm for idx,perm in enumerate(perms) if flags[idx] ]


##### ----------------------------------------------------------------------------------


def main():

    lines = sys.stdin.read().splitlines()

    lines = [l for l in lines if l != ""]

    if len(lines) > 2:
        raise Exception("Too many lines in input")
    if len(lines) < 2:
        raise Exception("Too few lines in input")


    l1 = lines[0]
    l2 = lines[1]

    l1 = [ double.split("-") for double in l1.split(",") ]
    l2 = [ double.split("-") for double in l2.split(",") ]

#    print(l1)
#    print(l2)

    g1 = Graph()
    g1.loadNodes([ node for sub in l1 for node in sub ] )
    g1.loadFromRelations(l1)

    g2 = Graph()
    g2.loadNodes([ node for sub in l2 for node in sub ] )
    g2.loadFromRelations(l2)

#    print(g1.nodes)
#    print(g2.nodes)

    print("* |U1| = |U2|:", "true" if g1.compareNodes(g2) else "false")
    print("* |H1| = |H2|:", "true" if g1.compareEdges(g2) else "false")

    align = list()
    if g1.compareNodesDegrees(g2):
        align = g1.findPossibleAlignments(g2)

    print("* Jsou-li u, v sousední uzly, pak i (u), (v) jsou sousední uzly:", "true" if len(align) else "false")
    print("* Grafy mají stejnou posloupnost stupňů uzlů:",
          "true" if g1.compareNodesDegrees(g2) else "false")
    print("* Pak pro každý uzel v z U platí")

    #print(g1.checkNodeDegreesForAlign(g2))
    print(" – stupeň uzlu v je roven stupni uzlu φ(v):", "true" if g1.checkNodeDegreesForAlign(g2) else "false")
    ###print(g1.checkNeighboursForAlign(g2))
    print(" – množina stupňů sousedů uzlu v je rovna množině stupňů sousedů uzlu φ(v):", "true" if g1.checkNeighboursForAlign(g2) else "false")



main()
