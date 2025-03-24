LARGE = True

import board
import time
import pwmio
import digitalio

motor_links =  pwmio.PWMOut(board.GP1)
motor_rechts = pwmio.PWMOut(board.GP0)
relais_links = digitalio.DigitalInOut(board.GP3)
relais_rechts = digitalio.DigitalInOut(board.GP2)

relais_links.direction = digitalio.Direction.OUTPUT
relais_links.value = True
relais_rechts.direction = digitalio.Direction.OUTPUT
relais_rechts.value = True

motor_rechts.duty_cycle = 0
motor_links.duty_cycle = 0

def motor_stop():
    motor_rechts.duty_cycle = 0
    motor_links.duty_cycle = 0

def motor_dir_reset():
    relais_rechts.value = True
    relais_links.value = True


if not LARGE:
    for i in range(3):
        motor_dir_reset()
        motor_stop()
        motor_links.duty_cycle = 30000
        motor_rechts.duty_cycle = 30000
        time.sleep(3)
        relais_links.value = not relais_links.value
        relais_rechts.value = not relais_rechts.value
        time.sleep(3)

    motor_stop()

for i in range(5):
    motor_dir_reset()
    motor_stop()
    print("direction: forward, motor: left, speed: %.2f " %(30000/65535))
    motor_links.duty_cycle = 30000
    time.sleep(2)

    motor_stop()
    print("direction: forward, motor: left, speed: %.2f " %(65000/65535))
    motor_links.duty_cycle = 65000
    time.sleep(2)

    motor_stop()
    print("direction: backward, motor: left, speed: %.2f " %(30000/65535))
    relais_links.value = not relais_links.value
    motor_links.duty_cycle = 30000
    time.sleep(2)

    motor_stop()
    print("direction: backward, motor: left, speed: %.2f " %(65000/65535))
    motor_links.duty_cycle = 65000
    time.sleep(2)

    motor_stop()
    print("direction: forward, motor: rechts, speed: %.2f " % (30000 / 65535))
    motor_rechts.duty_cycle = 30000
    time.sleep(2)

    motor_stop()
    print("direction: forward, motor: rechts, speed: %.2f " % (65000 / 65535))
    motor_rechts.duty_cycle = 65000
    time.sleep(2)

    motor_stop()
    print("direction: backward, motor: rechts, speed: %.2f " % (30000 / 65535))
    relais_rechts.value = not relais_rechts.value
    motor_rechts.duty_cycle = 30000
    time.sleep(2)

    motor_stop()
    print("direction: backward, motor: rechts, speed: %.2f " % (65000 / 65535))
    motor_rechts.duty_cycle = 65000
    time.sleep(2)

    motor_dir_reset()
    motor_stop()
    print("direction: forward, motor: both, speed: %.2f " % (30000 / 65535))
    motor_links.duty_cycle = 30000
    motor_rechts.duty_cycle = 30000
    time.sleep(2)

    motor_stop()
    print("direction: forward, motor: both, speed: %.2f " % (65000 / 65535))
    motor_links.duty_cycle = 65000
    motor_rechts.duty_cycle = 65000
    time.sleep(2)

    motor_stop()
    print("direction: backward, motor: both, speed: %.2f " % (30000 / 65535))
    relais_rechts.value = not relais_rechts.value
    motor_rechts.duty_cycle = 30000
    relais_links.value = not relais_links.value
    motor_links.duty_cycle = 30000
    time.sleep(2)

    motor_stop()
    print("direction: backward, motor: both, speed: %.2f " % (65000 / 65535))
    motor_links.duty_cycle = 65000
    motor_rechts.duty_cycle = 65000

    time.sleep(2)

