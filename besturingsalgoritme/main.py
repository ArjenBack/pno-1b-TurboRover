from helperFunctions import *


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
            if "pickup" in action_split:
                state = driveLine(
                    MIN_LEFT,
                    MAX_LEFT,
                    MIN_RIGHT,
                    MAX_RIGHT,
                    MIN_REAR,
                    MAX_REAR,
                    pickup=True,
                )
            else:
                state = driveLine(
                    MIN_LEFT,
                    MAX_LEFT,
                    MIN_RIGHT,
                    MAX_RIGHT,
                    MIN_REAR,
                    MAX_REAR,
                    pickup=False,
                )
        elif action == "left":
            statusLed(ledStatus)
            state = turnLeft(
                MIN_LEFT, MAX_LEFT, MIN_RIGHT, MAX_RIGHT, MIN_REAR, MAX_REAR
            )
        elif action == "right":
            statusLed(ledStatus)
            state = turnRight(
                MIN_LEFT, MAX_LEFT, MIN_RIGHT, MAX_RIGHT, MIN_REAR, MAX_REAR
            )
        if state == 1:
            statusLed("red")
            MOTOR_LEFT.duty_cycle = 0
            MOTOR_RIGHT.duty_cycle = 0
            index -= 1
            while True:
                if REAR_SWITCH.value:
                    break

        SERVO_MOTOR.angle = 180
        time.sleep(1)

        print(f"Executing action: {action_split}")
        index += 1

    statusLed("off")


while True:
    if REAR_SWITCH.value:
        print("first")
        break
time.sleep(1)
MIN_LEFT, MAX_LEFT, MIN_RIGHT, MAX_RIGHT, MIN_REAR, MAX_REAR = calibrate()
print("second")
time.sleep(1)
while True:
    if REAR_SWITCH.value:
        break

print("third")
