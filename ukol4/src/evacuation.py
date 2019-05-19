#!/usr/bin/python3

import sys
from itertools import permutations
import copy
import math
import re


math.inf = float("inf")

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

            self.nodes[e[0]].append([ e[1], e[2] ])
            if not oriented:
                self.nodes[e[1]].append([ e[0], e[2] ])


        #print(self.nodes)


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

    def removeEdge(self, edge):
        self.nodes[edge[0]].remove([ edge[1], edge[2] ])

    def removeNode(self, node):
        self.nodes.pop(node)
        for value in self.nodes.values():
            for vvalue in value:
                if vvalue[0] == node:
                    value.remove(vvalue)

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

    def getSpanningTree(self):
        relations = [ [ n, nn[0], nn[1] ] for n,value in self.nodes.items() for nn in value ]
        result = list()

#        print(relations)
#        return

        while True:
            minn = ['', '', 10000000]
            for n in relations:
                if int(n[2]) < int(minn[2]):
                    minn = n

            result.append(minn[:])

            relations.remove(minn)

            g = Graph()
            g.loadNodes([ n for r in result for n in r if not n.isnumeric() ])
            g.loadFromRelations(result, oriented=True)

            if len(g.nodes) != len(self.nodes):
                if g.isSpanningTree():
                    continue
                else:
                    result.pop()
                    continue
            else:
                if g.isSpanningTree():
                    return result
                else:
                    return ["Erroooor"]

    def checkIfValid(self):
        suspicious = dict()
        for n,value in self.nodes.items():
            if not value:
                suspicious[n] = False

        for value in self.nodes.values():
            for key,vvalue in suspicious.items():
                if key in [ i[0] for i in value ]:
                    suspicious[key] = True

        for key,value in suspicious.items():
            if not value:
                return False

        return True

    def dijkstra(self):
        perms = dict()
        other = dict()

        perms["Vy"] = [ None, 0 ]

        for l in self.nodes["Vy"]:
            other[l[0]] = [ "Vy", l[1] ]

        for key,value in self.nodes.items():
            if key not in perms and key not in other:
                other[key] = [ None, math.inf ]

        while True:
            node_name = None
            node = [ None, math.inf ]

            for key,value in other.items():
                if float(node[1]) > float(value[1]):
                    node_name = key
                    node = value

            perms[node_name] = node
            other.pop(node_name)

            for l in self.nodes[node_name]:
                if l[0] in other:
                    if int(node[1]) + int(l[1]) < other[l[0]][1]:
                        other[l[0]] = [ node_name, int(node[1]) + int(l[1]) ]

            if len(other) is 0:
                break

        return perms

    def bellmanFord(self, start):
        flags = dict()

        flags[start] = [ 0, None, 0 ]

        for key,value in self.nodes.items():
            if key not in flags:
                flags[key] = [ 0, None, -math.inf ]

        #print(flags)

        k = 0
        while True:

            for name,value in self.nodes.items():
#                print(name, value)
#                print(flags[name])
#                print()
                if flags[name][0] is k:
                    for l in value:
#                        print("nas:", l)
#                        print(flags)
                        if float(flags[name][2]) + float(l[1]) > flags[l[0]][2]:
                            flags[l[0]][2] = float(flags[name][2]) + float(l[1])
                            flags[l[0]][1] = name
                            flags[l[0]][0] = flags[name][0] + 1
#                       print(flags)
#                print()
            k += 1

            if k == len(flags):
                break

        return flags

    def handleBonuses(self, bonus):

        for b in bonus:
            node = self.nodes[b]
            new_node = list()
            counter = 1
            for l in node:
                self.nodes["_" + b + str(counter)] = [ l ]
                new_node.append([ "_" + b + str(counter), 1 ])
                counter += 1
            self.nodes[b] = new_node



##### ----------------------------------------------------------------------------------


def main():

    lines = sys.stdin.read().splitlines()

    lines = [l for l in lines if l != ""]

    relations = []
    bonus = []
    START = None
    END = None

    for idx,l in enumerate(lines):
        x = l.split(": ")
        node = x[0]
        if node[-1] is "+":
            node = node[:-1]
            bonus.append(node)

        neighbours = x[1].split(", ")

        if idx == 0:
            START = node
        if idx == len(lines)-1:
            END = node

        for item in neighbours:
            tmp = item.split("(")
            name = tmp[0]
            weight = tmp[1][:-1]
            relations.append([node, name, weight])


    g = Graph()
    g.loadNodes([ n for r in relations for idx,n in enumerate(r) if idx < 2 ])
    g.loadFromRelations(relations, oriented=True)
    g.handleBonuses(bonus)

#    print("START:", START)
#    print("END:", END)
#    print("Bonus:", bonus)
#    print(g.nodes)

    result = g.bellmanFord(START)

    walk = []
    actual = END
    while True:
        walk = [actual] + walk
        actual = result[actual][1]
        if actual is None:
            break

    print(walk[0], end="")
    for item in walk[1:]:
        if not re.match(r"_\w+\d+", item):
            print(" -", item, end="")

    print(":", int(result[END][2]))

main()
