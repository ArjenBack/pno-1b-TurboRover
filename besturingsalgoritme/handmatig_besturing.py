import board
import time
import pwmio
import digitalio
from analogio import AnalogIn

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
MINIMUM_AFWIJKWAARDE_LINKS = 24000
MINIMUM_AFWIJKWAARDE_RECHTS = 8000
MINIMUM_AFWIJKWAARDE_ACHTER = 14000

def drive_forward(speed):
    motor_links.duty_cycle = 0
    motor_rechts.duty_cycle = 0
    relais_links.value = True
    time.sleep(0.1)
    relais_rechts.value = True
    motor_links.duty_cycle = int(speed * 65000)
    motor_rechts.duty_cycle = int(speed * 65000)

def drive_backward(speed):
    motor_links.duty_cycle = 0
    motor_rechts.duty_cycle = 0
    relais_links.value = False
    time.sleep(0.1)
    relais_rechts.value = False
    motor_links.duty_cycle = 30000
    motor_rechts.duty_cycle = 30000


def drive_line():
    crossroad_found = False

    LDR_links_value = LDR_links.value
    LDR_rechts_value = LDR_rechts.value
    LDR_achter_value = LDR_achter.value

    drive_forward(1)

    while not crossroad_found:
        time.sleep(0.1)
        prev_LDR_achter_value = LDR_achter_value
        LDR_links_value = LDR_links.value
        LDR_rechts_value = LDR_rechts.value
        LDR_achter_value = LDR_achter.value

        #print("links: %s, rechts: %s, diff: %s" %(LDR_links_value, LDR_rechts_value ,LDR_links_value - LDR_rechts_value))

        if LDR_links_value - LDR_rechts_value < -18000:
            motor_rechts.duty_cycle = 15000
            motor_links.duty_cycle = 30000
            print("links-afw")
        elif LDR_links_value - LDR_rechts_value > 18000:
            motor_links.duty_cycle = 15000
            motor_rechts.duty_cycle = 30000
            print("rechts-afw")
        elif abs(prev_LDR_achter_value - LDR_achter_value) > MINIMUM_AFWIJKWAARDE_ACHTER:
            crossroad_found = True
            motor_links.duty_cycle = 0
            motor_rechts.duty_cycle = 0
            print("crossroads")
        else:
            drive_forward(0.5)
            print("nothing detected")

drive_line()
