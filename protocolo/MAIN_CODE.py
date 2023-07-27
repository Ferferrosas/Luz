import serial
from serial import SerialException
import sys
import os
import pygame
import time
from utils import *

import pyautogui
import math

from CONFIG import *
from concurrent.futures import ThreadPoolExecutor

dirP = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
sys.path.append(dirP + '/z1_ref_other/0_lib')
Complete_trial = 0

archivo  = input("Nombre del archivo: ")
fileName = archivo + ".csv"

VAR  = 1
FIN  = 1
TEMP = 0

EXIT_ON_SERIAL = False

arduino_port = "COM4"
baud         = 230400

screen = pyautogui.size()

screen_width    = screen[0]
screen_height   = screen[1]
screen_width_o  = screen[0]
screen_height_o = screen[1]
scaling_factor  = 1

# Normalize everything to the size of the bar as determined below
screen_width  = int(screen_width / scaling_factor)
screen_height = int(screen_height / scaling_factor)
screen        = pygame.display.set_mode((screen_width, screen_height))  # Setting up the screen size
screen_height = min(screen_width, screen_height)
screen_width  = min(screen_height, screen_width)

pygame.display.set_caption('Motor Imagery Experiment')

spaceToBeLeft          = 2.5 * int(screen_width * 0.1) 
Bigger_rectangle_width = screen_width - 2 * spaceToBeLeft
bar_width              = 0.5 * Bigger_rectangle_width

# Load flexion and extension images, scale them, and place them at the side of the rectangle
flexion_image         = pygame.image.load('flexion.png')
image_scaling_flexion = spaceToBeLeft / flexion_image.get_rect().size[0]
flexion_image         = pygame.transform.scale(flexion_image, (int(spaceToBeLeft), int(flexion_image.get_rect().size[1] * image_scaling_flexion)))

(flexion_image_x, flexion_image_y) = (0, screen_height / 2 - flexion_image.get_rect().size[1] / 2)

extension_image         = pygame.image.load('extension.png')
image_scaling_extension = spaceToBeLeft / extension_image.get_rect().size[0]
extension_image         = pygame.transform.scale(extension_image, (int(spaceToBeLeft), int(extension_image.get_rect().size[1] * image_scaling_extension)))

(extension_image_x, extension_image_y) = (screen_width - spaceToBeLeft, screen_height / 2 - extension_image.get_rect().size[1] / 2)
bar_height                             = int(flexion_image.get_rect().size[1] * 0.2086701)

# setting the dimensions of the rectangle in which the bar moves right/left
Bigger_rectangle_height = bar_height
Bigger_rectangle_X      = screen_width_o / 2 - Bigger_rectangle_width / 2
Bigger_rectangle_Y      = screen_height / 2 - bar_height / 2 + bar_height * 2
Bigthickness            = 3  # thickness of the edge lines for the rectangle and other shapes

# color setting
black           = (0, 0, 0)
bigRecEdgeColor = (185, 188, 181)  # FES:(130,92,63) #
bigRecColor     = (46, 52, 54)  # FES:(198,160,131) #
barColor        = bigRecEdgeColor
white           = (229, 229, 229)
yellow          = (255, 255, 0)
# rightRed      = (203, 0, 0)
# leftBlue      = (52, 101, 163)
upGreen         = (0, 128, 0)
upOrange        = (219, 71, 0)
upAqua          = (0, 193, 179)
upPink          = (191, 0, 96)
upRed           = (170, 0, 0)
upyellow        = (255, 255, 0)
upAquamarine    = (127, 255, 212)
upBlueviolet    = (138, 43, 226)
upBrown         = (165, 42, 42)
upGoldenrod     = (218, 165, 32)
uplightcoral    = (240, 128, 128)
upOlivedrab     = (107, 142, 35)
upPeachpuff     = (255, 218, 185)
upPink2         = (255, 192, 203)

# Initial position of the bar in the middle of the rectangle:
initial_x      = screen_width - bar_width
initial_y      = Bigger_rectangle_Y
centerOfScreen = (screen_width_o / 2, screen_height / 2)
initial_x_2    = centerOfScreen[0]
thickness      = 0

# time.sleep(5)
# correct for cue arrows by increasing the width of the bar so it is aligned with the arrow as it reaches the end of
# the task
arrowMidShift = (bar_height / 2)
bar_width     = bar_width + arrowMidShift
initial_x     = initial_x - arrowMidShift / 2

# new rectangle dimensions
Bigger_rectangle_new_X      = (Bigger_rectangle_X + (Bigger_rectangle_width / 2)) - (Bigger_rectangle_height / 2)
Bigger_rectangle_new_Y      = (Bigger_rectangle_Y + Bigger_rectangle_height) - (Bigger_rectangle_width / 2 + Bigger_rectangle_height / 2)
Bigger_rectangle_height_new = Bigger_rectangle_width / 2 + Bigger_rectangle_height / 2

# new 'down' rectangle dimensions (not used here)
Down_rectangle_X = Bigger_rectangle_new_X
Down_rectangle_Y = Bigger_rectangle_new_Y + (Bigger_rectangle_height_new - Bigger_rectangle_height)

# new bar
bar_height_new = Bigger_rectangle_height
bar_width_new  = bar_height
initial_y_new  = Bigger_rectangle_new_Y + (Bigger_rectangle_height_new / 2)
initial_x_new  = Bigger_rectangle_new_X

######## Arrow dimensions goes here
ArrowTipWidth        = bar_width / 3.5
ArrowRectangleHeight = Bigger_rectangle_height
ArrowRectangleWidth  = 0.5 * ArrowTipWidth

upArrowStartingX       = Bigger_rectangle_new_X
upArrowStartingY       = Bigger_rectangle_new_Y - ArrowRectangleWidth
upArrowRectangleHeight = ArrowRectangleWidth
upArrowRectangleWidth  = ArrowRectangleHeight

point1UpArrow = (centerOfScreen[0], upArrowStartingY - ArrowTipWidth)
point2UpArrow = (centerOfScreen[0] - ArrowTipWidth / math.sqrt(3), upArrowStartingY)
point3UpArrow = (centerOfScreen[0] + ArrowTipWidth / math.sqrt(3),upArrowStartingY)

bar_width                  = Bigger_rectangle_height
Bigger_rectangle_width_adj = Bigger_rectangle_width / 2 + bar_width / 2
Bigger_rectangle_X_adj     = Bigger_rectangle_X + (Bigger_rectangle_width / 2 - bar_width / 2)

IM_FLEXION_MET   = pygame.image.load("neu1.jfif").convert()
IM_FLEXION_MET   = pygame.transform.scale(IM_FLEXION_MET, (624, 577))
IM_EXTENSION_MET = pygame.image.load("neu2.jfif").convert()
IM_EXTENSION_MET = pygame.transform.scale(IM_EXTENSION_MET, (624, 619.19))
IM_FLEXION_PHA   = pygame.image.load("neu7.jfif").convert()
IM_FLEXION_PHA   = pygame.transform.scale(IM_FLEXION_PHA, (624, 636.70))
IM_EXTENSION_PHA = pygame.image.load("neu8.jfif").convert()
IM_EXTENSION_PHA = pygame.transform.scale(IM_EXTENSION_PHA, (624, 636.70))
IM_ADDUCTION_MET = pygame.image.load("neu6.jfif").convert()
IM_ADDUCTION_MET = pygame.transform.scale(IM_ADDUCTION_MET, (624, 590.60))
IM_ABDUCTION_MET = pygame.image.load("neu5.jfif").convert()
IM_ABDUCTION_MET = pygame.transform.scale(IM_ABDUCTION_MET, (624, 577))
# IM_PRONATION   = pygame.image.load("neu7.jfif").convert()
# IM_PRONATION   = pygame.transform.scale(IM_PRONATION, (624, 577))
# IM_SUPINATION  = pygame.image.load("neu8.jfif").convert()
# IM_SUPINATION  = pygame.transform.scale(IM_SUPINATION, (624, 577))
IM_POINTING      = pygame.image.load("neu9.jfif").convert()
IM_POINTING      = pygame.transform.scale(IM_POINTING, (624, 577))
IM_FINGER_3      = pygame.image.load("neu10.jfif").convert()
IM_FINGER_3      = pygame.transform.scale(IM_FINGER_3, (624, 577))
IM_FINGER_2      = pygame.image.load("neu11.jfif").convert()
IM_FINGER_2      = pygame.transform.scale(IM_FINGER_2, (624, 577))
IM_MIDDLE_FINGER = pygame.image.load("neu12.jfif").convert()
IM_MIDDLE_FINGER = pygame.transform.scale(IM_MIDDLE_FINGER, (624, 577))
IM_RING_FINGER   = pygame.image.load("neu13.jfif").convert()
IM_RING_FINGER   = pygame.transform.scale(IM_RING_FINGER, (624, 577))
IM_PINKIE_FINGER = pygame.image.load("neu14.jfif").convert()
IM_PINKIE_FINGER = pygame.transform.scale(IM_PINKIE_FINGER, (624, 577))


# CORRECTO = pygame.image.load("correcto.png").convert()
# CORRECTO = pygame.transform.scale(CORRECTO, (624, 577))
# INCORRECTO = pygame.image.load("incorrecto.png").convert()
# INCORRECTO = pygame.transform.scale(INCORRECTO, (624, 619.19))
##################################
######## RUN STARTS HERE #########
##################################
def visualinterface():
    time.sleep(ExperimentConfigureTime)  # display the interface for a certain period that is set in the i0_configFile.py file
    screen.fill(black)

    arrowColor = white

    for trial in all_arrays:  # trial = +1 (extension)/-1(flexion)
        class_to_color = {1: upGreen, 2: upOrange, 3: upAqua, 4: upPink, 5: upRed, 6: upyellow, 7: upBrown, 8: upGoldenrod, 9: uplightcoral, 10: upOlivedrab, 11: upPeachpuff, 12: upPink2}
        currentClass = trial
        arrowColor = class_to_color.get(currentClass)

        print('Class of current trial: ', currentClass)
        
        color_value = class_to_color.get(currentClass)
        pygame.draw.rect(screen, color_value, (upArrowStartingX, upArrowStartingY, upArrowRectangleWidth, upArrowRectangleHeight), 0)
        pygame.draw.polygon(screen, color_value, (point1UpArrow, point2UpArrow, point3UpArrow))

        SendID(',2000')
        if FIN == 1 and EXIT_ON_SERIAL == True:
            sys.exit()

        pygame.draw.rect(screen, bigRecColor, (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,Bigger_rectangle_height_new), 0)
        pygame.draw.rect(screen, bigRecEdgeColor, (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height, Bigger_rectangle_height_new),Bigthickness) 
        pygame.draw.rect(screen, barColor, (initial_x_new, Down_rectangle_Y, bar_width, bar_width))
        pygame.draw.rect(screen, barColor, (initial_x_new, Down_rectangle_Y, bar_width, bar_width))
        pygame.draw.rect(screen, barColor, (initial_x_new, Down_rectangle_Y, bar_width, bar_width))

        pygame.display.update()
        # new code for cue timing

        point1 = (centerOfScreen[0], Bigger_rectangle_Y)
        point2 = (centerOfScreen[0] - 0.35 * bar_height, Bigger_rectangle_Y + bar_height / 2)
        point3 = (centerOfScreen[0] + 0.35 * bar_height, Bigger_rectangle_Y + bar_height / 2)\
        
        context = globals().copy()
        context.update(locals())
        f_image_selection = {
            1:  lambda: draw_image_with_arrow(IM_EXTENSION_MET, context),
            2:  lambda: draw_image_with_arrow(IM_FLEXION_MET, context),
            3:  lambda: draw_image_with_arrow(IM_FLEXION_PHA, context),
            4:  lambda: draw_image_with_arrow(IM_EXTENSION_PHA, context),
            5:  lambda: draw_image_with_arrow(IM_ABDUCTION_MET, context),
            6:  lambda: draw_image_with_arrow(IM_ABDUCTION_MET, context),
            7:  lambda: draw_image_with_arrow(IM_POINTING, context),
            8:  lambda: draw_image_with_arrow(IM_FINGER_3, context),
            9:  lambda: draw_image_with_arrow(IM_FINGER_2, context),
            10: lambda: draw_image_with_arrow(IM_MIDDLE_FINGER, context),
            11: lambda: draw_image_with_arrow(IM_RING_FINGER, context),
        }
        f_image_selection.get(currentClass)()

        pygame.draw.polygon(screen, arrowColor, (point1, point2, point3))
        pygame.display.update()

        # COMENTAMOS ESTO
        if currentClass == 1:
            SendID(',300')
        elif currentClass == 2:
            SendID(',400')
        elif currentClass == 3:
            SendID(',500')
        elif currentClass == 4:
            SendID(',600')
        elif currentClass == 5:
            SendID(',700')
        elif currentClass == 6:
            SendID(',800')
        elif currentClass == 7:
            SendID(',1100')
        elif currentClass == 8:
            SendID(',1200')
        elif currentClass == 9:
            SendID(',1300')
        elif currentClass == 10:
            SendID(',1400')
        elif currentClass == 11:
            SendID(',1500')
        elif currentClass == 12:
            SendID(',1600')

        time.sleep(cueTime)  
        screen.fill(black)

        prevTime = time.time()
        task_cue = 0
        if EXIT_ON_SERIAL:
            if currentClass == 1 and task_cue == 0:
                SendID(',301')
                if FIN == 1:
                    sys.exit()
            elif currentClass == 2 and task_cue == 0:
                SendID(',401')
                if FIN == 1:
                    sys.exit()
            elif currentClass == 3 and task_cue == 0:
                SendID(',501')
                if FIN == 1:
                    sys.exit()
            elif currentClass == 4 and task_cue == 0:
                SendID(',601')
                if FIN == 1:
                    sys.exit()
            elif currentClass == 5 and task_cue == 0:
                SendID(',701')
                if FIN == 1:
                    sys.exit()
            #        sendTiD(7711)
            elif currentClass == 6 and task_cue == 0:
                SendID(',801')
                if FIN == 1:
                    sys.exit()
            elif currentClass == 7 and task_cue == 0:
                SendID(',1101')
                if FIN == 1:
                    sys.exit()
            elif currentClass == 8 and task_cue == 0:
                SendID(',1201')
                if FIN == 1:
                    sys.exit()
            #        sendTiD(7711)
            elif currentClass == 9 and task_cue == 0:
                SendID(',1301')
                if FIN == 1:
                    sys.exit()
            elif currentClass == 10 and task_cue == 0:
                SendID(',1401')
                if FIN == 1:
                    sys.exit()
            #        sendTiD(7711)
            elif currentClass == 11 and task_cue == 0:
                SendID(',1501')
                if FIN == 1:
                    sys.exit()
            elif currentClass == 12 and task_cue == 0:
                SendID(',1601')
                if FIN == 1:
                    sys.exit()

        fflag = 1

        context = globals().copy()
        context.update(locals())

        print("Entering main loop")
        while True:
            step_size = (0.5 * Bigger_rectangle_width - bar_width * 0.5) * (time.time() - prevTime) / taskTime
            y_bar = Bigger_rectangle_Y - step_size
            delta_height_2 = bar_width + step_size
            
            # re-draw the interface
            if fflag:
                class_to_color_image = {
                    1:  (upGreen,     IM_FLEXION_MET),
                    2:  (upOrange,    IM_EXTENSION_MET),
                    3:  (upAqua,      IM_FLEXION_PHA),
                    4:  (upPink,      IM_EXTENSION_PHA),
                    5:  (upRed,       IM_ADDUCTION_MET),
                    6:  (upyellow,    IM_ABDUCTION_MET),
                    7:  (upBrown,     IM_POINTING),
                    8:  (upGoldenrod, IM_FINGER_3),
                    9:  (uplightcoral,IM_FINGER_2),
                    10: (upOlivedrab, IM_MIDDLE_FINGER),
                    11: (upPeachpuff, IM_RING_FINGER),
                    12: (upPink2,     IM_PINKIE_FINGER)
                }
                
                color, image = class_to_color_image.get(currentClass, (None, None))
                context      = globals().copy()
                context.update(locals())
                draw_image_with_arrow_ff(color,image,context)
                fflag = 0

            pygame.draw.rect(screen, bigRecColor,     (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height, Bigger_rectangle_height_new), 0)  # third direction bar
            pygame.draw.rect(screen, bigRecEdgeColor, (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height, Bigger_rectangle_height_new), Bigthickness)  # edges of the rectangle (third)
            pygame.draw.rect(screen, barColor,        (initial_x_new, y_bar, bar_width, delta_height_2))  # draw up bar


            context = globals().copy()
            context.update(locals())

            class_to_image = {
                1:  IM_FLEXION_MET,
                2:  IM_EXTENSION_MET,
                3:  IM_FLEXION_PHA,
                4:  IM_EXTENSION_PHA,
                5:  IM_ADDUCTION_MET,
                6:  IM_ABDUCTION_MET,
                7:  IM_POINTING,
                8:  IM_FINGER_3,
                9:  IM_FINGER_2,
                10: IM_MIDDLE_FINGER,
                11: IM_RING_FINGER,
                12: IM_PINKIE_FINGER
            }

            image = class_to_image[currentClass]
            draw_task_image(image, context)

            pygame.draw.polygon(screen, arrowColor, (point1, point2, point3))
            pygame.display.update()

            # Stopping criteria based on taskTime that is set in a0_configFile.py
            if (time.time() - prevTime >= taskTime):
                class_to_send_id = {1: ',302', 2: ',402', 3: ',502', 4: ',602', 5: ',702', 6: ',802', 9: ',1102', 10: ',1202', 11: ',1302', 12: ',1402', 13: ',1502', 14: ',1602'}
                
                if currentClass in class_to_send_id:
                    SendID(class_to_send_id[currentClass])

                pygame.draw.rect(screen, bigRecColor, (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height, Bigger_rectangle_height_new), 0)  # third direction bar
                pygame.draw.rect(screen, bigRecEdgeColor, (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height, Bigger_rectangle_height_new), Bigthickness)  # edges of the rectangle (third)
                pygame.draw.rect(screen, barColor, (initial_x_new, initial_y, bar_width, bar_width), thickness)  # draw the bar
                pygame.draw.rect(screen, barColor, (initial_x_new, initial_y, bar_width, bar_width), thickness)  # draw the bar
                pygame.draw.rect(screen, barColor, (initial_x_new, initial_y, bar_width, bar_width))  # up bar

                context = globals().copy()
                context.update(locals())
                
                f_bleep = {
                    1: lambda:  bleep_arrow(IM_FLEXION_MET, context),
                    2: lambda:  bleep_arrow(IM_EXTENSION_MET, context),
                    3: lambda:  bleep_arrow(IM_FLEXION_PHA, context),
                    4: lambda:  bleep_arrow(IM_EXTENSION_PHA, context),
                    5: lambda:  bleep_arrow(IM_ADDUCTION_MET, context),
                    6: lambda:  bleep_arrow(IM_ABDUCTION_MET, context),
                    7: lambda:  bleep_arrow(IM_POINTING, context),
                    8: lambda:  bleep_arrow(IM_FINGER_3, context),
                    9: lambda:  bleep_arrow(IM_FINGER_2, context),
                    10: lambda: bleep_arrow(IM_MIDDLE_FINGER, context),
                    11: lambda: bleep_arrow(IM_RING_FINGER, context),
                    12: lambda: bleep_arrow(IM_PINKIE_FINGER, context)
                }
                f_bleep.get(currentClass)()
                pygame.display.update()
                time.sleep(resultTime)
                SendID(',2001')
                break

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # pygame.quit
                        sys.exit()

        task_cue = 0
        screen.fill(black)
        pygame.display.update()

                # <<<<<< REST >>>>>>
        time.sleep(restTime + random.random())
    end()

def SendID(Trigg):
    global TEMP

    TEMP = str(Trigg)

def end():
    global VAR
    VAR = 3

def SerialComunication():

    global TEMP
    global FIN
    global EXIT_ON_SERIAL

    try:
        ser = serial.Serial(arduino_port, baud)
        FIN = 0
    except SerialException:
        print("¡¡ERROR COMMUNICATION SERIAL!!")
        FIN = 0 # Changed to 0 so it does not stop
        if EXIT_ON_SERIAL:
            sys.exit()
            
    #ser = serial.Serial(arduino_port, baud)
    print("Connected to Arduino port:" + arduino_port)
    print("Created file")

    # display the data to the terminal
    if EXIT_ON_SERIAL:
        getData = str(ser.readline())
    else:
        getData = str([0,0,0])

    data = getData[2:][:-6] + TEMP
    TEMP = ',0'
    print(data)

    # add the data to the file
    file = open(fileName, "a")  # append the data to the file
    file.write(data + "\\n")  # write data with a newline

    file.close()

    # samples = 14000  # how many samples to collect
    print_labels = False
    line = 0  # start at 0 because our header is 0 (not real data)
    while VAR < 2:
        # incoming = ser.read(9999)
        # if len(incoming) > 0:
        if print_labels:
            if line == 0:
                print("Printing Column Headers")
            else:
                print("Line " + str(line) + ": writing...")
        
        if EXIT_ON_SERIAL:
            getData = str(ser.readline())
        else:
            getData = str([0,0,0])
            
        data = getData[2:][:-5] + TEMP
        TEMP = ',0'
        print(data)

        file = open(fileName, "a")
        file.write(data + "\n")  # write data with a newline
        line = line + 1

    print("Data collection complete!")
    file.close()

if __name__ == '__main__':
    if EXIT_ON_SERIAL == True:
        executor = ThreadPoolExecutor(max_workers=3)

        executor.submit(SerialComunication)
        executor.submit(visualinterface)
    else:
        visualinterface()