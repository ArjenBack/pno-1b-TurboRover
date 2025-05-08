#! /bin/python3

################
# Fastest path #
################


import display
from copy import deepcopy
import itertools

TIMESTRAIGHT = 3
TIMETURN = 4


def initiatieboard(nbRows, nbCols):
    """
    Deze functie maakt een bord aan met nbRows rijen en nbCols kolommen. Normaalgezien ga je hiermee een
    rooster van 4 rijen en 6 kolommen aanmaken.
    """

    board = []

    for row in range(nbRows):
        board.append([])
        for col in range(nbCols):
            board[row].append(0)

    return board


def putGreens(board, greens):
    """
    Deze functie duidt een groene, dus op te pikken schijf, aan op positie (x,y) op het bord met de naam board.
    """
    for green in greens:
        putGreen(board, green[0], green[1])


def putGreen(board, x, y):
    """
    Deze functie duidt een groene, dus op te pikken schijf, aan op positie (x,y) op het bord met de naam board.
    """
    board[x][y] = 1
    return board


def putReds(board, reds):
    for red in reds:
        putRed(board, red[0], red[1])


def putRed(board, x, y):
    """
    Deze functie duidt een rode, dus te vermijden schijf, aan op positie (x,y) op het rooster met de naam board.
    """
    board[x][y] = 2


def getGreens(board):
    """
    Deze functie geeft een set terug met de posities van alle groene schijfjes van het bord.
    """
    greens = []

    for x, row in enumerate(board):
        for y, cell in enumerate(row):
            if cell == 1:
                greens.append((x, y))

    return greens


def getReds(board):
    """
    Deze functie geeft een set terug met de posities van alle rode schijfjes van het bord.
    """
    reds = []

    for x, row in enumerate(board):
        for y, cell in enumerate(row):
            if cell == 2:
                reds.append((x, y))

    return reds


def getLegalNeighbours(board, pos):
    """
    Deze functie geeft een set terug met alle toegestane posities waar een wagentje naartoe kan bewegen vanuit
    de gegeven positie pos. De functie houdt daarbij rekening met de randen van het bord en de posities waar er
    zich een rood schijfje bevindt.
    """
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    newPositions = []

    for move in moves:
        newPos = (pos[0] + move[0], pos[1] + move[1])
        if (
            newPos[0] >= 0
            and newPos[1] >= 0
            and newPos[0] < len(board)
            and newPos[1] < len(board[0])
            and board[newPos[0]][newPos[1]] != 2
        ):
            newPositions.append(newPos)

    return newPositions


def calculateTime(route):
    """
    Deze functie berekent de tijd die het wagentje nodig heeft om een gegeven route te rijden. De functie ge-
    bruikt hiervoor de constanten TIMESTRAIGHT en TIMETURN, respectievelijk de tijd die nodig is om één
    roosterpunt vooruit te gaan of ter plekke één bocht van 90° te maken.
    """
    time = 0
    prevDirection = "up"
    string = ""

    for i in range(len(route) - 1):
        dx = route[i + 1][0] - route[i][0]
        dy = route[i + 1][1] - route[i][1]

        if dx == -1:
            direction = "left"
        elif dx == 1:
            direction = "right"
        elif dy == 1:
            direction = "up"
        elif dy == -1:
            direction = "down"
        else:
            direction = ""

        if prevDirection == direction:
            time += TIMESTRAIGHT
            string += "S"
        elif prevDirection in ["up", "down"] and direction in ["up", "down"]:
            time += TIMETURN * 2
            string += "TT"
            time += TIMESTRAIGHT
            string += "S"
        elif prevDirection in ["left", "right"] and direction in ["left", "right"]:
            time += TIMETURN * 2
            string += "TT"
            time += TIMESTRAIGHT
            string += "S"
        else:
            time += TIMETURN
            string += "T"
            time += TIMESTRAIGHT
            string += "S"

        prevDirection = direction

    return time


def displayBoard(board):
    """
    Deze functie print het bord op het scherm.
    """
    for row in board:
        print(" ".join(str(cell) for cell in row))


ABANDON = "ABANDON"
ACCEPT = "ACCEPT"
CONTINUE = "CONTINUE"
BEZOCHT = -1


def examine(board, path, start, end):
    if (
        all(red not in path for red in getReds(board))
        and path[0] == start
        and path[-1] == end
    ):
        return ACCEPT
    elif path[-1] in getReds(board):
        return ABANDON
    else:
        return CONTINUE


def solve(board, path, start, end, allPaths):
    exam = examine(board, path, start, end)
    if exam == ACCEPT:
        allPaths.append(path[:])
        path = [start]
    elif exam != ABANDON:
        for neighbor in getLegalNeighbours(board, path[-1]):
            if board[neighbor[0]][neighbor[1]] != BEZOCHT:
                originalValue = board[neighbor[0]][neighbor[1]]
                board[neighbor[0]][neighbor[1]] = BEZOCHT
                newpath = path + [neighbor]
                result = solve(board, newpath, start, end, allPaths)
                board[neighbor[0]][neighbor[1]] = originalValue
                if result is not None:
                    return result


def findFastestPath(paths):
    bestTime = float("inf")
    bestPath = []
    for path in paths:
        time = calculateTime(path)
        if time < bestTime:
            bestTime = time
            bestPath = path
    return bestPath


def calculateCost(permutation, paths):
    totalCost = 0

    n = len(permutation)

    for i in range(n):
        current = permutation[i]
        next = permutation[(i + 1) % n]

        if (current, next) in paths:
            totalCost += paths[(current, next)][0]
        else:
            totalCost += paths[(next, current)][0]

    return totalCost


def compose(board, START, FINISH):
    greens = getGreens(board)
    if START == FINISH:
        greens += [START]
    else:
        greens += [START, FINISH]

    combinations = itertools.combinations(greens, 2)

    paths = {}
    alph = [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
    ]
    for start, end in combinations:
        allPaths = []
        solve(board, [start], start, end, allPaths)
        path = findFastestPath(allPaths)
        paths[(alph[greens.index(start)], alph[greens.index(end)])] = (
            calculateTime(path),
            path,
        )

    permutations = itertools.permutations(alph[0 : len(greens)])

    bestTime = float("inf")
    bestPath = []

    for permutation in permutations:
        cost = calculateCost(permutation, paths)
        if cost < bestTime:
            bestTime = cost
            bestPath = permutation
    print(bestPath)
    fullPath = []

    for i in range(len(bestPath) - 1):
        start = bestPath[i]
        end = bestPath[i + 1]
        if (start, end) in paths:
            print(paths[(start, end)])
            fullPath += paths[(start, end)][1]
        else:
            print(paths[(end, start)])
            fullPath += paths[(end, start)][1][::-1]

    sweepedPath = [START]
    for i in range(len(fullPath) - 2):
        if fullPath[i] != fullPath[i + 1]:
            sweepedPath.append(fullPath[i])
    sweepedPath.append(fullPath[len(fullPath) - 2])
    sweepedPath.append(FINISH)
    return sweepedPath


board = initiatieboard(4, 6)
putGreens(board, [(2, 1), (1, 2), (3, 3), (1, 4), (0, 5), (3, 5)])
putReds(board, [(1, 0), (2, 2), (3, 2), (2, 3), (0, 4), (2, 5)])
oldBoard = deepcopy(board)
print("ANS:")
path = compose(board, (0, 0), (0, 0))
print(path)

display.displayBoardGUI(oldBoard)
"""
board = initiatieboard(4, 6)
putGreens(board, [(1, 0), (3, 0), (2, 4), (3, 4)])
putReds(board, [(2, 0), (3, 3)])
oldBoard = deepcopy(board)
path = compose(board, (0, 0), (0, 0))

print(path)

display.displayBoardGUI(oldBoard, path)
"""
