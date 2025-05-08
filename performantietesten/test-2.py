###########
# TESTS   #
###########
# test draaien
driveLine()
start = time.perf_counter()
turnRight()
stop = time.perf_counter()
print("Tijd: ", stop - start)

# test rechtdoor rijden
driveLine()
driveLine()
print("stop")
