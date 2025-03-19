#De eerste waarden van de LDR's moeten uitgelezen worden voor het programma start
import board
import time
import pwmio
import digitalio
from analogio import AnalogIn

MINIMUM_AFWIJKWAARDE_LINKS = 11000
MINIMUM_AFWIJKWAARDE_RECHTS = 8000
MINIMUM_AFWIJKWAARDE_ACHTER = 14000

LDR_links = AnalogIn(board.GP27)
LDR_links_value = LDR_links.value
LDR_rechts = AnalogIn(board.GP28)
LDR_rechts_value = LDR_rechts.value
LDR_achter = AnalogIn(board.GP26)
LDR_achter_value = LDR_achter.value

motor_links =  pwmio.PWMOut(board.GP0)
motor_rechts = pwmio.PWMOut(board.GP1)
relais_links = digitalio.DigitalInOut(board.GP2)
relais_rechts = digitalio.DigitalInOut(board.GP3)

relais_links.direction = digitalio.Direction.OUTPUT
relais_links.value = True
relais_rechts.direction = digitalio.Direction.OUTPUT
relais_rechts.value = True


def main():
#TODO: Nog toe te voegen: statusled nog integreren in code
    while True:  # endless loop

        #status_LED()  # Laat statusLED branden met variërende kleuren
        prev_LDR_links_value = LDR_links_value
        prev_LDR_rechts_value = LDR_rechts_value
        prev_LDR_achter_value = LDR_achter_value

        LDR_links_value = LDR_links.value
        LDR_rechts_value = LDR_rechts.value
        LDR_achter_value = LDR_achter.value

        color_change = abs(prev_LDR_links_value - LDR_links_value) > MINIMUM_AFWIJKWAARDE_LINKS or abs(prev_LDR_rechts_value - LDR_rechts_value) > MINIMUM_AFWIJKWAARDE_RECHTS

        crossroads_found = abs(prev_LDR_links_value - LDR_links_value) > MINIMUM_AFWIJKWAARDE_RECHTS and abs(prev_LDR_rechts_value - LDR_rechts_value) > MINIMUM_AFWIJKWAARDE_RECHTS

        time_to_turn = abs(prev_LDR_achter_value - LDR_achter_value) > MINIMUM_AFWIJKWAARDE_ACHTER

        #with open('databestand.txt', 'r') as info:
         #   info_list = info.readlines()
          #  groen_torentje_aanwezig = info_list[0] == "Green"
        if color_change:  # lichtsensor detecteert overgang wit bord naar zwarte lijn
            if crossroads_found:  # Aangekomen op kruispunt, beide lichtsensoren detecteren zwart
                #if groen_torentje_aanwezig:
                 #   lift_torentje()  # Drijf servo aan om met grijparm torentje op te tillen
                 has_turned == False
                 while has_turned == False:
                    if time_to_turn:
                        has_turned == True
                        rotate()
                    else:
                        drive_forward() #Ga naar het dichtstbijzijnde groene torentje, kies weg afhankelijk van snelsteroutealgoritme

        elif abs(prev_LDR_links_value - LDR_links_value) > MINIMUM_AFWIJKWAARDE_LINKS:  # Afwijking van de baan naar links, terug op de baan komen
            rotate("right", "partial")  # Draai naar rechts

        elif abs(prev_LDR_rechts_value - LDR_rechts_value) > MINIMUM_AFWIJKWAARDE_RECHTS:  # Afwijking van de baan naar rechts, terug op de baan komen
            rotate("left", "partial")  # Draai naar links

        #if botsing_gedetecteerd:  # botsingssensor detecteert botsing
         #   data = "manueel"  # Stopt de loop

        else:  # Normale situatie: Rijd vooruit
            drive_forward()

        time.sleep(0.1)

main()

def rotate(direction, mode):
    if mode == "partial":     # line correction
        if direction == "left":
            drive_stop()
            motor_links.duty_cycle = 30000
            motor_rechts.duty_cycle = 65535
        elif direction == "right":
            drive_stop()
            motor_rechts.duty_cycle = 30000
            motor_links.duty_cycle = 65535

    else: # full turn 90 degrees
        stop_turning = LDR_linksvoor > 25000 and LDR_rechtsvoor > 40000
        while not stop_turning:
            if direction == "left":
                pass
            elif direction == "right":
                pass

def drive_forward():
    motor_links.duty_cycle = 65535
    motor_rechts.duty_cycle = 65535
    relais_links.value = True
    relais_rechts.value = True

def drive_stop():
    motor_links.duty_cycle = 0
    motor_rechts.duty_cycle = 0

def drive_backward():
    motor_links.duty_cycle = 65535
    motor_rechts.duty_cycle = 65535
    relais_links.value = False
    relais_rechts.value = False

#def status_LED():
  #  pass
#def lift_torentje():
 #   pass
