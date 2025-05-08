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

    points = list(greens)
    unique_points = [START] + list(dict().fromkeys(points)) + [FINISH]

    labels = ["S"] + [chr(ord("a") + i) for i in range(len(unique_points) - 1)]
    point_to_label = {}
    for i in range(len(labels)):
        # print(unique_points[i])
        if unique_points[i] == (0, 0):
            point_to_label[unique_points[i]] = "S"
        else:
            point_to_label[unique_points[i]] = labels[i]

    label_to_point = {v: k for k, v in point_to_label.items()}

    # print(point_to_label)
    combinations = itertools.combinations(unique_points, 2)
    paths = {}

    for start, end in combinations:
        all_paths = []

        temp_board = deepcopy(board)
        solve(temp_board, [start], start, end, all_paths)
        path = findFastestPath(all_paths)
        paths[(point_to_label[start], point_to_label[end])] = (
            calculateTime(path),
            path,
        )
    # print(greens)
    green_labels = [point_to_label[p] for p in greens]
    # print("greenlabels %s" % (green_labels))
    best_time = float("inf")
    best_order = []

    for perm in itertools.permutations(green_labels):
        full_route = ["S"] + list(perm) + ["S"]
        # print(full_route)
        cost = calculateCost(full_route, paths)
        if cost < best_time:
            best_time = cost
            best_order = full_route

    full_path = []

    for i in range(len(best_order) - 1):
        a, b = best_order[i], best_order[i + 1]
        if (a, b) in paths:
            full_path += paths[(a, b)][1][:-1]
        else:
            full_path += paths[(b, a)][1][::-1][:-1]

    full_path.append(FINISH)

    # Cleanup duplicate consecutive steps
    cleanedPath = [full_path[0]]
    for i in range(1, len(full_path)):
        if full_path[i] != cleanedPath[-1]:
            cleanedPath.append(full_path[i])

    return cleanedPath


"""
board = initiatieboard(4, 6)
putGreens(board, [(2, 1), (1, 2), (3, 3), (1, 4), (0, 5), (3, 5)])
putReds(board, [(1, 0), (2, 2), (3, 2), (2, 3), (0, 4), (2, 5)])
oldBoard = deepcopy(board)
# print("ANS:")
path = compose(board, (0, 0), (0, 0))
# print(path)

display.displayBoardGUI(oldBoard)
"""
board = initiatieboard(4, 6)
putGreens(board, [(2, 1), (1, 2), (3, 3), (1, 4), (0, 5), (3, 5)])
putReds(board, [(1, 0), (2, 2), (3, 2), (2, 3), (0, 4), (2, 5)])

oldBoard = deepcopy(board)
path = compose(board, (0, 0), (0, 0))
print("Final path:", path)

display.displayBoardGUI(oldBoard, path)
