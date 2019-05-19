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

            if len(e) is not 3:
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

    def isSpanningTree(self):
        vertex_n = len(self.nodes)

        edges = 0
        for n in self.nodes.values():
            edges += len(n)

        #print(vertex_n, edges)
        return vertex_n -1 == edges

    def tryToSplit(self):
        if not self.isSpanningTree():
            nodes = list(self.nodes.keys())
            used = set()
            components = list()

            while(True):

                if len(nodes) == 0:
                    break

                group = [ nodes[0] ] + self.nodes[nodes[0]]
                group = set(group)
                nodes = nodes[1:]

                l = len(group)

#                print("IN:")
#                print(group)
#                print(nodes)
#                print()
                while(True):
                    for n in nodes:
                        if n in group:
                            group = group.union(set(self.nodes[n]))
                    if l == len(group):
                            break
                    l = len(group)

                used = used.union(group)
 #               print("used: ", used)
                nodes = [x for x in self.nodes.keys() if x not in used]
#                print(nodes)
                components.append(group)
#                print(components)

                if len(used) == len(self.nodes.keys()):
                    break

            ret = list()
            for nds in components:
                g = Graph()
                for n in nds:
                    g.nodes[n] = self.nodes[n]
                ret.append(g)
            return ret

        return [self]
##### ----------------------------------------------------------------------------------


def main():

    lines = sys.stdin.read().splitlines()

    lines = [l for l in lines if l != ""]

    relations = []
    for l in lines:
        x = l.split(": ")
        if len(x) != 2:
            raise Exception("Bad line", l)
        weight = x[1]
        relation = x[0].split(" - ")
        if len(relation) != 2:
            raise Exception("Bad line", l)
        relation.append(weight)
        relations.append(relation)

    g = Graph()
    g.loadNodes([ n for r in relations for n in r if not n.isnumeric() ])
    g.loadFromRelations(relations, oriented=True)


    graphs = g.tryToSplit()

    areOk = True
    for g in graphs:
        if not g.isSpanningTree():
            areOk = False

    print("Stav site", "OK" if areOk else "ERROR" )


main()
