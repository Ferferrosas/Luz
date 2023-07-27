import random
import numpy as np
from itertools import repeat
# TIMING CONSTANTS:
# *****************

updateRate= 0.9


ExperimentConfigureTime=0
fixationCrossTime=0
cueTime= 2
#timeout =3
taskTime =5
resultTime=1
restTime= 2
#fixationTime = 1

n = 1

n_flexion_met = n
n_extension_met = n
n_flexion_pha = n
n_extension_pha = n
n_adduction_met = n
n_abduction_met = n
# n_pronation = 0
# n_supination = 0
n_pointing = n
n_finger_3 = n
n_finger_2 = n
n_middle_finger = n
n_ring_finger = n
n_pinkie_finger = n


flexion_met_array = list(repeat(1, n_flexion_met))#upGreen-0,128,0
extension_met_array = list(repeat(2, n_extension_met))#upOrange-219,71,0
flexion_pha_array = list(repeat(3, n_flexion_pha))#upAqua-0,193,179
extension_pha_array = list(repeat(4, n_extension_pha))#upPink-191,0,96
adduction_met_array = list(repeat(5, n_adduction_met))#upRed-170,0,0
abduction_met_array = list(repeat(6, n_abduction_met))#upYellow-255,255,0
# pronation_array = list(repeat(7, n_pronation))#upAquamarine-127,255,212
# supination_array = list(repeat(8, n_supination))#upBlueviolet-138,43,226
pointing_array = list(repeat(7, n_pointing))#upBrown-165,42,42
finger_3_array = list(repeat(8, n_finger_3))#upGoldenrod-218,165,32
finger_2_array = list(repeat(9, n_finger_2))#uplightcoral-240,128,128
middle_finger_array = list(repeat(10, n_middle_finger))#upOlivedrab-107,142,35
ring_finger_array = list(repeat(11, n_ring_finger))#upPeachpuff-255,218,185
pinkie_finger_array = list(repeat(12, n_pinkie_finger))#upPink2-255,192,203


total = len(flexion_met_array) + len(extension_met_array) + len(flexion_pha_array) + len(extension_pha_array) + len(adduction_met_array) + \
         len(abduction_met_array) + len(pointing_array) + len(finger_3_array) + \
         len(finger_2_array) + len(middle_finger_array) + len(ring_finger_array) + len(pinkie_finger_array)
#trials = np.zeros(total)
all_arrays = flexion_met_array + extension_met_array + flexion_pha_array + extension_pha_array + adduction_met_array \
             + abduction_met_array + pointing_array + finger_3_array \
             + finger_2_array + middle_finger_array + ring_finger_array + pinkie_finger_array \

#for i in range(0, total, 1):
#    trials[i] = random.sample(all_arrays, 1)[0]
#    all_arrays.remove(trials[i])
