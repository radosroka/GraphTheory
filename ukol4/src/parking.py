#!/usr/bin/python3

import sys
import time

def calcHungarian(producers, consumers):
    # matrix = [
    #     [9, 11, 14, 11, 7],
    #     [6, 15, 13, 13, 10],
    #     [12, 13, 6, 8, 8],
    #     [11, 9, 10, 12, 9],
    #     [7, 12, 14, 10, 14]
    # ]

    # matrix = [
    #     [2,3,4],
    #     [1,0,1],
    #     [2,1,2]
    # ]
    matrix = [ [0  for j in range(len(producers))] for i in range(len(consumers))]
    res = [ [False  for j in range(len(producers))] for i in range(len(consumers))]

    names  = []

    for p_idx, p in enumerate(producers):
        names.append([])
        for c_idx, c in enumerate(consumers):
            names[p_idx].append(p[0] + " " + c[0])

    rows = [False for item in matrix]
    cols = [False for item in matrix[0]]

    # calc euclidean distancies
    for p_idx, p in enumerate(producers):
        for c_idx, c in enumerate(consumers):
#            matrix[p_idx][c_idx] = math.sqrt((p[1][0] - c[1][0])**2 + (p[1][1] - c[1][1])**2)
             matrix[p_idx][c_idx] = abs((p[1][0] - c[1][0])) + abs((p[1][1] - c[1][1]))

    old_old_matrix = matrix

    def subMinFromRow(row):
        minn = min(row)
        for item in row:
            yield item - minn

    cycled = 0
    old_matrix = matrix
    while(True):

        # substract from rows
        matrix = list(map(lambda x: list(subMinFromRow(x)), matrix))

        # substract from columns
        numRows = len(matrix)
        numColumns = len(matrix[0])

        for idx_col in range(numColumns):
            minn = 10000000
            for idx_row in range(numRows):
                if matrix[idx_row][idx_col] < minn:
                    minn = matrix[idx_row][idx_col]

            for idx_row in range(numRows):
                matrix[idx_row][idx_col] -= minn

        # scan rows
        for r_idx,row in enumerate(matrix):
            if rows[r_idx]:
                continue
            indexesOfZero = [c_idx for c_idx,value in enumerate(row) if not cols[c_idx] and value == 0]

            if len(indexesOfZero) is 1:
                res[r_idx][indexesOfZero[0]] = True
                cols[indexesOfZero[0]] = True

        # scan columns
        for c_idx in range(numColumns):
            if cols[c_idx]:
                continue
            indexesOfZero = []
            for r_idx in range(numRows):
                if rows[r_idx]:
                    continue
                if matrix[r_idx][c_idx] is 0:
                    indexesOfZero.append(r_idx)

            if len(indexesOfZero) is 1:
                res[indexesOfZero[0]][c_idx] = True
                rows[indexesOfZero[0]] = True

        counter = 0
        for row in res:
            if True in row:
                counter += 1

        if counter is len(matrix):
            break

        # min of the rest
        minn = 100000
        for r_idx,row in enumerate(matrix):
            if rows[r_idx]:
                continue

            for c_idx,col in enumerate(row):
                if cols[c_idx]:
                    continue

                if matrix[r_idx][c_idx] < minn:
                    minn = matrix[r_idx][c_idx]

        for r_idx,row in enumerate(matrix):
            for c_idx,col in enumerate(row):

                if rows[r_idx] and cols[c_idx]:
                    matrix[r_idx][c_idx] += minn
                elif not rows[r_idx] and not cols[c_idx]:
                    matrix[r_idx][c_idx] -= minn

        if old_matrix == matrix:
            cycled += 1
        else:
            cycled = 0

        if cycled > 5:
            for r_idx,row in enumerate(matrix):
                if rows[r_idx]:
                    continue

                for c_idx,col in enumerate(row):
                    if cols[c_idx]:
                        continue

                    if matrix[r_idx][c_idx] == 0:
                        res[r_idx][c_idx] = True
                        cols[c_idx] = True
                        rows[r_idx] = True
                        break

        old_matrix = matrix


    return [old_old_matrix, res, names]


##### ----------------------------------------------------------------------------------


def main():

    lines = sys.stdin.read().splitlines()
    lines = [l for l in lines if l != ""]

    cars = []
    places = []


    for line in lines:
        first, second = line.split(": ")
        name, coords = first.split(" ")
        coords = coords.split(",")
        coords = [int(coords[0]), int(coords[1])]

        for i in range(int(second)):
            if name[0] is "B":
                cars.append([name + "_" + str(i+1), coords])
            else:
                places.append([name + "_" + str(i+1), coords])

    # print(cars)
    # print(places)

    result = calcHungarian(cars, places)
    overall = 0
    for r_idx, row in enumerate(result[0]):
        for c_idx, col in enumerate(row):
            if result[1][r_idx][c_idx]:
                overall += result[0][r_idx][c_idx]
                print(result[2][r_idx][c_idx], result[0][r_idx][c_idx])

    print("Celkem:", overall)


main()
