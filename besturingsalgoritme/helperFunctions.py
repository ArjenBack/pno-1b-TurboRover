import board
import math
import time
import pwmio
import digitalio
from analogio import AnalogIn
from adafruit_motor import servo

# ------------------------------------------------------------------------------
#                           CONFIGURATION CONSTANTS
# ------------------------------------------------------------------------------
SPEED = 0.4
TURN_SPEED = 0.28


# ------------------------------------------------------------------------------
#                           HARDWARE INITIALIZATION
# ------------------------------------------------------------------------------

# Light sensors for line detection
LDR_LEFT = AnalogIn(board.GP26)
LDR_RIGHT = AnalogIn(board.GP27)
LDR_REAR = AnalogIn(board.GP28)

# Motor control
MOTOR_LEFT = pwmio.PWMOut(board.GP21)
MOTOR_RIGHT = pwmio.PWMOut(board.GP20)

# Relays for motor direction
RELAIS_LEFT = digitalio.DigitalInOut(board.GP17)
RELAIS_LEFT.direction = digitalio.Direction.OUTPUT
RELAIS_LEFT.value = False
relais_left_default = False

RELAIS_RIGHT = digitalio.DigitalInOut(board.GP16)
RELAIS_RIGHT.direction = digitalio.Direction.OUTPUT
RELAIS_RIGHT.value = True
relais_right_default = True

# Limit switches for collision detection
FRONT_SWITCH = digitalio.DigitalInOut(board.GP22)
FRONT_SWITCH.direction = digitalio.Direction.INPUT

LEFT_SWITCH = digitalio.DigitalInOut(board.GP19)
LEFT_SWITCH.direction = digitalio.Direction.INPUT

REAR_SWITCH = digitalio.DigitalInOut(board.GP18)
REAR_SWITCH.direction = digitalio.Direction.INPUT

RIGHT_SWITCH = digitalio.DigitalInOut(board.GP0)
RIGHT_SWITCH.direction = digitalio.Direction.INPUT

# Servo for pickup mechanism
SERVO_PWM = pwmio.PWMOut(board.GP3, duty_cycle=2**15, frequency=50)
SERVO_MOTOR = servo.Servo(SERVO_PWM)

# LED for status indication
LED_RED = pwmio.PWMOut(board.GP13)
LED_GREEN = pwmio.PWMOut(board.GP15)
LED_BLUE = pwmio.PWMOut(board.GP14)

# Calibration defaults
MIN_LEFT, MAX_LEFT, MIN_RIGHT, MAX_RIGHT, MIN_REAR, MAX_REAR = (
    28038,
    43850,
    21269,
    39113,
    14147,
    27830,
)


# ------------------------------------------------------------------------------
#                           SENSOR PROCESSING FUNCTIONS
# ------------------------------------------------------------------------------
def normalizeLeft(value):
    """
    Normalize the value of the left sensor to a percentage (0-1).

    Args:
        value (int): Raw sensor value

    Returns:
        Normalized value (float) between 0 and 1
    """
    return (value - MIN_LEFT) / (MAX_LEFT - MIN_LEFT)


def normalizeRight(value):
    """
    Normalize the value of the right sensor to a percentage (0-1).

    Args:
        value (int): Raw sensor value

    Returns:
        Normalized value (float) between 0 and 1
    """
    return (value - MIN_RIGHT) / (MAX_RIGHT - MIN_RIGHT)


def normalizeRear(value):
    """
    Normalize the value of the rear sensor to a percentage (0-1).

    Args:
        value (int): Raw sensor value

    Returns:
        Normalized value (float) between 0 and 1
    """
    return (value - MIN_REAR) / (MAX_REAR - MIN_REAR)


def calibrate():
    """
    Calibrate the min and max values of all LDR sensors.

    The function continuously reads sensor values until the front button is pressed,
    recording the minimum and maximum values for each sensor.

    Returns:
        Tuple of min and max values of each sensor
        (minLeft, maxLeft, minRight,maxRight, minBack, maxRear)
    """
    op_knop_gedrukt = False

    MIN_LEFT = 65535
    MIN_RIGHT = 65535
    MIN_REAR = 65535
    MAX_LEFT = 0
    MAX_RIGHT = 0
    MAX_REAR = 0

    LDR_left_value = LDR_LEFT.value
    LDR_right_value = LDR_RIGHT.value
    LDR_rear_value = LDR_REAR.value

    while not op_knop_gedrukt:

        time.sleep(0.1)

        LDR_left_value = LDR_LEFT.value
        LDR_right_value = LDR_RIGHT.value
        LDR_rear_value = LDR_REAR.value

        if LDR_left_value > MAX_LEFT:
            MAX_LEFT = LDR_left_value
        elif LDR_left_value < MIN_LEFT:
            MIN_LEFT = LDR_left_value

        if LDR_right_value > MAX_RIGHT:
            MAX_RIGHT = LDR_right_value
        elif LDR_right_value < MIN_RIGHT:
            MIN_RIGHT = LDR_right_value

        if LDR_rear_value > MAX_REAR:
            MAX_REAR = LDR_rear_value
        elif LDR_rear_value < MIN_REAR:
            MIN_REAR = LDR_rear_value

        if FRONT_SWITCH.value:
            op_knop_gedrukt = True
    return MIN_LEFT, MAX_LEFT, MIN_RIGHT, MAX_RIGHT, MIN_REAR, MAX_REAR


# -----------------------------------------------------------------------------
#                              MOVEMENT FUNCTIONS
# -----------------------------------------------------------------------------
def drive_line():
    """
    Drive along line until a crossroad is detected.

    Use LDR sensors to follow a line, adjusting motor speed to stay centered.
    Stops when a crossroad is detected by the rear sensor.
    """

    LDR_left_value = LDR_LEFT.value
    LDR_right_value = LDR_RIGHT.value
    LDR_rear_value = LDR_REAR.value

    # Set motor direction
    RELAIS_LEFT.value = relais_left_default
    RELAIS_RIGHT.value = relais_right_default

    # Start motors
    MOTOR_LEFT.duty_cycle = int(SPEED * 65000)
    MOTOR_RIGHT.duty_cycle = int(SPEED * 65000)

    while True:
        status_led("default")
        time.sleep(0.05)

        prev_LDR_rear_value = LDR_rear_value

        LDR_left_value = LDR_LEFT.value
        LDR_right_value = LDR_RIGHT.value
        LDR_rear_value = LDR_REAR.value

        # Line following logic
        if normalizeLeft(LDR_left_value) - normalizeRight(LDR_right_value) < -0.40:
            # Line is to the right, adjust steering
            MOTOR_RIGHT.duty_cycle = int(SPEED * 65535 / 2)
            MOTOR_LEFT.duty_cycle = int(SPEED * 65535)
        elif normalizeLeft(LDR_left_value) - normalizeRight(LDR_right_value) > 0.40:
            # Line is to the left, adjust steering
            MOTOR_LEFT.duty_cycle = int(SPEED * 65535 / 2)
            MOTOR_RIGHT.duty_cycle = int(SPEED * 65535)
        else:
            # Line is centered, go straight
            MOTOR_LEFT.duty_cycle = int(SPEED * 65535)
            MOTOR_RIGHT.duty_cycle = int(SPEED * 65535)

        # Detect crossroads by significant change in rear sensor
        if (normalizeRear(LDR_rear_value) - normalizeRear(prev_LDR_rear_value)) > 0.25:
            break
    MOTOR_LEFT.duty_cycle = 0
    MOTOR_RIGHT.duty_cycle = 0


def TURN_LEFT():
    """
    Make a left turn at a crossroad

    Reverses the left motor direction and runs both motors until
    the rover has completed a left turn.
    """
    status_led("blue")
    MOTOR_LEFT.duty_cycle = 0
    MOTOR_RIGHT.duty_cycle = 0

    # Set motor direction to left turn
    RELAIS_LEFT.value = not relais_left_default
    RELAIS_RIGHT.value = relais_right_default

    # Start motors
    MOTOR_LEFT.duty_cycle = int(TURN_SPEED * 65535)
    MOTOR_RIGHT.duty_cycle = int(TURN_SPEED * 65535)

    LDR_left_value = LDR_LEFT.value
    LDR_right_value = LDR_RIGHT.value

    ref = time.monotonic()

    crossroad_found = False

    while True:

        time.sleep(0.05)

        LDR_left_value = LDR_LEFT.value
        LDR_right_value = LDR_RIGHT.value

        # Check if the rover has turned enough
        if (
            normalizeLeft(LDR_left_value) - normalizeRight(LDR_right_value) > 0.8
            and time.monotonic() - ref > 0.5
        ):
            crossroad_found = True

        # Stop when the rover detects the line again
        if crossroad_found and normalizeLeft(LDR_left_value) > 0.25:
            MOTOR_LEFT.duty_cycle = 0
            MOTOR_RIGHT.duty_cycle = 0
            break

    MOTOR_LEFT.duty_cycle = 0
    MOTOR_RIGHT.duty_cycle = 0


def TURN_RIGHT():
    """
    Make a right turn at a crossroad.

    Reverses the right motor directions and runs both motors until
    the rover has completed a right turn.
    """
    status_led("blue")
    MOTOR_LEFT.duty_cycle = 0
    MOTOR_RIGHT.duty_cycle = 0

    # Set motor directions for right turn
    RELAIS_LEFT.value = relais_left_default
    RELAIS_RIGHT.value = not relais_right_default

    # Start motors
    MOTOR_LEFT.duty_cycle = int(TURN_SPEED * 65535)
    MOTOR_RIGHT.duty_cycle = int(TURN_SPEED * 65535)

    LDR_left_value = LDR_LEFT.value
    LDR_right_value = LDR_RIGHT.value

    ref = time.monotonic()

    crossroad_found = False

    while True:

        time.sleep(0.02)

        LDR_left_value = LDR_LEFT.value
        LDR_right_value = LDR_RIGHT.value

        # Check if the rover has turned enough
        if (
            normalizeLeft(LDR_left_value) - normalizeRight(LDR_right_value) < -0.8
            and time.monotonic() - ref > 0.5
        ):
            crossroad_found = True
            break

        # Stop when the rover detects the line again
        if crossroad_found and normalizeRight(LDR_right_value) > 0.25:
            MOTOR_LEFT.duty_cycle = 0
            MOTOR_RIGHT.duty_cycle = 0
            break

    MOTOR_LEFT.duty_cycle = 0
    MOTOR_RIGHT.duty_cycle = 0


def pick_up_tower():
    """
    Control the servo to pick up a tower object.

    Moves the servo to 0 degrees (lowered position), waits,
    then moves to 140 degrees (raised position) to grab the object.
    """
    SERVO_MOTOR.angle = 0
    time.sleep(0.7)
    SERVO_MOTOR.angle = 140
    time.sleep(0.3)
    SERVO_MOTOR.angle = 0


# -----------------------------------------------------------------------------
#                       STATUS INDICATION FUNCTIONS
# -----------------------------------------------------------------------------
def status_led(state="default"):
    """
    Control the RGB LED to indicate different states.

    Args:
        state (str): one of "default", "blue", "orange", "red", "party" or "off
    """

    if state == "default":
        ref = time.monotonic()
        value = 0.5 * math.sin(2 * math.pi * ref) + 0.5

        LED_RED.duty_cycle = int(value * 65535)
        LED_GREEN.duty_cycle = 65535
        LED_BLUE.duty_cycle = int(value * 65535)

    if state == "blue":
        LED_RED.duty_cycle = 0
        LED_GREEN.duty_cycle = 0
        LED_BLUE.duty_cycle = 65535

    if state == "orange":
        ref = time.monotonic()
        value = math.ceil(math.sin(ref))

        LED_RED.duty_cycle = 65535
        LED_GREEN.duty_cycle = int(0.1 * 65535)
        LED_BLUE.duty_cycle = 0

    if state == "red":
        ref = time.monotonic()
        value = math.ceil(math.sin(ref))

        LED_RED.duty_cycle = int(value * 65535)
        LED_GREEN.duty_cycle = 0
        LED_BLUE.duty_cycle = 0

    if state == "party":
        ref = time.monotonic()

        f_R, f_G, f_B = 0.5, 0.7, 0.9
        phi_R, phi_G, phi_B = 0, math.pi / 3, 2 * math.pi / 3

        R = int(127.5 * (math.sin(2 * math.pi * f_R * ref + phi_R) + 1))
        G = int(127.5 * (math.sin(2 * math.pi * f_G * ref + phi_G) + 1))
        B = int(127.5 * (math.sin(2 * math.pi * f_B * ref + phi_B) + 1))

        LED_RED.duty_cycle = int(65536 * R / 256)
        LED_GREEN.duty_cycle = int(65536 * G / 256)
        LED_BLUE.duty_cycle = int(65536 * B / 256)

    if state == "off":
        LED_RED.duty_cycle = 0
        LED_GREEN.duty_cycle = 0
        LED_BLUE.duty_cycle = 0
