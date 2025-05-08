def parse_output(path, greens, output_file="output.txt"):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    currentDirection = 0

    actions = []
    currentPos = path[0]
    for i in range(1, len(path)):
        action = ""
        nextPos = path[i]

        dx = nextPos[0] - currentPos[0]
        dy = nextPos[1] - currentPos[1]

        targetDirection = (dx, dy)

        targetIndex = directions.index(targetDirection)

        clockwiseSteps = (targetIndex - currentDirection) % 4
        counterClockwiseSteps = (currentDirection - targetIndex) % 4

        print(currentPos, nextPos, (dx, dy), clockwiseSteps, counterClockwiseSteps)
        if clockwiseSteps <= counterClockwiseSteps:
            for _ in range(clockwiseSteps):
                actions.append("right")
        else:
            for _ in range(counterClockwiseSteps):
                actions.append("left")

        currentDirection = targetIndex
        action += "forward"

        if nextPos in greens:
            action += " pickup"
            greens.remove(nextPos)

            if len(greens) == 0:
                action += " garage"

        currentPos = nextPos
        actions.append(action)

    with open(output_file, "w") as file:
        file.write("\n".join(actions))


parse_output(
    [
        (0, 0),
        (0, 1),
        (0, 2),
        (0, 3),
        (1, 3),
        (1, 4),
        (1, 5),
        (0, 5),
        (1, 5),
        (1, 4),
        (2, 4),
        (3, 4),
        (3, 3),
        (3, 4),
        (3, 5),
        (3, 4),
        (2, 4),
        (1, 4),
        (1, 3),
        (1, 2),
        (1, 1),
        (2, 1),
        (1, 1),
        (0, 1),
        (0, 0),
    ],
    [(1, 2), (1, 4), (0, 5), (3, 5), (3, 3), (2, 1)],
)
