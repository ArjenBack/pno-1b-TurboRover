from helperFunctions import driveLine, turnLeft, turnRight, calibrate
import time


def testLine():
    N = 5
    totalTime = 0
    for _ in range(N):
        driveLine()
        print("ik ben dom en net gestopt")
        time.sleep(0.1)
        startTime = time.monotonic()
        state = driveLine()
        endTime = time.monotonic()
        totalTime += endTime - startTime

        test = input("Press Enter to continue...")
        print("diff: %s -> %s " % (_, endTime - startTime))

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


input("start calibrate")
MIN_LEFT, MAX_LEFT, MIN_RIGHT, MAX_RIGHT, MIN_REAR, MAX_REAR = calibrate()
input("start calibrate")
input("rommel")

testLine()
