from helperFunctions import *
import board
import math
import time
import pwmio
import digitalio
from analogio import AnalogIn
from adafruit_motor import servo


def main():
    actions = []
    with open("output.txt", "r") as file:
        for line in file:
            actions.append(line.strip())

    index = 0

    status = "default"

    while index < len(actions):
        action_split = actions[index].split()
        action = action_split[0]

        if "garage" in action_split:
            status = "blue"

        if action == "forward":
            statusLed(status)
            driveLine()
        elif action == "left":
            statusLed(status)
            turnLeft()
        elif action == "right":
            statusLed(status)
            turnRight()
        elif action == "pickup":
            statusLed("orange")
            pickUpTower()

        SERVO_MOTOR.angle = 145
        time.sleep(1)

        print(f"Executing action: {action_split}")
        index += 1

    statusLed("off")


while True:
    if REAR_SWITCH.value:
        break

main()
