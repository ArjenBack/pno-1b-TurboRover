from helperFunctions import *


def main():
    actions = []
    with open("robot_actions.txt", "r") as file:
        for line in file:
            actions.append(line.strip())

    index = 0
    while index < len(actions):
        action = actions[index]

        print(f"Executing action: {action}")
        index += 1
