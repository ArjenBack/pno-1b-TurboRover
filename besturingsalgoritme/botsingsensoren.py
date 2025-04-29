import time
import digitalio
import board

frontSwitch = digitalio.DigitalInOut(board.GP22)
frontSwitch.direction = digitalio.Direction.INPUT

leftSwitch = digitalio.DigitalInOut(board.GP19)
leftSwitch.direction = digitalio.Direction.INPUT

backSwitch = digitalio.DigitalInOut(board.GP18)
backSwitch.direction = digitalio.Direction.INPUT

rightSwitch = digitalio.DigitalInOut(board.GP0)
rightSwitch.direction = digitalio.Direction.INPUT

while True:
    if frontSwitch.value:
        print("front")

    if leftSwitch.value:
        print("left")

    if rightSwitch.value:
        print("right")

    if backSwitch.value:
        print("back")

    time.sleep(0.1)

# GP21 -> achter
# GP20 -> left
