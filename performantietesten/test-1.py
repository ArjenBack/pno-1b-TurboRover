from besturingsalgoritme.helperFunctions import driveLine, turnLeft, turnRight
import time


def testLine():
    N = 5
    totalTime = 0
    for _ in range(N):
        driveLine()
        startTime = time.monotonic()
        driveLine()
        endTime = time.monotonic()

        totalTime += endTime - startTime
        input("Press Enter to continue...")

    print(totalTime / N)


def testTurnLeft():
    N = 5
    totalTime = 0
    for _ in range(N):
        driveLine()
        startTime = time.monotonic()
        turnLeft()
        endTime = time.monotonic()

        totalTime += endTime - startTime
        input("Press Enter to continue...")

    print(totalTime / N)


def testTurnRight():
    N = 5
    totalTime = 0
    for _ in range(N):
        driveLine()
        startTime = time.monotonic()
        turnRight()
        endTime = time.monotonic()

        totalTime += endTime - startTime
        input("Press Enter to continue...")

    print(totalTime / N)


def testPickUp():
    N = 5
    totalTime = 0
    for _ in range(N):
        driveLine()
        startTime = time.monotonic()
        pickUp()
        endTime = time.monotonic()

        totalTime += endTime - startTime
        input("Press Enter to continue...")

    print(totalTime / N)
