import board
import time
import pwmio
import digitalio
import statusled as RGB
from analogio import AnalogIn
import random
from adafruit_motor import servo

### Defineren van de pinnen
SPEED = 0.3
# LDR-s
LDR_links = AnalogIn(board.GP26)
LDR_rechts = AnalogIn(board.GP27)
LDR_achter = AnalogIn(board.GP28)

# Motoren
motor_links = pwmio.PWMOut(board.GP21)
motor_rechts = pwmio.PWMOut(board.GP20)

relais_links = digitalio.DigitalInOut(board.GP17)
relais_links.direction = digitalio.Direction.OUTPUT
relais_links.value = False
relais_links_default = False

relais_rechts = digitalio.DigitalInOut(board.GP16)
relais_rechts.direction = digitalio.Direction.OUTPUT
relais_rechts.value = True
relais_rechts_default = True

# Servo-motor

servo_PWM = pwmio.PWMOut(board.GP3, duty_cycle=2**15, frequency=50)
servo_motor = servo.Servo(servo_PWM)

# Gevoeligheden
MINIMUM_AFWIJKWAARDE_LINKS = 24000
MINIMUM_AFWIJKWAARDE_RECHTS = 8000
MINIMUM_AFWIJKWAARDE_ACHTER = 10000

# Initialiseren score groene torentjes (voor browserapplicatie)
aantal_groene_torentjes = 0


def drive_forward(speed):
    motor_links.duty_cycle = 0
    motor_rechts.duty_cycle = 0

    relais_links.value = relais_links_default
    relais_rechts.value = relais_rechts_default

    motor_links.duty_cycle = int(speed * 65000)
    motor_rechts.duty_cycle = int(speed * 65000)


def drive_backward(speed):
    motor_links.duty_cycle = 0
    motor_rechts.duty_cycle = 0
    RGB.status_led("red")  # RGB kleurt rood volgens aan-uit-cyclus
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

    drive_forward(0.05)

    while not crossroad_found:
        RGB.status_led("default")  # Laat RGB-LED afwisselend wit-groen branden
        time.sleep(0.1)

        # Behoud vorige waarde
        prev_LDR_achter_value = LDR_achter_value

        # Update LDR waarde
        LDR_links_value = LDR_links.value
        LDR_rechts_value = LDR_rechts.value
        LDR_achter_value = LDR_achter.value

        print(
            "ACHTER: prev %s, current: %s, diff: %s"
            % (
                prev_LDR_achter_value,
                LDR_achter_value,
                abs(prev_LDR_achter_value - LDR_achter_value),
            )
        )

        # aanpassing links
        if LDR_links_value - LDR_rechts_value < -18000:
            motor_rechts.duty_cycle = int(SPEED * 65535 / 2)
            motor_links.duty_cycle = int(SPEED * 65535)
        # aanpassing rechts
        elif LDR_links_value - LDR_rechts_value > 18000:
            motor_links.duty_cycle = int(SPEED * 65535 / 2)
            motor_rechts.duty_cycle = int(SPEED * 65535)
        # Zet motoren gelijk
        else:
            drive_forward(SPEED)
        # kruispunt stop
        if abs(prev_LDR_achter_value - LDR_achter_value) > MINIMUM_AFWIJKWAARDE_ACHTER:
            print("Klaar om te draaien, waar zijn die handjes")
            crossroad_found = True
            motor_links.duty_cycle = 0
            motor_rechts.duty_cycle = 0
            # pick_up_torentje()
            print("Torentje wordt opgepakt...")
            RGB.status_led(
                "orange"
            )  # Laat RGB-LED oranje branden volgens aan-uit-cyclus


def turn_left():
    motor_links.duty_cycle = 0
    motor_rechts.duty_cycle = 0

    relais_links.value = not relais_links_default
    relais_rechts.value = relais_rechts_default

    motor_links.duty_cycle = int(SPEED * 65535)
    motor_rechts.duty_cycle = int(SPEED * 65535)

    LDR_links_value = LDR_links.value
    LDR_rechts_value = LDR_rechts.value
    LDR_achter_value = LDR_achter.value

    ref = time.monotonic()

    while True:

        time.sleep(0.05)
        prev_LDR_achter_value = LDR_achter_value
        prev_LDR_links_value = LDR_links_value
        prev_LDR_rechts_value = LDR_rechts_value

        LDR_links_value = LDR_links.value
        LDR_rechts_value = LDR_rechts.value
        LDR_achter_value = LDR_achter.value

        print(
            f"LDR_links_value: {LDR_links_value}, LDR_rechts_value: {LDR_rechts_value}, LDR_achter_value: {LDR_achter_value}, diff: {LDR_links_value - LDR_rechts_value}"
        )

        if LDR_links_value - LDR_rechts_value < -10000:
            motor_links.duty_cycle = 0
            motor_rechts.duty_cycle = 0
            break


def turn_right():
    motor_links.duty_cycle = 0
    motor_rechts.duty_cycle = 0
    relais_links.value = relais_links_default
    relais_rechts.value = not relais_rechts_default
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
            "links: %s, rechts: %s, diff: %s"
            % (LDR_links_value, LDR_rechts_value, LDR_links_value - LDR_rechts_value)
        )

        if (
            black_found
            and LDR_links_value - LDR_rechts_value > 16000
            and time.monotonic() > (ref + 0.5)
        ):
            motor_links.duty_cycle = 0
            motor_rechts.duty_cycle = 0
            print("stopped")
            break
        if LDR_links_value - LDR_rechts_value < -18000:
            black_found = True
            print("Found black")


def dance():
    for i in range(5):
        motor_links.duty_cycle = 0
        motor_rechts.duty_cycle = 0
        relais_links.value = True
        relais_rechts.value = False
        motor_links.duty_cycle = int(SPEED * 65535)
        motor_rechts.duty_cycle = int(SPEED * 65535)
        time.sleep(0.5)
        motor_links.duty_cycle = 0
        motor_rechts.duty_cycle = 0
        relais_links.value = False
        relais_rechts.value = True
        motor_links.duty_cycle = int(SPEED * 65535)
        motor_rechts.duty_cycle = int(SPEED * 65535)
        time.sleep(0.5)


def pick_up_torentje():
    servo_motor.angle = 0
    time.sleep(0.7)
    print("hoog")
    servo_motor.angle = 140
    time.sleep(0.3)
    print("laag")
    servo_motor.angle = 0


"""
microswitch = digitalio.DigitalInOut(board.GP0)
microswitch.direction = digitalio.Direction.OUTPUT

def onderzoek_ondergrond():
    op_knop_gedrukt = False

    min_links = 65535
    min_rechts = 65535
    min_achter = 65535
    max_links = 0
    max_rechts = 0
    max_achter = 0
    LDR_links_value = LDR_links.value
    LDR_rechts_value = LDR_rechts.value
    LDR_achter_value = LDR_achter.value

    while not op_knop_gedrukt:

        time.sleep(0.1)

        # onhou de vorige LDR-waarde:
        prev_LDR_links_value = LDR_links_value
        prev_LDR_rechts_value = LDR_rechts_value
        prev_LDR_achter_value = LDR_achter_value

        # lees een nieuwe waarde uit
        LDR_links_value = LDR_links.value
        LDR_rechts_value = LDR_rechts.value
        LDR_achter_value = LDR_achter.value
        print(
            'linksvoor: %s rechtsvoor: %s achter: %s' %
            (LDR_links_value, LDR_rechts_value, LDR_achter_value)
        )

        # houd de kleinste en grootste waarde bij
        if LDR_links_value > max_links:
            max_links = LDR_links_value
        elif LDR_links_value < min_links:
            min_links = LDR_links_value

        if LDR_rechts_value > max_rechts:
            max_rechts = LDR_rechts_value
        elif LDR_rechts_value < min_rechts:
            min_rechts = LDR_rechts_value

        if LDR_achter_value > max_achter:
            max_achter = LDR_achter_value
        elif LDR_achter_value < min_achter:
            min_achter = LDR_achter_value

        # stop als er op de knop gedrukt wordt
        if microswitch.value == True:
            op_knop_gedrukt = True
            print(
                'max links: %s max rechts: %s max achter: %s min links: %s min rechts: %s min achter: %s' %
                (max_links, max_rechts, max_achter, min_links, min_rechts, min_achter)
            )
        # bereken de procentuele afwijking
        LDR_links_procent = (LDR_links_value - min_links) / (max_links - min_links)
        LDR_rechts_procent = (LDR_rechts_value - min_rechts) / (max_rechts - min_rechts)
        LDR_achter_procent = (LDR_achter_value - min_achter) / (max_achter - min_achter)
    return LDR_links_procent, LDR_rechts_procent, LDR_achter_procent
"""

drive_line()
pick_up_torentje()
