LARGE = True

import board
import time
import pwmio
import digitalio
from adafruit_motor import servo

motor_links = pwmio.PWMOut(board.GP1)
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
    for i in range(2):
        motor_rechts.duty_cycle = int(motor_rechts.duty_cycle / 10)
        motor_links.duty_cycle = int(motor_links.duty_cycle / 10)
    motor_rechts.duty_cycle = 0
    motor_links.duty_cycle = 0


def motor_dir_reset():
    relais_rechts.value = True
    relais_links.value = True


if True:
    pass
else:
    for i in range(1):
        motor_dir_reset()
        motor_stop()
        print("direction: forward, motor: left, speed: %.2f " % (30000 / 65535))
        motor_links.duty_cycle = 30000
        time.sleep(2)

        motor_stop()
        print("direction: forward, motor: left, speed: %.2f " % (20000 / 65535))
        motor_links.duty_cycle = 20000
        time.sleep(2)

        motor_stop()
        print("direction: backward, motor: left, speed: %.2f " % (30000 / 65535))
        relais_links.value = not relais_links.value
        motor_links.duty_cycle = 30000
        time.sleep(2)

        motor_stop()
        print("direction: backward, motor: left, speed: %.2f " % (20000 / 65535))
        motor_links.duty_cycle = 20000
        time.sleep(2)

        motor_stop()
        print("direction: forward, motor: rechts, speed: %.2f " % (30000 / 65535))
        motor_rechts.duty_cycle = 30000
        time.sleep(2)

        motor_stop()
        print("direction: forward, motor: rechts, speed: %.2f " % (20000 / 65535))
        motor_rechts.duty_cycle = 20000
        time.sleep(2)

        motor_stop()
        print("direction: backward, motor: rechts, speed: %.2f " % (30000 / 65535))
        relais_rechts.value = not relais_rechts.value
        motor_rechts.duty_cycle = 30000
        time.sleep(2)

        motor_stop()
        print("direction: backward, motor: rechts, speed: %.2f " % (20000 / 65535))
        motor_rechts.duty_cycle = 20000
        time.sleep(2)

        motor_dir_reset()
        motor_stop()
        print("direction: forward, motor: both, speed: %.2f " % (30000 / 65535))
        motor_links.duty_cycle = 30000
        motor_rechts.duty_cycle = 30000
        time.sleep(2)

        motor_stop()
        print("direction: forward, motor: both, speed: %.2f " % (20000 / 65535))
        motor_links.duty_cycle = 20000
        motor_rechts.duty_cycle = 20000
        time.sleep(2)

        motor_stop()
        print("direction: backward, motor: both, speed: %.2f " % (30000 / 65535))
        relais_rechts.value = not relais_rechts.value
        motor_rechts.duty_cycle = 30000
        relais_links.value = not relais_links.value
        motor_links.duty_cycle = 30000
        time.sleep(2)

        motor_stop()
        print("direction: backward, motor: both, speed: %.2f " % (20000 / 65535))
        motor_links.duty_cycle = 20000
        motor_rechts.duty_cycle = 20000

        time.sleep(2)




motor_stop()

servo_PWM = pwmio.PWMOut(board.GP5, duty_cycle= 2 **15, frequency=50)
servo_motor = servo.Servo(servo_PWM)

for i in range(10):
    servo_motor.angle = 0
    print(0)
    time.sleep(1)
    servo_motor.angle = 90
    print(90)
    time.sleep(1)
