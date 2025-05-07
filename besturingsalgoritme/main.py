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

    ledStatus = "default"

    while index < len(actions):
        action_split = actions[index].split()
        action = action_split[0]
        state = 0
        if "garage" in action_split:
            ledStatus = "blue"

        if action == "forward":
            statusLed(ledStatus)
            state = driveLine()
        elif action == "left":
            statusLed(ledStatus)
            state = turnLeft()
        elif action == "right":
            statusLed(ledStatus)
            state = turnRight()
        elif action == "pickup":
            statusLed("orange")
        #        pickUpTower()

        if state == 1:
            statusLed("red")
            index -= 1
            while True:
                if REAR_SWITCH.value:
                    break

        SERVO_MOTOR.angle = 145
        time.sleep(1)

        print(f"Executing action: {action_split}")
        index += 1

    statusLed("off")


while True:
    if REAR_SWITCH.value:
        pickUpTower(0.30)
