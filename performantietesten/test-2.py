from helperFunctions import *

MOTOR_LEFT.duty_cycle = int(0.3 * 65535)
MOTOR_RIGHT.duty_cycle = int(0.3 * 65535)

while True:
    if REAR_SWITCH.value:
        break
