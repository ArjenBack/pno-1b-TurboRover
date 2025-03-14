import digitalio
import time
import board
from analogio import AnalogIn

LDR_linksvoor = AnalogIn(board.GP28)
LDR_rechtsvoor = AnalogIn(board.GP27)
LDR_achter = AnalogIn(board.GP26)
metingnummer = 0

while metingnummer < 1000:
    metingnummer += 1
    gemiddelde = (LDR_linksvoor.value + LDR_rechtsvoor.value) / 2
    verschil = LDR_linksvoor.value - LDR_rechtsvoor.value
    print(metingnummer, LDR_linksvoor.value, LDR_rechtsvoor.value, LDR_achter.value, verschil, gemiddelde)
    time.sleep(0.1)