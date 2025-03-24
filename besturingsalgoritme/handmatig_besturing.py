import board
import time
import pwmio
import digitalio
from analogio import AnalogIn

from besturingsalgoritme.besturingsalgoritme import MINIMUM_AFWIJKWAARDE_LINKS

### Defineren van de pinnen

# LDR-s
LDR_links = AnalogIn(board.GP27)
LDR_rechts = AnalogIn(board.GP28)
LDR_achter = AnalogIn(board.GP26)

# Motoren
motor_links =  pwmio.PWMOut(board.GP1)
motor_rechts = pwmio.PWMOut(board.GP0)

relais_links = digitalio.DigitalInOut(board.GP3)
relais_links.direction = digitalio.Direction.OUTPUT
relais_links.value = False

relais_rechts = digitalio.DigitalInOut(board.GP2)
relais_rechts.direction = digitalio.Direction.OUTPUT
relais_rechts.value = False

# Gevoeligheden
MINIMUM_AFWIJKWAARDE_LINKS = 11000
MINIMUM_AFWIJKWAARDE_RECHTS = 8000
MINIMUM_AFWIJKWAARDE_ACHTER = 14000

def drive_forward(speed):
    motor_links.duty_cycle = 0
    motor_rechts.duty_cycle = 0
    time.sleep(0.1)
    relais_links.Value = True
    relais_rechts.Value = True
    motor_links.duty_cycle = speed * 65000
    motor_rechts.duty_cycle = speed * 65000

def drive_backward(speed):
    motor_links.duty_cycle = 0
    motor_rechts.duty_cycle = 0
    time.sleep(0.1)
    relais_links.Value = False
    relais_rechts.Value = False
    motor_links.duty_cycle = speed * 65000
    motor_rechts.duty_cycle = speed * 65000


def drive_line():
    crossroad_found = False

    LDR_links_value = LDR_links.value
    LDR_rechts_value = LDR_rechts.value
    LDR_achter_value = LDR_achter.value

    while not crossroad_found:
        prev_LDR_link_value = LDR_links_value
        prev_LDR_rechts_value = LDR_rechts_value
        prev_LDR_achter_value = LDR_achter_value

        LDR_links_value = LDR_links.value
        LDR_rechts_value = LDR_rechts.value
        LDR_achter_value = LDR_achter.value

        if abs(prev_LDR_link_value - LDR_links_value) < MINIMUM_AFWIJKWAARDE_LINKS:
            motor_links.duty_cycle = int(motor_links.duty_cycle / 2)
        elif abs(prev_LDR_rechts_value - LDR_rechts_value) < MINIMUM_AFWIJKWAARDE_RECHTS:
            motor_rechts.duty_cycle = int(motor_rechts.duty_cycle / 2)
        elif abs(prev_LDR_achter_value - LDR_achter_value) < MINIMUM_AFWIJKWAARDE_ACHTER:
            crossroad_found = True
        else:
            drive_forward(1)
