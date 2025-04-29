import math
import board
import pwmio
import time

LED_RED = pwmio.PWMOut(board.GP13)
LED_GREEN = pwmio.PWMOut(board.GP15)
LED_BLUE = pwmio.PWMOut(board.GP14)


def status_led(state="default"):
    # print(state)
    if state == "default":
        # status led wit-groen (volgens functie)
        ref = time.monotonic()
        value = 0.5 * math.sin(2 * math.pi * ref) + 0.5

        LED_RED.duty_cycle = int(value * 65535)
        LED_GREEN.duty_cycle = 65535
        LED_BLUE.duty_cycle = int(value * 65535)

    if state == "blue":
        # status led blauw
        LED_RED.duty_cycle = 0
        LED_GREEN.duty_cycle = 0
        LED_BLUE.duty_cycle = 65535

    if state == "orange":
        # status led oranje (aan-uit)
        ref = time.monotonic()
        value = math.ceil(math.sin(ref))

        LED_RED.duty_cycle = 65535
        LED_GREEN.duty_cycle = int(0.1 * 65535)
        LED_BLUE.duty_cycle = 0

    if state == "red":
        # status led red (aan-uit)
        ref = time.monotonic()
        value = math.ceil(math.sin(ref))

        LED_RED.duty_cycle = int(value * 65535)
        LED_GREEN.duty_cycle = 0
        LED_BLUE.duty_cycle = 0

    if state == "party":
        # status led party mode
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
        # status led uit
        LED_RED.duty_cycle = 0
        LED_GREEN.duty_cycle = 0
        LED_BLUE.duty_cycle = 0
