import pygame
import time

def bleep_arrow(image,global_vars):
    
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

    point1 = (centerOfScreen[0], Bigger_rectangle_Y)
    point2 = (centerOfScreen[0] - 0.35 * bar_height, Bigger_rectangle_Y + bar_height / 2)
    point3 = (centerOfScreen[0] + 0.35 * bar_height, Bigger_rectangle_Y + bar_height / 2)

    negative_color              = (255 - arrowColor[0], 255 - arrowColor[1], 255 - arrowColor[2])
    center_x, center_y = global_vars['centerOfScreen']
    screen_width , screen_height  = screen.get_size()
    # Relative positioning for the image at 30% of the center
    displacement = 0.30 * screen.get_width()
    image_width, image_height = image.get_size()
    new_image_width = int(0.30 * screen_width)
    new_image_height = int((new_image_width / image_width) * image_height)  # Preserving aspect ratio
    scaled_image = pygame.transform.scale(image, (new_image_width, new_image_height))
    displacementx = 0.30*screen_width
    relative_image_x = center_x - (new_image_width / 2) - displacementx
    relative_image_y = center_y - (new_image_height / 2)
    screen.blit(scaled_image, (relative_image_x, relative_image_y))

    pygame.draw.rect(screen, negative_color, (upArrowStartingX, upArrowStartingY, upArrowRectangleWidth, upArrowRectangleHeight), 0)  # Moving bar specs
    pygame.draw.polygon(screen, negative_color, (point1UpArrow, point2UpArrow, point3UpArrow))
    pygame.draw.rect(screen, arrowColor, (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height, Bigger_rectangle_height_new), 0)  # fill bar with the class color
    pygame.draw.rect(screen, bigRecEdgeColor, (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height, Bigger_rectangle_height_new), Bigthickness)  # mark the edge 
    pygame.draw.rect(screen, bigRecEdgeColor, (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height, Bigger_rectangle_height_new), Bigthickness)  # Bigger edge

    pygame.draw.circle(screen, arrowColor, (int(centerOfScreen[0]), int(Bigger_rectangle_Y + bar_height / 2)), int(bar_height * 0.8), 0) 
    pygame.draw.circle(screen, bigRecEdgeColor, (int(centerOfScreen[0]), int(Bigger_rectangle_Y + bar_height / 2)), int(bar_height * 0.8), Bigthickness)  # highlight the edge of 
    pygame.draw.polygon(screen, arrowColor, (point1, point2, point3))
    pygame.display.update()
    return

def draw_task_image(image, context): 
    screen = context['screen']
    arrowColor = context['arrowColor']
    centerOfScreen = context['centerOfScreen']
    bar_height = context['bar_height']
    Bigger_rectangle_Y = context['Bigger_rectangle_Y']
    Bigger_rectangle_height = context['Bigger_rectangle_height']
    thickness = context['thickness']
    bigRecColor = context['bigRecColor']
    bigRecEdgeColor = context['bigRecEdgeColor']
    Bigger_rectangle_new_X = context['Bigger_rectangle_new_X']
    Bigger_rectangle_new_Y = context['Bigger_rectangle_new_Y']
    Bigger_rectangle_height_new = context['Bigger_rectangle_height_new']
    Bigthickness = context['Bigthickness']
    barColor = context['barColor']
    initial_x_new = context['initial_x_new']
    y_bar = context['y_bar']
    bar_width = context['bar_width']
    delta_height_2 = context['delta_height_2']
    color = context['arrowColor']
    point1UpArrow = context['point1UpArrow']
    point2UpArrow = context['point2UpArrow']
    point3UpArrow = context['point3UpArrow']
    center_x, center_y = context['centerOfScreen']

    upArrowStartingX            = context['upArrowStartingX']
    upArrowStartingY            = context['upArrowStartingY']
    upArrowRectangleWidth       = context['upArrowRectangleWidth']
    upArrowRectangleHeight      = context['upArrowRectangleHeight']    
    screen_width , screen_height  = screen.get_size()
    # Relative positioning for the image at 30% of the center
    displacement = 0.30 * screen.get_width()
    image_width, image_height = image.get_size()
    new_image_width = int(0.30 * screen_width)
    new_image_height = int((new_image_width / image_width) * image_height)  # Preserving aspect ratio
    scaled_image = pygame.transform.scale(image, (new_image_width, new_image_height))
    displacementx = 0.30*screen_width
    relative_image_x = center_x - (new_image_width / 2) - displacementx
    relative_image_y = center_y - (new_image_height / 2)
    screen.blit(scaled_image, (relative_image_x, relative_image_y))
    pygame.draw.rect(screen, bigRecColor,     (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height, Bigger_rectangle_height_new), 0)  
    pygame.draw.rect(screen, bigRecEdgeColor, (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height, Bigger_rectangle_height_new), Bigthickness)  
    pygame.draw.rect(screen, barColor,        (initial_x_new, y_bar, bar_width, delta_height_2))  

    pygame.draw.polygon(screen, color, (point1UpArrow, point2UpArrow, point3UpArrow))
    pygame.draw.rect(screen, color, (upArrowStartingX, upArrowStartingY, upArrowRectangleWidth, upArrowRectangleHeight), 0)
    pygame.draw.rect(screen, bigRecEdgeColor, (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height, Bigger_rectangle_height_new), Bigthickness)   
    pygame.draw.rect(screen, bigRecEdgeColor, (Bigger_rectangle_new_X, Bigger_rectangle_new_Y, Bigger_rectangle_height, Bigger_rectangle_height_new), Bigthickness)  
    
    
    pygame.draw.circle(screen, (0,0,0), (int(centerOfScreen[0]), int(Bigger_rectangle_Y + bar_height / 2)), int(bar_height * 0.8), 0)
    pygame.draw.circle(screen, bigRecEdgeColor, (int(centerOfScreen[0]), int(Bigger_rectangle_Y + bar_height / 2)), int(bar_height * 0.8), Bigthickness)

    pygame.display.update()
    return 
    

def draw_image_with_arrow(image, context):
    screen = context['screen']
    screen_width, screen_height = screen.get_size()
    displacementx = 0.30 * screen_width
    center_x, center_y = context['centerOfScreen']

    # Scale the image
    image_width, image_height = image.get_size()
    new_image_width = int(0.30 * screen_width)
    new_image_height = int((new_image_width / image_width) * image_height)  # Preserving aspect ratio
    scaled_image = pygame.transform.scale(image, (new_image_width, new_image_height))
    
    relative_image_x = center_x - (new_image_width / 2) - displacementx
    relative_image_y = center_y - (new_image_height / 2)

    arrow_rect_x = center_x - context['bar_height'] / 6
    arrow_rect_y = center_y + context['Bigger_rectangle_Y'] + context['bar_height'] / 2
    arrow_rect_width = 2 * context['bar_height'] / 6
    arrow_rect_height = context['Bigger_rectangle_height'] / 2

    screen.blit(scaled_image, (relative_image_x, relative_image_y))
    pygame.draw.rect(screen, context['arrowColor'], (arrow_rect_x, arrow_rect_y, arrow_rect_width, arrow_rect_height), context['thickness'])
    pygame.display.update()
    return



def draw_image_with_arrow_ff(color, image, context):
    screen = context['screen']
    screen_width, screen_height = screen.get_size()
    center_x, center_y = context['centerOfScreen']

    # Adjusting image placement to be centered on the screen
    image_width, image_height = image.get_size()
    image_x = (screen_width - image_width) / 2 - 0.15 * screen_width
    image_y = (screen_height - image_height) / 2 

    # Using the same positioning for arrow as in the above function
    arrow_rect_x = center_x - context['bar_height'] / 6
    arrow_rect_y = center_y + context['Bigger_rectangle_Y'] + context['bar_height'] / 2
    arrow_rect_width = 2 * context['bar_height'] / 6
    arrow_rect_height = context['Bigger_rectangle_height'] / 2

    image_width, image_height = image.get_size()
    new_image_width = int(0.30 * screen_width)
    new_image_height = int((new_image_width / image_width) * image_height)  # Preserving aspect ratio
    scaled_image = pygame.transform.scale(image, (new_image_width, new_image_height))
    displacementx = 0.30*screen_width
    relative_image_x = center_x - (new_image_width / 2) - displacementx
    relative_image_y = center_y - (new_image_height / 2)
    screen.blit(scaled_image, (relative_image_x, relative_image_y))
    pygame.draw.rect(screen, color, (arrow_rect_x, arrow_rect_y, arrow_rect_width, arrow_rect_height), context['thickness'])
    pygame.display.update()
    return

def update_bar_height(context):
    Bigger_rectangle_width = context['Bigger_rectangle_width']
    bar_width = context['bar_width']
    prevTime = context['prevTime']
    taskTime = context['taskTime']
    Bigger_rectangle_Y = context['Bigger_rectangle_Y']

    step_size = (0.5 * Bigger_rectangle_width - bar_width * 0.5) * (time.time() - prevTime) / taskTime
    y_bar = Bigger_rectangle_Y - step_size
    delta_height_2 = bar_width + step_size

    # Update the context with the new values
    context['y_bar'] = y_bar
    context['delta_height_2'] = delta_height_2
