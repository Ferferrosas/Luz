import pygame
import time

def bleep_arrow(thumbnail,global_vars):
    
    screen                      = global_vars['screen']
    upArrowStartingX            = global_vars['upArrowStartingX']
    upArrowStartingY            = global_vars['upArrowStartingY']
    upArrowRectangleWidth       = global_vars['upArrowRectangleWidth']
    upArrowRectangleHeight      = global_vars['upArrowRectangleHeight']
    Bigger_rectangle_new_X      = global_vars['Bigger_rectangle_new_X']
    Bigger_rectangle_new_Y      = global_vars['Bigger_rectangle_new_Y']
    Bigger_rectangle_height     = global_vars['Bigger_rectangle_height']
    Bigger_rectangle_height_new = global_vars['Bigger_rectangle_height_new']
    bigRecEdgeColor             = global_vars['bigRecEdgeColor']
    arrowColor                  = global_vars['arrowColor']
    Bigthickness                = global_vars['Bigthickness']
    centerOfScreen              = global_vars['centerOfScreen']
    Bigger_rectangle_Y          = global_vars['Bigger_rectangle_Y']
    point1UpArrow               = global_vars['point1UpArrow']
    point2UpArrow               = global_vars['point2UpArrow']
    point3UpArrow               = global_vars['point3UpArrow']
    bar_height                  = global_vars['bar_height']

    negative_color              = (255 - arrowColor[0], 255 - arrowColor[1], 255 - arrowColor[2])

    screen.blit(thumbnail, (150, 150))
    pygame.draw.rect(screen, negative_color, (upArrowStartingX, upArrowStartingY, upArrowRectangleWidth, upArrowRectangleHeight), 0)  # Moving bar specs

    pygame.draw.polygon(screen, negative_color, (point1UpArrow, point2UpArrow, point3UpArrow))
    pygame.draw.rect(screen, arrowColor, (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height, Bigger_rectangle_height_new), 0)  # fill bar with the class color
    pygame.draw.rect(screen, bigRecEdgeColor, (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height, Bigger_rectangle_height_new), Bigthickness)  # mark the edge of the bar with original color

    pygame.draw.rect(screen, bigRecEdgeColor, (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height, Bigger_rectangle_height_new), Bigthickness)  # Bigger edge mark

    pygame.draw.circle(screen, arrowColor, (int(centerOfScreen[0]), int(Bigger_rectangle_Y + bar_height / 2)), int(bar_height * 0.8), 0)  # draw a colored filled circle to show result
    pygame.draw.circle(screen, bigRecEdgeColor, (int(centerOfScreen[0]), int(Bigger_rectangle_Y + bar_height / 2)), int(bar_height * 0.8), Bigthickness)  # highlight the edge of the circle

def draw_task_image(image, context):
    screen = context['screen']
    arrowColor = context['arrowColor']
    centerOfScreen = context['centerOfScreen']
    bar_height = context['bar_height']
    Bigger_rectangle_Y = context['Bigger_rectangle_Y']
    Bigger_rectangle_height = context['Bigger_rectangle_height']
    thickness = context['thickness']

    screen.blit(image, (150, 150))
    pygame.draw.rect(screen, arrowColor, (
        centerOfScreen[0] - bar_height / 6, Bigger_rectangle_Y + bar_height / 2, 2 * bar_height / 6,
        Bigger_rectangle_height / 2), thickness)  # Arrow Specs
    

def draw_image_with_arrow(image, context):
    screen = context['screen']
    screen.blit(image, (150, 150))
    pygame.draw.rect(screen, context['arrowColor'], (
        context['centerOfScreen'][0] - context['bar_height'] / 6, context['Bigger_rectangle_Y'] + context['bar_height'] / 2,
        2 * context['bar_height'] / 6, context['Bigger_rectangle_height'] / 2), context['thickness'])  # Arrow Specs

def draw_image_with_arrow_ff(color,image,context):
    screen                 = context['screen']
    upArrowStartingX       = context['upArrowStartingX']
    upArrowStartingY       = context['upArrowStartingY']
    upArrowRectangleWidth  = context['upArrowRectangleWidth']
    upArrowRectangleHeight = context['upArrowRectangleHeight']
    point1UpArrow          = context['point1UpArrow']
    point2UpArrow          = context['point2UpArrow']
    point3UpArrow          = context['point3UpArrow']
    
    screen.blit(image, (150, 150))
    pygame.draw.rect(screen, color, (upArrowStartingX, upArrowStartingY, upArrowRectangleWidth, upArrowRectangleHeight), 0)  # Moving bar specs
    pygame.draw.polygon(screen, color, (point1UpArrow, point2UpArrow, point3UpArrow))

