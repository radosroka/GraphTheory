#!/usr/bin/python3

import sys

class AvlTree:

    class AvlItem:
        id = None
        right = None
        left = None
        value = None
        height = 1

        def __init__(self, number, id):
            self.value = number
            self.id = id

        def __repr__(self):
            return "<" + self.__str__() + ">"

        def __str__(self):
            return "Left: " + str(self.left) + " | ID: " + str(self.id) + " | Value: " + str(self.value) + " | High: " + str(self.height) +  " | Right: " + str(self.right)

    nodes = None
    root = None
    counter = 0

    def __init__(self):
        self.nodes = list()

    def __repr__(self):
        return "<" + self.__str__() + ">"

    def __str__(self):
        return str(self.nodes)

    def put(self, start_index, item):
        s = self.nodes[start_index]
 #       print("put:")
 #       print("value:", s.value)
 #       print("index:", start_index)
 #       print(item)
  #      print()


        if item.value >= s.value:
            if s.right is not None:
                res = self.put(s.right, item)
                if res is not None:
                    s.right = res
            else:
                s.right = self.nodes.index(item)

        else:
            if s.left is not None:
                res = self.put(s.left, item)
                if res is not None:
                    s.left = res
            else:
                s.left = self.nodes.index(item)

        #print(self)
        self.calcHeight(start_index)

        balance = self.calcBalance(start_index)

#        print("put:", balance)
#        print("put:", s)
#        print("put:", self)
#        print()
        if balance > 1 and item.value < self.nodes[s.left].value:
            return self.rightRotate(start_index)
        if balance < -1 and item.value > self.nodes[s.right].value:
            return self.leftRotate(start_index)
        if balance > 1 and item.calue > self.nodes[s.left].value:
            s.left = self.leftRotate(s.left)
            return self.rightRotate(start_index)
        if balance < -1 and item.value < self.nodes[s.right].value:
            s.right = self.rightRotate(s.right)
            return self.leftRotate(start_index)

    def leftRotate(self, start_index): # 1

        right = self.nodes[start_index].right # 4
        rLeft = self.nodes[right].left # None
        self.nodes[right].left = start_index
        self.nodes[start_index].right = rLeft
        self.calcHeight(start_index)
        self.calcHeight(right)

        return right

    def rightRotate(self, start_index): # 1

        left = self.nodes[start_index].left # None
        lRight = self.nodes[left].right # None
        self.nodes[left].right = start_index
        self.nodes[start_index].left = lRight
        self.calcHeight(start_index)
        self.calcHeight(left)

        return left


    def calcHeight(self, index):
        item = self.nodes[index]

        right = 0
        left = 0

        if item.right is not None:
            right = self.high_r(item.right)

        if item.left is not None:
            left = self.high_r(item.left)

        item.height = max([left,right]) + 1

    def calcBalance(self, index):
        item = self.nodes[index]

        right = 0
        left = 0

        if item.right is not None:
            right = self.high_r(item.right)

        if item.left is not None:
            left = self.high_r(item.left)

        return left - right

    def addNode(self, number):
        self.nodes.append(self.AvlItem(number, self.counter))
        self.counter += 1

        item = self.nodes[-1]
        index = self.nodes.index(item)

        if len(self.nodes) == 1:
            self.root = 0
            self.nodes[self.root].height = 1
            return

        self.put(self.root, item)

        max_height = 0
        max_index = 0
        for index, value in enumerate(self.nodes):
            if value.height > max_height:
                max_height = value.height
                max_index = index

        self.root = max_index



    def high_r(self, root):
        item = self.nodes[root]

        right = 0
        left = 0

        if item.right is not None:
            right = self.high_r(item.right)

        if item.left is not None:
            left = self.high_r(item.left)

        if right > left:
            return right + 1
        else:
            return left + 1

    def high(self):
        return self.high_r(self.root)

    def travel_r(self, root, level, max_level):

        item =  self.nodes[root]

        if level == max_level:
            print(self.nodes[item.left].value if item.left is not None else "_", end="")
            print(",", end="")
            print(self.nodes[item.right].value if item.right is not None else "_", end="")
            return [ item ]

        left = []
        if item.left is not None:
            left = self.travel_r(item.left, level + 1, max_level )

        print(",", end="")
        right = []
        if item.right is not None:
            right = self.travel_r(item.right, level + 1, max_level )

        result = left + right

#        print("return: ", result)
#        print()
        return result

    def travel(self):

        result = list()

        print(self.nodes[self.root].value, end="")
        for i in range(self.high()-1):
            print("|", end="")
            result += self.travel_r(self.root, 0, i)

        print()
        return result



##### ----------------------------------------------------------------------------------


def main():

    lines = sys.stdin.read().splitlines()

    lines = [l for l in lines if l != ""]

    numbers = [ int(n) for n in lines ]

    tree = AvlTree()
    for i in numbers:
        tree.addNode(i)
#        print(i)
        tree.travel()
#        print(tree)
 #       print()


main()
