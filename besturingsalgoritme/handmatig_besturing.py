import board
import time
import pwmio
import digitalio
import statusled as RGB
from analogio import AnalogIn
<<<<<<< HEAD
import random
=======
from adafruit_motor import servo

>>>>>>> 850643582d6a7ae8df73fa8a50c2d68d3ae9416e

### Defineren van de pinnen

# LDR-s
LDR_links = AnalogIn(board.GP27)
LDR_rechts = AnalogIn(board.GP28)
LDR_achter = AnalogIn(board.GP26)

# Motoren
motor_links = pwmio.PWMOut(board.GP1)
motor_rechts = pwmio.PWMOut(board.GP0)

relais_links = digitalio.DigitalInOut(board.GP3)
relais_links.direction = digitalio.Direction.OUTPUT
relais_links.value = False

relais_rechts = digitalio.DigitalInOut(board.GP2)
relais_rechts.direction = digitalio.Direction.OUTPUT
relais_rechts.value = False

# Servo-motor

servo_PWM = pwmio.PWMOut(board.GP5, duty_cycle = 2 ** 15, frequency = 50)
servo_motor = servo.Servo(servo_PWM)

# Gevoeligheden
MINIMUM_AFWIJKWAARDE_LINKS = 24000
MINIMUM_AFWIJKWAARDE_RECHTS = 8000
MINIMUM_AFWIJKWAARDE_ACHTER = 14000


def drive_forward(speed):
    motor_links.duty_cycle = 0
    motor_rechts.duty_cycle = 0

    relais_links.value = True
    relais_rechts.value = True

    motor_links.duty_cycle = int(speed * 65000)
    motor_rechts.duty_cycle = int(speed * 65000)


def drive_backward(speed):
    motor_links.duty_cycle = 0
    motor_rechts.duty_cycle = 0
    RGB.status_led("red") #RGB kleurt rood volgens aan-uit-cyclus
    relais_links.value = False
    time.sleep(0.1)
    relais_rechts.value = False
    motor_links.duty_cycle = 30000
    motor_rechts.duty_cycle = 30000


def drive_line():
    crossroad_found = False

    # Initialize LDR values
    LDR_links_value = LDR_links.value
    LDR_rechts_value = LDR_rechts.value
    LDR_achter_value = LDR_achter.value

    drive_forward(0.5)

    while not crossroad_found:
        RGB.status_led("default")  # Laat RGB-LED afwisselend wit-groen branden
        time.sleep(0.1)

        # Behoud vorige waarde
        prev_LDR_achter_value = LDR_achter_value

        # Update LDR waarde
        LDR_links_value = LDR_links.value
        LDR_rechts_value = LDR_rechts.value
        LDR_achter_value = LDR_achter.value

        print("ACHTER: prev %s, current: %s, diff: %s" % (prev_LDR_achter_value, LDR_achter_value, abs(prev_LDR_achter_value - LDR_achter_value)))
        # aanpassing links
        if LDR_links_value - LDR_rechts_value < -18000:
            motor_rechts.duty_cycle = 30000
            motor_links.duty_cycle = 60000

        # aanpassing rechts
        elif LDR_links_value - LDR_rechts_value > 18000:
            motor_links.duty_cycle = 30000
            motor_rechts.duty_cycle = 60000

        # Zet motoren gelijk
        else:
            drive_forward(0.5)

        # kruispunt stop
        if abs(prev_LDR_achter_value - LDR_achter_value) > MINIMUM_AFWIJKWAARDE_ACHTER:
            print("Klaar om te draaien, waar zijn die handjes")
            crossroad_found = True
            motor_links.duty_cycle = 0
            motor_rechts.duty_cycle = 0
            pick_up_torentje()
            print("Torentje wordt opgepakt...")
            RGB.status_led("orange") #Laat RGB-LED oranje branden volgens aan-uit-cyclus



def turn_left():

    motor_links.duty_cycle = 0
    motor_rechts.duty_cycle = 0

    relais_links.value = False
    relais_rechts.value = True

    motor_links.duty_cycle = 15000
    motor_rechts.duty_cycle = 15000

    LDR_links_value = LDR_links.value
    LDR_rechts_value = LDR_rechts.value
    LDR_achter_value = LDR_achter.value

    ref = time.monotonic()
    black_found = False

    while True:

        time.sleep(0.05)
        prev_LDR_achter_value = LDR_achter_value
        prev_LDR_links_value = LDR_links_value
        prev_LDR_rechts_value = LDR_rechts_value

        LDR_links_value = LDR_links.value
        LDR_rechts_value = LDR_rechts.value
        LDR_achter_value = LDR_achter.value

        if black_found and LDR_links_value - LDR_rechts_value < -16000 and time.monotonic() > (ref + 0.5):
            motor_links.duty_cycle = 0
            motor_rechts.duty_cycle = 0
            break

        if LDR_links_value - LDR_rechts_value < -18000:
            black_found = True

def turn_right():
    motor_links.duty_cycle = 0
    motor_rechts.duty_cycle = 0
    relais_links.value = True
    relais_rechts.value = False
    motor_links.duty_cycle = 15000
    motor_rechts.duty_cycle = 15000
    LDR_links_value = LDR_links.value
    LDR_rechts_value = LDR_rechts.value
    LDR_achter_value = LDR_achter.value

    ref = time.monotonic()
    black_found = False
    while True:

        time.sleep(0.05)
        prev_LDR_achter_value = LDR_achter_value
        prev_LDR_links_value = LDR_links_value
        prev_LDR_rechts_value = LDR_rechts_value

        LDR_links_value = LDR_links.value
        LDR_rechts_value = LDR_rechts.value
        LDR_achter_value = LDR_achter.value

        print(
            "links: %s, rechts: %s, diff: %s" % (LDR_links_value, LDR_rechts_value, LDR_links_value - LDR_rechts_value))

        if black_found and LDR_links_value - LDR_rechts_value > 16000 and time.monotonic() > (ref + 0.5):
            motor_links.duty_cycle = 0
            motor_rechts.duty_cycle = 0
            print("stopped")
            break

        if LDR_links_value - LDR_rechts_value < -18000:
            black_found = True
            print("Found black")

<<<<<<< HEAD
def dance():
    for i in range(5):
        motor_links.duty_cycle = 0
        motor_rechts.duty_cycle = 0
        relais_links.value = True
        relais_rechts.value = False
        motor_links.duty_cycle = 10000
        motor_rechts.duty_cycle = 10000
        time.sleep(0.5)
        motor_links.duty_cycle = 0
        motor_rechts.duty_cycle = 0
        relais_links.value = False
        relais_rechts.value = True
        motor_links.duty_cycle = 10000
        motor_rechts.duty_cycle = 10000
        time.sleep(0.5)



motor_links.duty_cycle = 1000
motor_rechts.duty_cycle = 1000

dance()
=======

def pick_up_torentje():

    servo_motor.angle = 0
    time.sleep(0.3)
    servo_motor.angle = 135
    time.sleep(0.3)
    servo_motor.angle = 0


drive_line()
turn_right()

"""
with open('testfile.txt', 'r') as file:
    tekst = file.readlines()
    for lijn in tekst:
        lijn.strip("\n")
"""

>>>>>>> 850643582d6a7ae8df73fa8a50c2d68d3ae9416e
