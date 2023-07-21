
print("Nombre del archivo")
archivo = input()
fileName = archivo + ".csv"

import serial
from serial import SerialException
import sys
import os
dirP = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
# #print(dirP + '/4_ref_other')
sys.path.append(dirP + '/z1_ref_other/0_lib')
Complete_trial = 0


import pygame
import time

import pyautogui
import math


from CONFIG import *
from concurrent.futures import ThreadPoolExecutor

VAR = 1
FIN = 1
TEMP = 0

EXIT_ON_SERIAL = False

arduino_port = "COM4"
baud = 230400

screen = pyautogui.size()

screen_width = screen[0]
screen_height = screen[1]
screen_width_o = screen[0]
screen_height_o = screen[1]
scaling_factor = 1

# Normalize everything to the size of the bar as determined below
screen_width = int(screen_width / scaling_factor)
screen_height = int(screen_height / scaling_factor)
screen = pygame.display.set_mode((screen_width, screen_height))  # Setting up the screen size
pygame.display.set_caption('Motor Imagery Experiment')
screen_height = min(screen_width, screen_height)
screen_width = min(screen_height, screen_width)

spaceToBeLeft = 2.5 * int(screen_width * 0.1)  # space to be left at the edges of the rectangle to fit the
# images at the sides (2*original bar width)
Bigger_rectangle_width = screen_width - 2 * spaceToBeLeft
bar_width = 0.5 * Bigger_rectangle_width

# Load flexion and extension images, scale them, and place them at the side of the rectangle
flexion_image = pygame.image.load('flexion.png')
image_scaling_flexion = spaceToBeLeft / flexion_image.get_rect().size[0]
flexion_image = pygame.transform.scale(flexion_image, (
    int(spaceToBeLeft), int(flexion_image.get_rect().size[1] * image_scaling_flexion)))
(flexion_image_x, flexion_image_y) = (0, screen_height / 2 - flexion_image.get_rect().size[1] / 2)
extension_image = pygame.image.load('extension.png')
image_scaling_extension = spaceToBeLeft / extension_image.get_rect().size[0]
extension_image = pygame.transform.scale(extension_image, (
    int(spaceToBeLeft), int(extension_image.get_rect().size[1] * image_scaling_extension)))
(extension_image_x, extension_image_y) = (
    screen_width - spaceToBeLeft, screen_height / 2 - extension_image.get_rect().size[1] / 2)
# make the height of the bar consistent with the size of wrist in the images
bar_height = int(flexion_image.get_rect().size[1] * 0.2086701)

# setting the dimensions of the rectangle in which the bar moves right/left
Bigger_rectangle_height = bar_height
Bigger_rectangle_X = screen_width_o / 2 - Bigger_rectangle_width / 2
Bigger_rectangle_Y = screen_height / 2 - bar_height / 2 + bar_height * 2
Bigthickness = 3  # thickness of the edge lines for the rectangle and other shapes

# color setting
black = (0, 0, 0)
bigRecEdgeColor = (185, 188, 181)  # FES:(130,92,63) #
bigRecColor = (46, 52, 54)  # FES:(198,160,131) #
barColor = bigRecEdgeColor
white = (229, 229, 229)
yellow = (255, 255, 0)
# rightRed = (203, 0, 0)
# leftBlue = (52, 101, 163)
upGreen = (0, 128, 0)
upOrange = (219, 71, 0)
upAqua = (0, 193, 179)
upPink = (191, 0, 96)
upRed = (170, 0, 0)
upyellow = (255, 255, 0)
upAquamarine = (127, 255, 212)
upBlueviolet = (138, 43, 226)
upBrown = (165, 42, 42)
upGoldenrod = (218, 165, 32)
uplightcoral = (240, 128, 128)
upOlivedrab = (107, 142, 35)
upPeachpuff = (255, 218, 185)
upPink2 = (255, 192, 203)

# Initial position of the bar in the middle of the rectangle:
initial_x = screen_width - bar_width
initial_y = Bigger_rectangle_Y
centerOfScreen = (screen_width_o / 2, screen_height / 2)
initial_x_2 = centerOfScreen[0]
thickness = 0

# time.sleep(5)
# correct for cue arrows by increasing the width of the bar so it is aligned with the arrow as it reaches the end of
# the task
arrowMidShift = (bar_height / 2)
bar_width = bar_width + arrowMidShift
initial_x = initial_x - arrowMidShift / 2

# new rectangle dimensions
Bigger_rectangle_new_X = (Bigger_rectangle_X + (Bigger_rectangle_width / 2)) - (Bigger_rectangle_height / 2)
Bigger_rectangle_new_Y = (Bigger_rectangle_Y + Bigger_rectangle_height) - (Bigger_rectangle_width / 2
                                                                           + Bigger_rectangle_height / 2)
Bigger_rectangle_height_new = Bigger_rectangle_width / 2 + Bigger_rectangle_height / 2

# new 'down' rectangle dimensions (not used here)
Down_rectangle_X = Bigger_rectangle_new_X
Down_rectangle_Y = Bigger_rectangle_new_Y + (Bigger_rectangle_height_new - Bigger_rectangle_height)

# new bar
bar_height_new = Bigger_rectangle_height
bar_width_new = bar_height
initial_y_new = Bigger_rectangle_new_Y + (Bigger_rectangle_height_new / 2)
initial_x_new = Bigger_rectangle_new_X

######## Arrow dimensions goes here
ArrowTipWidth = bar_width / 3.5
ArrowRectangleHeight = Bigger_rectangle_height
ArrowRectangleWidth = 0.5 * ArrowTipWidth

upArrowStartingX = Bigger_rectangle_new_X
upArrowStartingY = Bigger_rectangle_new_Y - ArrowRectangleWidth
upArrowRectangleHeight = ArrowRectangleWidth
upArrowRectangleWidth = ArrowRectangleHeight

point1UpArrow = (centerOfScreen[0], upArrowStartingY - ArrowTipWidth)
point2UpArrow = (centerOfScreen[0] - ArrowTipWidth / math.sqrt(3), upArrowStartingY)
point3UpArrow = (centerOfScreen[0] + ArrowTipWidth / math.sqrt(3),upArrowStartingY)

# adjustment to bar_width for drawing the bars
bar_width = Bigger_rectangle_height

# changes in horizontal rectangle to create two rectangles
Bigger_rectangle_width_adj = Bigger_rectangle_width / 2 + bar_width / 2
Bigger_rectangle_X_adj = Bigger_rectangle_X + (Bigger_rectangle_width / 2 - bar_width / 2)

IM_FLEXION_MET = pygame.image.load("neu1.jfif").convert()
IM_FLEXION_MET = pygame.transform.scale(IM_FLEXION_MET, (624, 577))
IM_EXTENSION_MET = pygame.image.load("neu2.jfif").convert()
IM_EXTENSION_MET = pygame.transform.scale(IM_EXTENSION_MET, (624, 619.19))
IM_FLEXION_PHA = pygame.image.load("neu7.jfif").convert()
IM_FLEXION_PHA = pygame.transform.scale(IM_FLEXION_PHA, (624, 636.70))
IM_EXTENSION_PHA = pygame.image.load("neu8.jfif").convert()
IM_EXTENSION_PHA = pygame.transform.scale(IM_EXTENSION_PHA, (624, 636.70))
IM_ADDUCTION_MET = pygame.image.load("neu6.jfif").convert()
IM_ADDUCTION_MET = pygame.transform.scale(IM_ADDUCTION_MET, (624, 590.60))
IM_ABDUCTION_MET = pygame.image.load("neu5.jfif").convert()
IM_ABDUCTION_MET = pygame.transform.scale(IM_ABDUCTION_MET, (624, 577))
# IM_PRONATION = pygame.image.load("neu7.jfif").convert()
# IM_PRONATION = pygame.transform.scale(IM_PRONATION, (624, 577))
# IM_SUPINATION = pygame.image.load("neu8.jfif").convert()
# IM_SUPINATION = pygame.transform.scale(IM_SUPINATION, (624, 577))
IM_POINTING = pygame.image.load("neu9.jfif").convert()
IM_POINTING = pygame.transform.scale(IM_POINTING, (624, 577))
IM_FINGER_3 = pygame.image.load("neu10.jfif").convert()
IM_FINGER_3 = pygame.transform.scale(IM_FINGER_3, (624, 577))
IM_FINGER_2 = pygame.image.load("neu11.jfif").convert()
IM_FINGER_2 = pygame.transform.scale(IM_FINGER_2, (624, 577))
IM_MIDDLE_FINGER = pygame.image.load("neu12.jfif").convert()
IM_MIDDLE_FINGER = pygame.transform.scale(IM_MIDDLE_FINGER, (624, 577))
IM_RING_FINGER = pygame.image.load("neu13.jfif").convert()
IM_RING_FINGER = pygame.transform.scale(IM_RING_FINGER, (624, 577))
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

# pygame.display.update()
    time.sleep(ExperimentConfigureTime)  # display the interface for a certain period that is set in the i0_configFile.py file

    screen.fill(black)

    #prevTime = time.time()  # record time at beginning of the trial

    arrowColor = white

    for trial in all_arrays:  # trial = +1 (extension)/-1(flexion)

        currentClass = trial
        if currentClass == 1:
            arrowColor = upGreen

        elif currentClass == 2:
            arrowColor = upOrange

        elif currentClass == 3:
            arrowColor = upAqua

        elif currentClass == 4:
            arrowColor = upPink

        elif currentClass == 5:
            arrowColor = upRed

        elif currentClass == 6:
            arrowColor = upyellow

        # if currentClass == 7:
        #     arrowColor = upAquamarine
        #
        # if currentClass == 8:
        #     arrowColor = upBlueviolet

        elif currentClass == 7:
            arrowColor = upBrown

        elif currentClass == 8:
            arrowColor = upGoldenrod

        elif currentClass == 9:
            arrowColor = uplightcoral

        elif currentClass == 10:
            arrowColor = upOlivedrab

        elif currentClass == 11:
            arrowColor = upPeachpuff

        elif currentClass == 12:
            arrowColor = upPink2

        print('Class of current trial: ', currentClass)

        if currentClass == 1:
            pygame.draw.rect(screen, upGreen,
                             (upArrowStartingX, upArrowStartingY, upArrowRectangleWidth, upArrowRectangleHeight),
                             0)  # Moving bar specs
            pygame.draw.polygon(screen, upGreen, (point1UpArrow, point2UpArrow, point3UpArrow))

        elif currentClass == 2:
            pygame.draw.rect(screen, upOrange,
                             (upArrowStartingX, upArrowStartingY, upArrowRectangleWidth, upArrowRectangleHeight),
                             0)  # Moving bar specs
            pygame.draw.polygon(screen, upOrange, (point1UpArrow, point2UpArrow, point3UpArrow))

        elif currentClass == 3:
            pygame.draw.rect(screen, upAqua,
                             (upArrowStartingX, upArrowStartingY, upArrowRectangleWidth, upArrowRectangleHeight),
                             0)  # Moving bar specs
            pygame.draw.polygon(screen, upAqua, (point1UpArrow, point2UpArrow, point3UpArrow))

        elif currentClass == 4:
            pygame.draw.rect(screen, upPink,
                             (upArrowStartingX, upArrowStartingY, upArrowRectangleWidth, upArrowRectangleHeight),
                             0)  # Moving bar specs
            pygame.draw.polygon(screen, upPink, (point1UpArrow, point2UpArrow, point3UpArrow))

        elif currentClass == 5:
            pygame.draw.rect(screen, upRed,
                             (upArrowStartingX, upArrowStartingY, upArrowRectangleWidth, upArrowRectangleHeight),
                             0)  # Moving bar specs
            pygame.draw.polygon(screen, upRed, (point1UpArrow, point2UpArrow, point3UpArrow))
        elif currentClass == 6:
            pygame.draw.rect(screen, upyellow,
                             (upArrowStartingX, upArrowStartingY, upArrowRectangleWidth, upArrowRectangleHeight),
                             0)  # Moving bar specs
            pygame.draw.polygon(screen, upyellow, (point1UpArrow, point2UpArrow, point3UpArrow))

        # if currentClass == 7:
        #     pygame.draw.rect(screen, upAquamarine,
        #                      (upArrowStartingX, upArrowStartingY, upArrowRectangleWidth, upArrowRectangleHeight),
        #                      0)  # Moving bar specs
        #     pygame.draw.polygon(screen, upAquamarine, (point1UpArrow, point2UpArrow, point3UpArrow))
        #
        # if currentClass == 8:
        #     pygame.draw.rect(screen, upBlueviolet,
        #                      (upArrowStartingX, upArrowStartingY, upArrowRectangleWidth, upArrowRectangleHeight),
        #                      0)  # Moving bar specs
        #     pygame.draw.polygon(screen, upBlueviolet, (point1UpArrow, point2UpArrow, point3UpArrow))

        elif currentClass == 7:
            pygame.draw.rect(screen, upBrown,
                             (upArrowStartingX, upArrowStartingY, upArrowRectangleWidth, upArrowRectangleHeight),
                             0)  # Moving bar specs
            pygame.draw.polygon(screen, upBrown, (point1UpArrow, point2UpArrow, point3UpArrow))

        elif currentClass == 8:
            pygame.draw.rect(screen, upGoldenrod,
                             (upArrowStartingX, upArrowStartingY, upArrowRectangleWidth, upArrowRectangleHeight),
                             0)  # Moving bar specs
            pygame.draw.polygon(screen, upGoldenrod, (point1UpArrow, point2UpArrow, point3UpArrow))

        elif currentClass == 9:
            pygame.draw.rect(screen, uplightcoral,
                             (upArrowStartingX, upArrowStartingY, upArrowRectangleWidth, upArrowRectangleHeight),
                             0)  # Moving bar specs
            pygame.draw.polygon(screen, uplightcoral, (point1UpArrow, point2UpArrow, point3UpArrow))

        elif currentClass == 10:
            pygame.draw.rect(screen, upOlivedrab,
                             (upArrowStartingX, upArrowStartingY, upArrowRectangleWidth, upArrowRectangleHeight),
                             0)  # Moving bar specs
            pygame.draw.polygon(screen, upOlivedrab, (point1UpArrow, point2UpArrow, point3UpArrow))

        elif currentClass == 11:
            pygame.draw.rect(screen, upPeachpuff,
                             (upArrowStartingX, upArrowStartingY, upArrowRectangleWidth, upArrowRectangleHeight),
                             0)  # Moving bar specs
            pygame.draw.polygon(screen, upPeachpuff, (point1UpArrow, point2UpArrow, point3UpArrow))

        elif currentClass == 12:
            pygame.draw.rect(screen, upPink2,
                             (upArrowStartingX, upArrowStartingY, upArrowRectangleWidth, upArrowRectangleHeight),
                             0)  # Moving bar specs
            pygame.draw.polygon(screen, upPink2, (point1UpArrow, point2UpArrow, point3UpArrow))

        SendID(',2000')
        if FIN == 1:
            sys.exit()

        pygame.draw.rect(screen, bigRecColor,
                         (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,
                          Bigger_rectangle_height_new), 0)  # third direction bar
        pygame.draw.rect(screen, bigRecEdgeColor,
                         (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,
                          Bigger_rectangle_height_new),
                         Bigthickness)  # edges of the rectangle (third)

        pygame.draw.rect(screen, barColor, (initial_x_new, Down_rectangle_Y, bar_width, bar_width))
        pygame.draw.rect(screen, barColor, (initial_x_new, Down_rectangle_Y, bar_width, bar_width))
        pygame.draw.rect(screen, barColor, (initial_x_new, Down_rectangle_Y, bar_width, bar_width))

        pygame.display.update()
        # new code for cue timing

        # pygame.display.update()
        # point1 = 0
        # point2 = 0
        # point3 = 0
        if currentClass == 1:
            screen.blit(IM_FLEXION_MET, (150, 150))
            pygame.draw.rect(screen, arrowColor, (
                centerOfScreen[0] - bar_height / 6, Bigger_rectangle_Y + bar_height / 2, 2 * bar_height / 6,
                Bigger_rectangle_height / 2), thickness)  # Arrow Specs
            point1 = (centerOfScreen[0], Bigger_rectangle_Y)
            point2 = (centerOfScreen[0] - 0.35 * bar_height, Bigger_rectangle_Y + bar_height / 2)
            point3 = (centerOfScreen[0] + 0.35 * bar_height, Bigger_rectangle_Y + bar_height / 2)
        elif currentClass == 2:
            screen.blit(IM_EXTENSION_MET, (150, 150))
            pygame.draw.rect(screen, arrowColor, (
                centerOfScreen[0] - bar_height / 6, Bigger_rectangle_Y + bar_height / 2, 2 * bar_height / 6,
                Bigger_rectangle_height / 2), thickness)  # Arrow Specs
            point1 = (centerOfScreen[0], Bigger_rectangle_Y)
            point2 = (centerOfScreen[0] - 0.35 * bar_height, Bigger_rectangle_Y + bar_height / 2)
            point3 = (centerOfScreen[0] + 0.35 * bar_height, Bigger_rectangle_Y + bar_height / 2)
        elif currentClass == 3:
            screen.blit(IM_FLEXION_PHA, (150, 150))
            pygame.draw.rect(screen, arrowColor, (
                centerOfScreen[0] - bar_height / 6, Bigger_rectangle_Y + bar_height / 2, 2 * bar_height / 6,
                Bigger_rectangle_height / 2), thickness)  # Arrow Specs
            point1 = (centerOfScreen[0], Bigger_rectangle_Y)
            point2 = (centerOfScreen[0] - 0.35 * bar_height, Bigger_rectangle_Y + bar_height / 2)
            point3 = (centerOfScreen[0] + 0.35 * bar_height, Bigger_rectangle_Y + bar_height / 2)
        elif currentClass == 4:
            screen.blit(IM_EXTENSION_PHA, (150, 150))
            pygame.draw.rect(screen, arrowColor, (
                centerOfScreen[0] - bar_height / 6, Bigger_rectangle_Y + bar_height / 2, 2 * bar_height / 6,
                Bigger_rectangle_height / 2), thickness)  # Arrow Specs
            point1 = (centerOfScreen[0], Bigger_rectangle_Y)
            point2 = (centerOfScreen[0] - 0.35 * bar_height, Bigger_rectangle_Y + bar_height / 2)
            point3 = (centerOfScreen[0] + 0.35 * bar_height, Bigger_rectangle_Y + bar_height / 2)
        elif currentClass == 5:
            screen.blit(IM_ADDUCTION_MET, (150, 150))
            pygame.draw.rect(screen, arrowColor, (
                centerOfScreen[0] - bar_height / 6, Bigger_rectangle_Y + bar_height / 2, 2 * bar_height / 6,
                Bigger_rectangle_height / 2), thickness)  # Arrow Specs
            point1 = (centerOfScreen[0], Bigger_rectangle_Y)
            point2 = (centerOfScreen[0] - 0.35 * bar_height, Bigger_rectangle_Y + bar_height / 2)
            point3 = (centerOfScreen[0] + 0.35 * bar_height, Bigger_rectangle_Y + bar_height / 2)
        elif currentClass == 6:
            screen.blit(IM_ABDUCTION_MET, (150, 150))
            pygame.draw.rect(screen, arrowColor, (
                centerOfScreen[0] - bar_height / 6, Bigger_rectangle_Y + bar_height / 2, 2 * bar_height / 6,
                Bigger_rectangle_height / 2), thickness)  # Arrow Specs
            point1 = (centerOfScreen[0], Bigger_rectangle_Y)
            point2 = (centerOfScreen[0] - 0.35 * bar_height, Bigger_rectangle_Y + bar_height / 2)
            point3 = (centerOfScreen[0] + 0.35 * bar_height, Bigger_rectangle_Y + bar_height / 2)
        # elif currentClass == 7:
        #     screen.blit(IM_PRONATION, (150, 150))
        #     pygame.draw.rect(screen, arrowColor, (
        #         centerOfScreen[0] - bar_height / 6, Bigger_rectangle_Y + bar_height / 2, 2 * bar_height / 6,
        #         Bigger_rectangle_height / 2), thickness)  # Arrow Specs
        #     point1 = (centerOfScreen[0], Bigger_rectangle_Y)
        #     point2 = (centerOfScreen[0] - 0.35 * bar_height, Bigger_rectangle_Y + bar_height / 2)
        #     point3 = (centerOfScreen[0] + 0.35 * bar_height, Bigger_rectangle_Y + bar_height / 2)
        # elif currentClass == 8:
        #     screen.blit(IM_SUPINATION, (150, 150))
        #     pygame.draw.rect(screen, arrowColor, (
        #         centerOfScreen[0] - bar_height / 6, Bigger_rectangle_Y + bar_height / 2, 2 * bar_height / 6,
        #         Bigger_rectangle_height / 2), thickness)  # Arrow Specs
        #     point1 = (centerOfScreen[0], Bigger_rectangle_Y)
        #     point2 = (centerOfScreen[0] - 0.35 * bar_height, Bigger_rectangle_Y + bar_height / 2)
        #     point3 = (centerOfScreen[0] + 0.35 * bar_height, Bigger_rectangle_Y + bar_height / 2)
        elif currentClass == 7:
            screen.blit(IM_POINTING, (150, 150))
            pygame.draw.rect(screen, arrowColor, (
                centerOfScreen[0] - bar_height / 6, Bigger_rectangle_Y + bar_height / 2, 2 * bar_height / 6,
                Bigger_rectangle_height / 2), thickness)  # Arrow Specs
            point1 = (centerOfScreen[0], Bigger_rectangle_Y)
            point2 = (centerOfScreen[0] - 0.35 * bar_height, Bigger_rectangle_Y + bar_height / 2)
            point3 = (centerOfScreen[0] + 0.35 * bar_height, Bigger_rectangle_Y + bar_height / 2)
        elif currentClass == 8:
            screen.blit(IM_FINGER_3, (150, 150))
            pygame.draw.rect(screen, arrowColor, (
                centerOfScreen[0] - bar_height / 6, Bigger_rectangle_Y + bar_height / 2, 2 * bar_height / 6,
                Bigger_rectangle_height / 2), thickness)  # Arrow Specs
            point1 = (centerOfScreen[0], Bigger_rectangle_Y)
            point2 = (centerOfScreen[0] - 0.35 * bar_height, Bigger_rectangle_Y + bar_height / 2)
            point3 = (centerOfScreen[0] + 0.35 * bar_height, Bigger_rectangle_Y + bar_height / 2)
        elif currentClass == 9:
            screen.blit(IM_FINGER_2, (150, 150))
            pygame.draw.rect(screen, arrowColor, (
                centerOfScreen[0] - bar_height / 6, Bigger_rectangle_Y + bar_height / 2, 2 * bar_height / 6,
                Bigger_rectangle_height / 2), thickness)  # Arrow Specs
            point1 = (centerOfScreen[0], Bigger_rectangle_Y)
            point2 = (centerOfScreen[0] - 0.35 * bar_height, Bigger_rectangle_Y + bar_height / 2)
            point3 = (centerOfScreen[0] + 0.35 * bar_height, Bigger_rectangle_Y + bar_height / 2)
        elif currentClass == 10:
            screen.blit(IM_MIDDLE_FINGER, (150, 150))
            pygame.draw.rect(screen, arrowColor, (
                centerOfScreen[0] - bar_height / 6, Bigger_rectangle_Y + bar_height / 2, 2 * bar_height / 6,
                Bigger_rectangle_height / 2), thickness)  # Arrow Specs
            point1 = (centerOfScreen[0], Bigger_rectangle_Y)
            point2 = (centerOfScreen[0] - 0.35 * bar_height, Bigger_rectangle_Y + bar_height / 2)
            point3 = (centerOfScreen[0] + 0.35 * bar_height, Bigger_rectangle_Y + bar_height / 2)
        elif currentClass == 11:
            screen.blit(IM_RING_FINGER, (150, 150))
            pygame.draw.rect(screen, arrowColor, (
                centerOfScreen[0] - bar_height / 6, Bigger_rectangle_Y + bar_height / 2, 2 * bar_height / 6,
                Bigger_rectangle_height / 2), thickness)  # Arrow Specs
            point1 = (centerOfScreen[0], Bigger_rectangle_Y)
            point2 = (centerOfScreen[0] - 0.35 * bar_height, Bigger_rectangle_Y + bar_height / 2)
            point3 = (centerOfScreen[0] + 0.35 * bar_height, Bigger_rectangle_Y + bar_height / 2)
        else:
            screen.blit(IM_PINKIE_FINGER, (150, 150))
            pygame.draw.rect(screen, arrowColor, (
                centerOfScreen[0] - bar_height / 6, Bigger_rectangle_Y + bar_height / 2, 2 * bar_height / 6,
                Bigger_rectangle_height / 2), thickness)  # Arrow Specs
            point1 = (centerOfScreen[0], Bigger_rectangle_Y)
            point2 = (centerOfScreen[0] - 0.35 * bar_height, Bigger_rectangle_Y + bar_height / 2)
            point3 = (centerOfScreen[0] + 0.35 * bar_height, Bigger_rectangle_Y + bar_height / 2)

        pygame.draw.polygon(screen, arrowColor, (point1, point2, point3))
        pygame.display.update()

        # COMENTAMOS ESTO
        if currentClass == 1:
            SendID(',300')
        #        SendID(',769')  # send Event CUE: 769 to LOOP to indicate flexion cue
        elif currentClass == 2:
            SendID(',400')
        #        SendID(',770') # send Event CUE: 770 to LOOP to indicate extension cue
        elif currentClass == 3:
            SendID(',500')
        elif currentClass == 4:
            SendID(',600')
        #        SendID(',770') # send Event CUE: 770 to LOOP to indicate extension cue
        elif currentClass == 5:
            SendID(',700')
        #        SendID(',771')
        elif currentClass == 6:
            SendID(',800')
        # if currentClass == 7:
        #     SendID(',900')
        # #        SendID(',769')  # send Event CUE: 769 to LOOP to indicate flexion cue
        # if currentClass == 8:
        #     SendID(',1000')
        #        SendID(',770') # send Event CUE: 770 to LOOP to indicate extension cue
        elif currentClass == 7:
            SendID(',1100')
        elif currentClass == 8:
            SendID(',1200')
        #        SendID(',770') # send Event CUE: 770 to LOOP to indicate extension cue
        elif currentClass == 9:
            SendID(',1300')
        #        SendID(',771')
        elif currentClass == 10:
            SendID(',1400')
        elif currentClass == 11:
            SendID(',1500')
        #        SendID(',771')
        elif currentClass == 12:
            SendID(',1600')

        time.sleep(cueTime)  # wait for the period determined in a0_configFile.py

        screen.fill(black)  # clear display

        prevTime = time.time()
        task_cue = 0
        if currentClass == 1 and task_cue == 0:
            SendID(',301')
            if FIN == 1:
                sys.exit()
        #        sendTiD(7691)  # send Event: 7691 to LOOP to indicate start of flexion task
        # task_cue = 1  # send this cue only once at the beginning of the task
        elif currentClass == 2 and task_cue == 0:
            SendID(',401')
            if FIN == 1:
                sys.exit()
        #        sendTiD(7701)  # send Event CUE: 7701 to LOOP to indicate start of extension task
        # task_cue = 1  # send this cue only once at the beginning of the task
        elif currentClass == 3 and task_cue == 0:
            SendID(',501')
            if FIN == 1:
                sys.exit()
        elif currentClass == 4 and task_cue == 0:
            SendID(',601')
            if FIN == 1:
                sys.exit()
        #        sendTiD(7701)  # send Event CUE: 7701 to LOOP to indicate start of extension task
        # task_cue = 1  # send this cue only once at the beginning of the task
        elif currentClass == 5 and task_cue == 0:
            SendID(',701')
            if FIN == 1:
                sys.exit()
        #        sendTiD(7711)
        elif currentClass == 6 and task_cue == 0:
            SendID(',801')
            if FIN == 1:
                sys.exit()
        # task_cue = 1
        # elif currentClass == 7 and task_cue == 0:
        #     SendID(',901')
        #     if FIN == 1:
        #         sys.exit()
        # #        sendTiD(7701)  # send Event CUE: 7701 to LOOP to indicate start of extension task
        # # task_cue = 1  # send this cue only once at the beginning of the task
        # elif currentClass == 8 and task_cue == 0:
        #     SendID(',1001')
        #     if FIN == 1:
        #         sys.exit()
        elif currentClass == 7 and task_cue == 0:
            SendID(',1101')
            if FIN == 1:
                sys.exit()
        #        sendTiD(7701)  # send Event CUE: 7701 to LOOP to indicate start of extension task
        # task_cue = 1  # send this cue only once at the beginning of the task
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

        while True:

            # x_bar = initial_x_new
            # y_bar = Bigger_rectangle_Y
            # delta_width = bar_width
            # delta_width_1 = bar_width
            # delta_height_2 = bar_width

        # find how much the bar must move to the left based on how much time has passed
            if currentClass == 1:
                step_size = (0.5 * Bigger_rectangle_width - bar_width * 0.5) * (time.time() - prevTime) / taskTime
                y_bar = Bigger_rectangle_Y - step_size
                delta_height_2 = bar_width + step_size
            elif currentClass == 2:
                 step_size = (0.5 * Bigger_rectangle_width - bar_width * 0.5) * (time.time() - prevTime) / taskTime
                 y_bar = Bigger_rectangle_Y - step_size
                 delta_height_2 = bar_width + step_size
            elif currentClass == 3:
                 step_size = (0.5 * Bigger_rectangle_width - bar_width * 0.5) * (time.time() - prevTime) / taskTime
                 y_bar = Bigger_rectangle_Y - step_size
                 delta_height_2 = bar_width + step_size
            elif currentClass == 4:
                 step_size = (0.5 * Bigger_rectangle_width - bar_width * 0.5) * (time.time() - prevTime) / taskTime
                 y_bar = Bigger_rectangle_Y - step_size
                 delta_height_2 = bar_width + step_size
            elif currentClass == 5:
                 step_size = (0.5 * Bigger_rectangle_width - bar_width * 0.5) * (time.time() - prevTime) / taskTime
                 y_bar = Bigger_rectangle_Y - step_size
                 delta_height_2 = bar_width + step_size
            elif currentClass == 6:
                 step_size = (0.5 * Bigger_rectangle_width - bar_width * 0.5) * (time.time() - prevTime) / taskTime
                 y_bar = Bigger_rectangle_Y - step_size
                 delta_height_2 = bar_width + step_size
            # elif currentClass == 7:
            #      step_size = (0.5 * Bigger_rectangle_width - bar_width * 0.5) * (time.time() - prevTime) / taskTime
            #      y_bar = Bigger_rectangle_Y - step_size
            #      delta_height_2 = bar_width + step_size
            # elif currentClass == 8:
            #      step_size = (0.5 * Bigger_rectangle_width - bar_width * 0.5) * (time.time() - prevTime) / taskTime
            #      y_bar = Bigger_rectangle_Y - step_size
            #      delta_height_2 = bar_width + step_size
            elif currentClass == 7:
                 step_size = (0.5 * Bigger_rectangle_width - bar_width * 0.5) * (time.time() - prevTime) / taskTime
                 y_bar = Bigger_rectangle_Y - step_size
                 delta_height_2 = bar_width + step_size
            elif currentClass == 8:
                 step_size = (0.5 * Bigger_rectangle_width - bar_width * 0.5) * (time.time() - prevTime) / taskTime
                 y_bar = Bigger_rectangle_Y - step_size
                 delta_height_2 = bar_width + step_size
            elif currentClass == 9:
                 step_size = (0.5 * Bigger_rectangle_width - bar_width * 0.5) * (time.time() - prevTime) / taskTime
                 y_bar = Bigger_rectangle_Y - step_size
                 delta_height_2 = bar_width + step_size
            elif currentClass == 10:
                 step_size = (0.5 * Bigger_rectangle_width - bar_width * 0.5) * (time.time() - prevTime) / taskTime
                 y_bar = Bigger_rectangle_Y - step_size
                 delta_height_2 = bar_width + step_size
            elif currentClass == 11:
                 step_size = (0.5 * Bigger_rectangle_width - bar_width * 0.5) * (time.time() - prevTime) / taskTime
                 y_bar = Bigger_rectangle_Y - step_size
                 delta_height_2 = bar_width + step_size
            else:
                 step_size = (0.5 * Bigger_rectangle_width - bar_width * 0.5) * (time.time() - prevTime) / taskTime
                 y_bar = Bigger_rectangle_Y - step_size
                 delta_height_2 = bar_width + step_size
        # re-draw the interface
            if fflag:
                if currentClass == 1:
                    screen.blit(IM_FLEXION_MET, (150, 150))
                    pygame.draw.rect(screen, upGreen,
                                     (upArrowStartingX, upArrowStartingY, upArrowRectangleWidth, upArrowRectangleHeight),
                                     0)  # Moving bar specs
                    pygame.draw.polygon(screen, upGreen, (point1UpArrow, point2UpArrow, point3UpArrow))

                elif currentClass == 2:
                    screen.blit(IM_EXTENSION_MET, (150, 150))
                    pygame.draw.rect(screen, upOrange,
                                     (upArrowStartingX, upArrowStartingY, upArrowRectangleWidth, upArrowRectangleHeight),
                                     0)  # Moving bar specs
                    pygame.draw.polygon(screen, upOrange, (point1UpArrow, point2UpArrow, point3UpArrow))

                elif currentClass == 3:
                    screen.blit(IM_FLEXION_PHA, (150, 150))
                    pygame.draw.rect(screen, upAqua,
                                     (upArrowStartingX, upArrowStartingY, upArrowRectangleWidth, upArrowRectangleHeight),
                                     0)  # Moving bar specs
                    pygame.draw.polygon(screen, upAqua, (point1UpArrow, point2UpArrow, point3UpArrow))

                elif currentClass == 4:
                    screen.blit(IM_EXTENSION_PHA, (150, 150))
                    pygame.draw.rect(screen, upPink,
                                     (upArrowStartingX, upArrowStartingY, upArrowRectangleWidth, upArrowRectangleHeight),
                                     0)  # Moving bar specs
                    pygame.draw.polygon(screen, upPink, (point1UpArrow, point2UpArrow, point3UpArrow))

                elif currentClass == 5:
                    screen.blit(IM_ADDUCTION_MET, (150, 150))
                    pygame.draw.rect(screen, upRed,
                                     (upArrowStartingX, upArrowStartingY, upArrowRectangleWidth, upArrowRectangleHeight),
                                     0)  # Moving bar specs
                    pygame.draw.polygon(screen, upRed, (point1UpArrow, point2UpArrow, point3UpArrow))

                elif currentClass == 6:
                    screen.blit(IM_ABDUCTION_MET, (150, 150))
                    pygame.draw.rect(screen, upyellow,
                                     (upArrowStartingX, upArrowStartingY, upArrowRectangleWidth, upArrowRectangleHeight),
                                     0)  # Moving bar specs
                    pygame.draw.polygon(screen, upyellow, (point1UpArrow, point2UpArrow, point3UpArrow))

                # if currentClass == 7:
                #     screen.blit(IM_PRONATION, (150, 150))
                #     pygame.draw.rect(screen, upAquamarine,
                #                      (upArrowStartingX, upArrowStartingY, upArrowRectangleWidth, upArrowRectangleHeight),
                #                      0)  # Moving bar specs
                #     pygame.draw.polygon(screen, upAquamarine, (point1UpArrow, point2UpArrow, point3UpArrow))
                #
                # if currentClass == 8:
                #     screen.blit(IM_SUPINATION, (150, 150))
                #     pygame.draw.rect(screen, upBlueviolet,
                #                      (upArrowStartingX, upArrowStartingY, upArrowRectangleWidth, upArrowRectangleHeight),
                #                      0)  # Moving bar specs
                #     pygame.draw.polygon(screen, upBlueviolet, (point1UpArrow, point2UpArrow, point3UpArrow))

                elif currentClass == 7:
                    screen.blit(IM_POINTING, (150, 150))
                    pygame.draw.rect(screen, upBrown,
                                     (upArrowStartingX, upArrowStartingY, upArrowRectangleWidth, upArrowRectangleHeight),
                                     0)  # Moving bar specs
                    pygame.draw.polygon(screen, upBrown, (point1UpArrow, point2UpArrow, point3UpArrow))

                elif currentClass == 8:
                    screen.blit(IM_FINGER_3, (150, 150))
                    pygame.draw.rect(screen, upGoldenrod,
                                     (upArrowStartingX, upArrowStartingY, upArrowRectangleWidth, upArrowRectangleHeight),
                                     0)  # Moving bar specs
                    pygame.draw.polygon(screen, upGoldenrod, (point1UpArrow, point2UpArrow, point3UpArrow))

                elif currentClass == 9:
                    screen.blit(IM_FINGER_2, (150, 150))
                    pygame.draw.rect(screen, uplightcoral,
                                     (upArrowStartingX, upArrowStartingY, upArrowRectangleWidth, upArrowRectangleHeight),
                                     0)  # Moving bar specs
                    pygame.draw.polygon(screen, uplightcoral, (point1UpArrow, point2UpArrow, point3UpArrow))

                elif currentClass == 10:
                    screen.blit(IM_MIDDLE_FINGER, (150, 150))
                    pygame.draw.rect(screen, upOlivedrab,
                                     (upArrowStartingX, upArrowStartingY, upArrowRectangleWidth, upArrowRectangleHeight),
                                     0)  # Moving bar specs
                    pygame.draw.polygon(screen, upOlivedrab, (point1UpArrow, point2UpArrow, point3UpArrow))

                elif currentClass == 11:
                    screen.blit(IM_RING_FINGER, (150, 150))
                    pygame.draw.rect(screen, upPeachpuff,
                                     (upArrowStartingX, upArrowStartingY, upArrowRectangleWidth, upArrowRectangleHeight),
                                     0)  # Moving bar specs
                    pygame.draw.polygon(screen, upPeachpuff, (point1UpArrow, point2UpArrow, point3UpArrow))

                elif currentClass == 12:
                    screen.blit(IM_PINKIE_FINGER, (150, 150))
                    pygame.draw.rect(screen, upPink2,
                                     (upArrowStartingX, upArrowStartingY, upArrowRectangleWidth, upArrowRectangleHeight),
                                     0)  # Moving bar specs
                    pygame.draw.polygon(screen, upPink2, (point1UpArrow, point2UpArrow, point3UpArrow))
                fflag = 0

            pygame.draw.rect(screen, bigRecColor,
                             (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,
                              Bigger_rectangle_height_new), 0)  # third direction bar
            pygame.draw.rect(screen, bigRecEdgeColor,
                             (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,
                              Bigger_rectangle_height_new),
                             Bigthickness)  # edges of the rectangle (third)

            pygame.draw.rect(screen, barColor, (initial_x_new, y_bar, bar_width, delta_height_2))  # draw up bar

        # Drawing arrow polygon to point towards required task (right for extension and left for flexion)
            if currentClass == 1:
                screen.blit(IM_FLEXION_MET, (150, 150))
                pygame.draw.rect(screen, arrowColor, (
                    centerOfScreen[0] - bar_height / 6, Bigger_rectangle_Y + bar_height / 2, 2 * bar_height / 6,
                    Bigger_rectangle_height / 2), thickness)  # Arrow Specs
            elif currentClass == 2:
                screen.blit(IM_EXTENSION_MET, (150, 150))
                pygame.draw.rect(screen, arrowColor, (
                    centerOfScreen[0] - bar_height / 6, Bigger_rectangle_Y + bar_height / 2, 2 * bar_height / 6,
                    Bigger_rectangle_height / 2), thickness)  # Arrow Specs
            elif currentClass == 3:
                screen.blit(IM_FLEXION_PHA, (150, 150))
                pygame.draw.rect(screen, arrowColor, (
                    centerOfScreen[0] - bar_height / 6, Bigger_rectangle_Y + bar_height / 2, 2 * bar_height / 6,
                    Bigger_rectangle_height / 2), thickness)  # Arrow Specs
            elif currentClass == 4:
                screen.blit(IM_EXTENSION_PHA, (150, 150))
                pygame.draw.rect(screen, arrowColor, (
                    centerOfScreen[0] - bar_height / 6, Bigger_rectangle_Y + bar_height / 2, 2 * bar_height / 6,
                    Bigger_rectangle_height / 2), thickness)  # Arrow Specs
            elif currentClass == 5:
                screen.blit(IM_ADDUCTION_MET, (150, 150))
                pygame.draw.rect(screen, arrowColor, (
                    centerOfScreen[0] - bar_height / 6, Bigger_rectangle_Y + bar_height / 2, 2 * bar_height / 6,
                    Bigger_rectangle_height / 2), thickness)  # Arrow Specs
            elif currentClass == 6:
                screen.blit(IM_ABDUCTION_MET, (150, 150))
                pygame.draw.rect(screen, arrowColor, (
                    centerOfScreen[0] - bar_height / 6, Bigger_rectangle_Y + bar_height / 2, 2 * bar_height / 6,
                    Bigger_rectangle_height / 2), thickness)  # Arrow Specs
            # elif currentClass == 7:
            #     screen.blit(IM_PRONATION, (150, 150))
            #     pygame.draw.rect(screen, arrowColor, (
            #         centerOfScreen[0] - bar_height / 6, Bigger_rectangle_Y + bar_height / 2, 2 * bar_height / 6,
            #         Bigger_rectangle_height / 2), thickness)  # Arrow Specs
            # elif currentClass == 8:
            #     screen.blit(IM_SUPINATION, (150, 150))
            #     pygame.draw.rect(screen, arrowColor, (
            #         centerOfScreen[0] - bar_height / 6, Bigger_rectangle_Y + bar_height / 2, 2 * bar_height / 6,
            #         Bigger_rectangle_height / 2), thickness)  # Arrow Specs
            elif currentClass == 7:
                screen.blit(IM_POINTING, (150, 150))
                pygame.draw.rect(screen, arrowColor, (
                    centerOfScreen[0] - bar_height / 6, Bigger_rectangle_Y + bar_height / 2, 2 * bar_height / 6,
                    Bigger_rectangle_height / 2), thickness)  # Arrow Specs
            elif currentClass == 8:
                screen.blit(IM_FINGER_3, (150, 150))
                pygame.draw.rect(screen, arrowColor, (
                    centerOfScreen[0] - bar_height / 6, Bigger_rectangle_Y + bar_height / 2, 2 * bar_height / 6,
                    Bigger_rectangle_height / 2), thickness)  # Arrow Specs
            elif currentClass == 9:
                screen.blit(IM_FINGER_2, (150, 150))
                pygame.draw.rect(screen, arrowColor, (
                    centerOfScreen[0] - bar_height / 6, Bigger_rectangle_Y + bar_height / 2, 2 * bar_height / 6,
                    Bigger_rectangle_height / 2), thickness)  # Arrow Specs
            elif currentClass == 10:
                screen.blit(IM_MIDDLE_FINGER, (150, 150))
                pygame.draw.rect(screen, arrowColor, (
                    centerOfScreen[0] - bar_height / 6, Bigger_rectangle_Y + bar_height / 2, 2 * bar_height / 6,
                    Bigger_rectangle_height / 2), thickness)  # Arrow Specs
            elif currentClass == 11:
                screen.blit(IM_RING_FINGER, (150, 150))
                pygame.draw.rect(screen, arrowColor, (
                    centerOfScreen[0] - bar_height / 6, Bigger_rectangle_Y + bar_height / 2, 2 * bar_height / 6,
                    Bigger_rectangle_height / 2), thickness)  # Arrow Specs
            else:
                screen.blit(IM_PINKIE_FINGER, (150, 150))
                pygame.draw.rect(screen, arrowColor, (
                    centerOfScreen[0] - bar_height / 6, Bigger_rectangle_Y + bar_height / 2, 2 * bar_height / 6,
                    Bigger_rectangle_height / 2), thickness)  # Arrow Specs

            pygame.draw.polygon(screen, arrowColor, (point1, point2, point3))
            pygame.display.update()

        # Stopping criteria based on taskTime that is set in a0_configFile.py
            if (time.time() - prevTime >= taskTime):
            # COMENTAMOS ESTO

                if currentClass == 1:
                    SendID(',302')
                # send Event CUE: 7692 to LOOP to indicate end of flexion task and start of result view time
                elif currentClass == 2:
                    SendID(',402')
                # send Event CUE: 7702 to LOOP to indicate end of extension task and start of result view time
                elif currentClass == 3:
                    SendID(',502')
                elif currentClass == 4:
                    SendID(',602')
                # send Event CUE: 7702 to LOOP to indicate end of extension task and start of result view time
                elif currentClass == 5:
                    SendID(',702')
                elif currentClass == 6:
                    SendID(',802')
                # elif currentClass == 7:
                #     SendID(',902')
                # # send Event CUE: 7702 to LOOP to indicate end of extension task and start of result view time
                # elif currentClass == 8:
                #     SendID(',1002')
                elif currentClass == 9:
                    SendID(',1102')
                # send Event CUE: 7702 to LOOP to indicate end of extension task and start of result view time
                elif currentClass == 10:
                    SendID(',1202')
                elif currentClass == 11:
                    SendID(',1302')
                elif currentClass == 12:
                    SendID(',1402')
                elif currentClass == 13:
                    SendID(',1502')
                elif currentClass == 14:
                    SendID(',1602')

            #                sendTiD(7712)
            # <<<<<< RESULT CUE >>>>>>

                pygame.draw.rect(screen, bigRecColor,
                                 (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,
                                  Bigger_rectangle_height_new), 0)  # third direction bar
                pygame.draw.rect(screen, bigRecEdgeColor,
                                 (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,
                                  Bigger_rectangle_height_new),
                                 Bigthickness)  # edges of the rectangle (third)
                pygame.draw.rect(screen, barColor, (initial_x_new, initial_y, bar_width, bar_width),
                                 thickness)  # draw the bar
                pygame.draw.rect(screen, barColor, (initial_x_new, initial_y, bar_width, bar_width),
                                 thickness)  # draw the bar
                pygame.draw.rect(screen, barColor, (initial_x_new, initial_y, bar_width, bar_width))  # up bar

                if currentClass == 1:
                    screen.blit(IM_FLEXION_MET, (150, 150))
                    pygame.draw.rect(screen, upGreen,
                                     (upArrowStartingX, upArrowStartingY, upArrowRectangleWidth, upArrowRectangleHeight),
                                     0)  # Moving bar specs

                    pygame.draw.polygon(screen, upGreen, (point1UpArrow, point2UpArrow, point3UpArrow))

                    pygame.draw.rect(screen, arrowColor,
                                     (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,
                                      Bigger_rectangle_height_new),
                                     0)  # fill bar with the class color
                    pygame.draw.rect(screen, bigRecEdgeColor,
                                     (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,
                                      Bigger_rectangle_height_new),
                                     Bigthickness)  # mark the edge of the bar with original color

                    pygame.draw.rect(screen, bigRecEdgeColor,
                                     (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,
                                      Bigger_rectangle_height_new),
                                     Bigthickness)  # Bigger edge mark

                    pygame.draw.circle(screen, arrowColor,
                                       (int(centerOfScreen[0]), int(Bigger_rectangle_Y + bar_height / 2)),
                                       int(bar_height * 0.8),
                                       0)  # draw a colored filled circle to show result
                    pygame.draw.circle(screen, bigRecEdgeColor,
                                       (int(centerOfScreen[0]), int(Bigger_rectangle_Y + bar_height / 2)),
                                       int(bar_height * 0.8), Bigthickness)  # highlight the edge of the circle

                    # Drawing arrow polygon
                    pygame.draw.rect(screen, white, (
                        centerOfScreen[0] - bar_height / 6, Bigger_rectangle_Y + bar_height / 2, 2 * bar_height / 6,
                        Bigger_rectangle_height / 2), thickness)  # Arrow Specs  # Arrow Specs
                    pygame.draw.polygon(screen, white, (point1, point2, point3))
                elif currentClass == 2:
                    screen.blit(IM_EXTENSION_MET, (150, 150))
                    pygame.draw.rect(screen, upOrange,
                                     (upArrowStartingX, upArrowStartingY, upArrowRectangleWidth, upArrowRectangleHeight),
                                     0)  # Moving bar specs

                    pygame.draw.polygon(screen, upOrange, (point1UpArrow, point2UpArrow, point3UpArrow))
                    pygame.draw.rect(screen, arrowColor,
                                     (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,
                                      Bigger_rectangle_height_new),
                                     0)  # fill bar with the class color
                    pygame.draw.rect(screen, bigRecEdgeColor,
                                     (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,
                                      Bigger_rectangle_height_new),
                                     Bigthickness)  # mark the edge of the bar with original color

                    pygame.draw.rect(screen, bigRecEdgeColor,
                                     (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,
                                      Bigger_rectangle_height_new),
                                     Bigthickness)  # Bigger edge mark

                    pygame.draw.circle(screen, arrowColor,
                                       (int(centerOfScreen[0]), int(Bigger_rectangle_Y + bar_height / 2)),
                                       int(bar_height * 0.8),
                                       0)  # draw a colored filled circle to show result
                    pygame.draw.circle(screen, bigRecEdgeColor,
                                       (int(centerOfScreen[0]), int(Bigger_rectangle_Y + bar_height / 2)),
                                       int(bar_height * 0.8), Bigthickness)  # highlight the edge of the circle

                    # Drawing arrow polygon
                    pygame.draw.rect(screen, white, (
                        centerOfScreen[0] - bar_height / 6, Bigger_rectangle_Y + bar_height / 2, 2 * bar_height / 6,
                        Bigger_rectangle_height / 2), thickness)  # Arrow Specs  # Arrow Specs
                    pygame.draw.polygon(screen, white, (point1, point2, point3))
                elif currentClass == 3:
                    screen.blit(IM_FLEXION_PHA, (150, 150))
                    pygame.draw.rect(screen, upAqua,
                                     (upArrowStartingX, upArrowStartingY, upArrowRectangleWidth, upArrowRectangleHeight),
                                     0)  # Moving bar specs

                    pygame.draw.polygon(screen, upAqua, (point1UpArrow, point2UpArrow, point3UpArrow))
                    pygame.draw.rect(screen, arrowColor,
                                     (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,
                                      Bigger_rectangle_height_new),
                                     0)  # fill bar with the class color
                    pygame.draw.rect(screen, bigRecEdgeColor,
                                     (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,
                                      Bigger_rectangle_height_new),
                                     Bigthickness)  # mark the edge of the bar with original color

                    pygame.draw.rect(screen, bigRecEdgeColor,
                                     (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,
                                      Bigger_rectangle_height_new),
                                     Bigthickness)  # Bigger edge mark

                    pygame.draw.circle(screen, arrowColor,
                                       (int(centerOfScreen[0]), int(Bigger_rectangle_Y + bar_height / 2)),
                                       int(bar_height * 0.8),
                                       0)  # draw a colored filled circle to show result
                    pygame.draw.circle(screen, bigRecEdgeColor,
                                       (int(centerOfScreen[0]), int(Bigger_rectangle_Y + bar_height / 2)),
                                       int(bar_height * 0.8), Bigthickness)  # highlight the edge of the circle

                    # Drawing arrow polygon
                    pygame.draw.rect(screen, white, (
                        centerOfScreen[0] - bar_height / 6, Bigger_rectangle_Y + bar_height / 2, 2 * bar_height / 6,
                        Bigger_rectangle_height / 2), thickness)  # Arrow Specs  # Arrow Specs
                    pygame.draw.polygon(screen, white, (point1, point2, point3))
                elif currentClass == 4:
                    screen.blit(IM_EXTENSION_PHA, (150, 150))
                    pygame.draw.rect(screen, upPink,
                                     (upArrowStartingX, upArrowStartingY, upArrowRectangleWidth, upArrowRectangleHeight),
                                     0)  # Moving bar specs

                    pygame.draw.polygon(screen, upPink, (point1UpArrow, point2UpArrow, point3UpArrow))
                    pygame.draw.rect(screen, arrowColor,
                                     (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,
                                      Bigger_rectangle_height_new),
                                     0)  # fill bar with the class color
                    pygame.draw.rect(screen, bigRecEdgeColor,
                                     (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,
                                      Bigger_rectangle_height_new),
                                     Bigthickness)  # mark the edge of the bar with original color

                    pygame.draw.rect(screen, bigRecEdgeColor,
                                     (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,
                                      Bigger_rectangle_height_new),
                                     Bigthickness)  # Bigger edge mark

                    pygame.draw.circle(screen, arrowColor,
                                       (int(centerOfScreen[0]), int(Bigger_rectangle_Y + bar_height / 2)),
                                       int(bar_height * 0.8),
                                       0)  # draw a colored filled circle to show result
                    pygame.draw.circle(screen, bigRecEdgeColor,
                                       (int(centerOfScreen[0]), int(Bigger_rectangle_Y + bar_height / 2)),
                                       int(bar_height * 0.8), Bigthickness)  # highlight the edge of the circle

                    # Drawing arrow polygon
                    pygame.draw.rect(screen, white, (
                        centerOfScreen[0] - bar_height / 6, Bigger_rectangle_Y + bar_height / 2, 2 * bar_height / 6,
                        Bigger_rectangle_height / 2), thickness)  # Arrow Specs  # Arrow Specs
                    pygame.draw.polygon(screen, white, (point1, point2, point3))
                elif currentClass == 5:
                    screen.blit(IM_ADDUCTION_MET, (150, 150))
                    pygame.draw.rect(screen, upRed,
                                     (upArrowStartingX, upArrowStartingY, upArrowRectangleWidth, upArrowRectangleHeight),
                                     0)  # Moving bar specs

                    pygame.draw.polygon(screen, upRed, (point1UpArrow, point2UpArrow, point3UpArrow))
                    pygame.draw.rect(screen, arrowColor,
                                     (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,
                                      Bigger_rectangle_height_new),
                                     0)  # fill bar with the class color
                    pygame.draw.rect(screen, bigRecEdgeColor,
                                     (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,
                                      Bigger_rectangle_height_new),
                                     Bigthickness)  # mark the edge of the bar with original color

                    pygame.draw.rect(screen, bigRecEdgeColor,
                                     (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,
                                      Bigger_rectangle_height_new),
                                     Bigthickness)  # Bigger edge mark

                    pygame.draw.circle(screen, arrowColor,
                                       (int(centerOfScreen[0]), int(Bigger_rectangle_Y + bar_height / 2)),
                                       int(bar_height * 0.8),
                                       0)  # draw a colored filled circle to show result
                    pygame.draw.circle(screen, bigRecEdgeColor,
                                       (int(centerOfScreen[0]), int(Bigger_rectangle_Y + bar_height / 2)),
                                       int(bar_height * 0.8), Bigthickness)  # highlight the edge of the circle

                    # Drawing arrow polygon
                    pygame.draw.rect(screen, white, (
                        centerOfScreen[0] - bar_height / 6, Bigger_rectangle_Y + bar_height / 2, 2 * bar_height / 6,
                        Bigger_rectangle_height / 2), thickness)  # Arrow Specs  # Arrow Specs
                    pygame.draw.polygon(screen, white, (point1, point2, point3))
                elif currentClass == 6:
                    screen.blit(IM_ABDUCTION_MET, (150, 150))
                    pygame.draw.rect(screen, upyellow,
                                     (upArrowStartingX, upArrowStartingY, upArrowRectangleWidth, upArrowRectangleHeight),
                                     0)  # Moving bar specs

                    pygame.draw.polygon(screen, upyellow, (point1UpArrow, point2UpArrow, point3UpArrow))
                    pygame.draw.rect(screen, arrowColor,
                                     (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,
                                      Bigger_rectangle_height_new),
                                     0)  # fill bar with the class color
                    pygame.draw.rect(screen, bigRecEdgeColor,
                                     (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,
                                      Bigger_rectangle_height_new),
                                     Bigthickness)  # mark the edge of the bar with original color

                    pygame.draw.rect(screen, bigRecEdgeColor,
                                     (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,
                                      Bigger_rectangle_height_new),
                                     Bigthickness)  # Bigger edge mark

                    pygame.draw.circle(screen, arrowColor,
                                       (int(centerOfScreen[0]), int(Bigger_rectangle_Y + bar_height / 2)),
                                       int(bar_height * 0.8),
                                       0)  # draw a colored filled circle to show result
                    pygame.draw.circle(screen, bigRecEdgeColor,
                                       (int(centerOfScreen[0]), int(Bigger_rectangle_Y + bar_height / 2)),
                                       int(bar_height * 0.8), Bigthickness)  # highlight the edge of the circle

                    # Drawing arrow polygon
                    pygame.draw.rect(screen, white, (
                        centerOfScreen[0] - bar_height / 6, Bigger_rectangle_Y + bar_height / 2, 2 * bar_height / 6,
                        Bigger_rectangle_height / 2), thickness)  # Arrow Specs  # Arrow Specs
                    pygame.draw.polygon(screen, white, (point1, point2, point3))
                # elif currentClass == 7:
                #     screen.blit(IM_PRONATION, (150, 150))
                #     pygame.draw.rect(screen, upAquamarine,
                #                      (upArrowStartingX, upArrowStartingY, upArrowRectangleWidth, upArrowRectangleHeight),
                #                      0)  # Moving bar specs
                #
                #     pygame.draw.polygon(screen, upAquamarine, (point1UpArrow, point2UpArrow, point3UpArrow))
                #     pygame.draw.rect(screen, arrowColor,
                #                      (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,
                #                       Bigger_rectangle_height_new),
                #                      0)  # fill bar with the class color
                #     pygame.draw.rect(screen, bigRecEdgeColor,
                #                      (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,
                #                       Bigger_rectangle_height_new),
                #                      Bigthickness)  # mark the edge of the bar with original color
                #
                #     pygame.draw.rect(screen, bigRecEdgeColor,
                #                      (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,
                #                       Bigger_rectangle_height_new),
                #                      Bigthickness)  # Bigger edge mark
                #
                #     pygame.draw.circle(screen, arrowColor,
                #                        (int(centerOfScreen[0]), int(Bigger_rectangle_Y + bar_height / 2)),
                #                        int(bar_height * 0.8),
                #                        0)  # draw a colored filled circle to show result
                #     pygame.draw.circle(screen, bigRecEdgeColor,
                #                        (int(centerOfScreen[0]), int(Bigger_rectangle_Y + bar_height / 2)),
                #                        int(bar_height * 0.8), Bigthickness)  # highlight the edge of the circle
                #
                #     # Drawing arrow polygon
                #     pygame.draw.rect(screen, white, (
                #         centerOfScreen[0] - bar_height / 6, Bigger_rectangle_Y + bar_height / 2, 2 * bar_height / 6,
                #         Bigger_rectangle_height / 2), thickness)  # Arrow Specs  # Arrow Specs
                #     pygame.draw.polygon(screen, white, (point1, point2, point3))
                # elif currentClass == 8:
                #     screen.blit(IM_SUPINATION, (150, 150))
                #     pygame.draw.rect(screen, upBlueviolet,
                #                      (upArrowStartingX, upArrowStartingY, upArrowRectangleWidth, upArrowRectangleHeight),
                #                      0)  # Moving bar specs
                #
                #     pygame.draw.polygon(screen, upBlueviolet, (point1UpArrow, point2UpArrow, point3UpArrow))
                #     pygame.draw.rect(screen, arrowColor,
                #                      (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,
                #                       Bigger_rectangle_height_new),
                #                      0)  # fill bar with the class color
                #     pygame.draw.rect(screen, bigRecEdgeColor,
                #                      (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,
                #                       Bigger_rectangle_height_new),
                #                      Bigthickness)  # mark the edge of the bar with original color
                #
                #     pygame.draw.rect(screen, bigRecEdgeColor,
                #                      (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,
                #                       Bigger_rectangle_height_new),
                #                      Bigthickness)  # Bigger edge mark
                #
                #     pygame.draw.circle(screen, arrowColor,
                #                        (int(centerOfScreen[0]), int(Bigger_rectangle_Y + bar_height / 2)),
                #                        int(bar_height * 0.8),
                #                        0)  # draw a colored filled circle to show result
                #     pygame.draw.circle(screen, bigRecEdgeColor,
                #                        (int(centerOfScreen[0]), int(Bigger_rectangle_Y + bar_height / 2)),
                #                        int(bar_height * 0.8), Bigthickness)  # highlight the edge of the circle
                #
                #     # Drawing arrow polygon
                #     pygame.draw.rect(screen, white, (
                #         centerOfScreen[0] - bar_height / 6, Bigger_rectangle_Y + bar_height / 2, 2 * bar_height / 6,
                #         Bigger_rectangle_height / 2), thickness)  # Arrow Specs  # Arrow Specs
                #     pygame.draw.polygon(screen, white, (point1, point2, point3))
                elif currentClass == 7:
                    screen.blit(IM_POINTING, (150, 150))
                    pygame.draw.rect(screen, upBrown,
                                     (upArrowStartingX, upArrowStartingY, upArrowRectangleWidth, upArrowRectangleHeight),
                                     0)  # Moving bar specs

                    pygame.draw.polygon(screen, upBrown, (point1UpArrow, point2UpArrow, point3UpArrow))
                    pygame.draw.rect(screen, arrowColor,
                                     (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,
                                      Bigger_rectangle_height_new),
                                     0)  # fill bar with the class color
                    pygame.draw.rect(screen, bigRecEdgeColor,
                                     (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,
                                      Bigger_rectangle_height_new),
                                     Bigthickness)  # mark the edge of the bar with original color

                    pygame.draw.rect(screen, bigRecEdgeColor,
                                     (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,
                                      Bigger_rectangle_height_new),
                                     Bigthickness)  # Bigger edge mark

                    pygame.draw.circle(screen, arrowColor,
                                       (int(centerOfScreen[0]), int(Bigger_rectangle_Y + bar_height / 2)),
                                       int(bar_height * 0.8),
                                       0)  # draw a colored filled circle to show result
                    pygame.draw.circle(screen, bigRecEdgeColor,
                                       (int(centerOfScreen[0]), int(Bigger_rectangle_Y + bar_height / 2)),
                                       int(bar_height * 0.8), Bigthickness)  # highlight the edge of the circle

                    # Drawing arrow polygon
                    pygame.draw.rect(screen, white, (
                        centerOfScreen[0] - bar_height / 6, Bigger_rectangle_Y + bar_height / 2, 2 * bar_height / 6,
                        Bigger_rectangle_height / 2), thickness)  # Arrow Specs  # Arrow Specs
                    pygame.draw.polygon(screen, white, (point1, point2, point3))
                elif currentClass == 8:
                    screen.blit(IM_FINGER_3, (150, 150))
                    pygame.draw.rect(screen, upGoldenrod,
                                     (upArrowStartingX, upArrowStartingY, upArrowRectangleWidth, upArrowRectangleHeight),
                                     0)  # Moving bar specs

                    pygame.draw.polygon(screen, upGoldenrod, (point1UpArrow, point2UpArrow, point3UpArrow))
                    pygame.draw.rect(screen, arrowColor,
                                     (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,
                                      Bigger_rectangle_height_new),
                                     0)  # fill bar with the class color
                    pygame.draw.rect(screen, bigRecEdgeColor,
                                     (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,
                                      Bigger_rectangle_height_new),
                                     Bigthickness)  # mark the edge of the bar with original color

                    pygame.draw.rect(screen, bigRecEdgeColor,
                                     (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,
                                      Bigger_rectangle_height_new),
                                     Bigthickness)  # Bigger edge mark

                    pygame.draw.circle(screen, arrowColor,
                                       (int(centerOfScreen[0]), int(Bigger_rectangle_Y + bar_height / 2)),
                                       int(bar_height * 0.8),
                                       0)  # draw a colored filled circle to show result
                    pygame.draw.circle(screen, bigRecEdgeColor,
                                       (int(centerOfScreen[0]), int(Bigger_rectangle_Y + bar_height / 2)),
                                       int(bar_height * 0.8), Bigthickness)  # highlight the edge of the circle

                    # Drawing arrow polygon
                    pygame.draw.rect(screen, white, (
                        centerOfScreen[0] - bar_height / 6, Bigger_rectangle_Y + bar_height / 2, 2 * bar_height / 6,
                        Bigger_rectangle_height / 2), thickness)  # Arrow Specs  # Arrow Specs
                    pygame.draw.polygon(screen, white, (point1, point2, point3))
                elif currentClass == 9:
                    screen.blit(IM_FINGER_2, (150, 150))
                    pygame.draw.rect(screen, uplightcoral,
                                     (upArrowStartingX, upArrowStartingY, upArrowRectangleWidth, upArrowRectangleHeight),
                                     0)  # Moving bar specs

                    pygame.draw.polygon(screen, uplightcoral, (point1UpArrow, point2UpArrow, point3UpArrow))
                    pygame.draw.rect(screen, arrowColor,
                                     (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,
                                      Bigger_rectangle_height_new),
                                     0)  # fill bar with the class color
                    pygame.draw.rect(screen, bigRecEdgeColor,
                                     (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,
                                      Bigger_rectangle_height_new),
                                     Bigthickness)  # mark the edge of the bar with original color

                    pygame.draw.rect(screen, bigRecEdgeColor,
                                     (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,
                                      Bigger_rectangle_height_new),
                                     Bigthickness)  # Bigger edge mark

                    pygame.draw.circle(screen, arrowColor,
                                       (int(centerOfScreen[0]), int(Bigger_rectangle_Y + bar_height / 2)),
                                       int(bar_height * 0.8),
                                       0)  # draw a colored filled circle to show result
                    pygame.draw.circle(screen, bigRecEdgeColor,
                                       (int(centerOfScreen[0]), int(Bigger_rectangle_Y + bar_height / 2)),
                                       int(bar_height * 0.8), Bigthickness)  # highlight the edge of the circle

                    # Drawing arrow polygon
                    pygame.draw.rect(screen, white, (
                        centerOfScreen[0] - bar_height / 6, Bigger_rectangle_Y + bar_height / 2, 2 * bar_height / 6,
                        Bigger_rectangle_height / 2), thickness)  # Arrow Specs  # Arrow Specs
                    pygame.draw.polygon(screen, white, (point1, point2, point3))
                elif currentClass == 10:
                    screen.blit(IM_MIDDLE_FINGER, (150, 150))
                    pygame.draw.rect(screen, upOlivedrab,
                                     (upArrowStartingX, upArrowStartingY, upArrowRectangleWidth, upArrowRectangleHeight),
                                     0)  # Moving bar specs

                    pygame.draw.polygon(screen, upOlivedrab, (point1UpArrow, point2UpArrow, point3UpArrow))
                    pygame.draw.rect(screen, arrowColor,
                                     (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,
                                      Bigger_rectangle_height_new),
                                     0)  # fill bar with the class color
                    pygame.draw.rect(screen, bigRecEdgeColor,
                                     (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,
                                      Bigger_rectangle_height_new),
                                     Bigthickness)  # mark the edge of the bar with original color

                    pygame.draw.rect(screen, bigRecEdgeColor,
                                     (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,
                                      Bigger_rectangle_height_new),
                                     Bigthickness)  # Bigger edge mark

                    pygame.draw.circle(screen, arrowColor,
                                       (int(centerOfScreen[0]), int(Bigger_rectangle_Y + bar_height / 2)),
                                       int(bar_height * 0.8),
                                       0)  # draw a colored filled circle to show result
                    pygame.draw.circle(screen, bigRecEdgeColor,
                                       (int(centerOfScreen[0]), int(Bigger_rectangle_Y + bar_height / 2)),
                                       int(bar_height * 0.8), Bigthickness)  # highlight the edge of the circle

                    # Drawing arrow polygon
                    pygame.draw.rect(screen, white, (
                        centerOfScreen[0] - bar_height / 6, Bigger_rectangle_Y + bar_height / 2, 2 * bar_height / 6,
                        Bigger_rectangle_height / 2), thickness)  # Arrow Specs  # Arrow Specs
                    pygame.draw.polygon(screen, white, (point1, point2, point3))
                elif currentClass == 11:
                    screen.blit(IM_RING_FINGER, (150, 150))
                    pygame.draw.rect(screen, upPeachpuff,
                                     (upArrowStartingX, upArrowStartingY, upArrowRectangleWidth, upArrowRectangleHeight),
                                     0)  # Moving bar specs

                    pygame.draw.polygon(screen, upPeachpuff, (point1UpArrow, point2UpArrow, point3UpArrow))
                    pygame.draw.rect(screen, arrowColor,
                                     (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,
                                      Bigger_rectangle_height_new),
                                     0)  # fill bar with the class color
                    pygame.draw.rect(screen, bigRecEdgeColor,
                                     (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,
                                      Bigger_rectangle_height_new),
                                     Bigthickness)  # mark the edge of the bar with original color

                    pygame.draw.rect(screen, bigRecEdgeColor,
                                     (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,
                                      Bigger_rectangle_height_new),
                                     Bigthickness)  # Bigger edge mark

                    pygame.draw.circle(screen, arrowColor,
                                       (int(centerOfScreen[0]), int(Bigger_rectangle_Y + bar_height / 2)),
                                       int(bar_height * 0.8),
                                       0)  # draw a colored filled circle to show result
                    pygame.draw.circle(screen, bigRecEdgeColor,
                                       (int(centerOfScreen[0]), int(Bigger_rectangle_Y + bar_height / 2)),
                                       int(bar_height * 0.8), Bigthickness)  # highlight the edge of the circle

                    # Drawing arrow polygon
                    pygame.draw.rect(screen, white, (
                        centerOfScreen[0] - bar_height / 6, Bigger_rectangle_Y + bar_height / 2, 2 * bar_height / 6,
                        Bigger_rectangle_height / 2), thickness)  # Arrow Specs  # Arrow Specs
                    pygame.draw.polygon(screen, white, (point1, point2, point3))
                else:
                    screen.blit(IM_PINKIE_FINGER, (150, 150))
                    pygame.draw.rect(screen, upPink2,
                                     (upArrowStartingX, upArrowStartingY, upArrowRectangleWidth, upArrowRectangleHeight),
                                     0)  # Moving bar specs

                    pygame.draw.polygon(screen, upPink2, (point1UpArrow, point2UpArrow, point3UpArrow))
                    pygame.draw.rect(screen, arrowColor,
                                     (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,
                                      Bigger_rectangle_height_new),
                                     0)  # fill bar with the class color
                    pygame.draw.rect(screen, bigRecEdgeColor,
                                     (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,
                                      Bigger_rectangle_height_new),
                                     Bigthickness)  # mark the edge of the bar with original color

                    pygame.draw.rect(screen, bigRecEdgeColor,
                                     (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height,
                                      Bigger_rectangle_height_new),
                                     Bigthickness)  # Bigger edge mark

                    pygame.draw.circle(screen, arrowColor,
                                       (int(centerOfScreen[0]), int(Bigger_rectangle_Y + bar_height / 2)),
                                       int(bar_height * 0.8),
                                       0)  # draw a colored filled circle to show result
                    pygame.draw.circle(screen, bigRecEdgeColor,
                                       (int(centerOfScreen[0]), int(Bigger_rectangle_Y + bar_height / 2)),
                                       int(bar_height * 0.8), Bigthickness)  # highlight the edge of the circle

                    # Drawing arrow polygon
                    pygame.draw.rect(screen, white, (
                        centerOfScreen[0] - bar_height / 6, Bigger_rectangle_Y + bar_height / 2, 2 * bar_height / 6,
                        Bigger_rectangle_height / 2), thickness)  # Arrow Specs  # Arrow Specs
                    pygame.draw.polygon(screen, white, (point1, point2, point3))

                pygame.display.update()

                # COMENTAMOS ESTO
                time.sleep(resultTime)

                # sendTiD(1000)  # send Event CUE: 1000 to LOOP to indicate end of result view time
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

    executor = ThreadPoolExecutor(max_workers=3)

    executor.submit(SerialComunication)
    executor.submit(visualinterface)
