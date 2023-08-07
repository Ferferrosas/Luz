import os
import json
import pygame

class Leaderboard():
    def __init__(self) -> None:
        if not os.path.exists('scores.json'):
            self.scores = {
            "IM_FLEXION_MET"  : [],
            "IM_EXTENSION_MET": [],
            "IM_FLEXION_PHA"  : [],
            "IM_EXTENSION_PHA": [],
            "IM_ADDUCTION_MET": [],
            "IM_ABDUCTION_MET": [],
            "IM_POINTING"     : [],
            "IM_FINGER_3"     : [],
            "IM_FINGER_2"     : [],
            "IM_MIDDLE_FINGER": [],
            "IM_RING_FINGER"  : [],
            "IM_PINKIE_FINGER": []
            }
            with open('scores.json', 'w') as file:
                json.dump(self.scores,file)
        else:
            with open('scores.json', 'r') as file:
                self.scores = json.load(file)

    def save(self):
        with open('scores.json', 'w') as file:
            json.dump(self.scores,file)
    def load(self):
        with open('scores.json', 'r') as file:
            self.scores = json.load(file)
    def get_current_scores(self):
        return self.scores
    
    def push_score(self,className,value):
        class_to_text = {
            1:  "IM_FLEXION_MET",
            2:  "IM_EXTENSION_MET",
            3:  "IM_FLEXION_PHA",
            4:  "IM_EXTENSION_PHA",
            5:  "IM_ADDUCTION_MET",
            6:  "IM_ABDUCTION_MET",
            7:  "IM_POINTING",
            8:  "IM_FINGER_3",
            9:  "IM_FINGER_2",
            10: "IM_MIDDLE_FINGER",
            11: "IM_RING_FINGER",
            12: "IM_PINKIE_FINGER"
        }
        scoreName = class_to_text[className]
        if scoreName in self.scores:
            self.scores[scoreName].append(value)
            self.scores[scoreName].sort()
            self.save()
        
    def draw_table(self, screen,className):
        screen_width, screen_height = pygame.display.get_surface().get_size()
        rows = 10
        cols = 2
        CELL_HEIGHT = screen_height / 10  # Cell height spans the full screen y-direction divided by the number of rows
        CELL_WIDTH = 0.20 * screen_width / cols  # Each cell's width based on 20% of screen width divided by the number of columns

        table_width = cols * CELL_WIDTH
        table_x = screen_width - table_width  # Starting x-coordinate for the table, to place it on the right side
        table_y = 0  # Starting at the top of the screen
        # Colors
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        class_to_text = {
            1:  "IM_FLEXION_MET",
            2:  "IM_EXTENSION_MET",
            3:  "IM_FLEXION_PHA",
            4:  "IM_EXTENSION_PHA",
            5:  "IM_ADDUCTION_MET",
            6:  "IM_ABDUCTION_MET",
            7:  "IM_POINTING",
            8:  "IM_FINGER_3",
            9:  "IM_FINGER_2",
            10: "IM_MIDDLE_FINGER",
            11: "IM_RING_FINGER",
            12: "IM_PINKIE_FINGER"
        }
        self.load()
        current = class_to_text[className]
        thisScores = self.scores[current]
        

        for row in range(rows):
            for col in range(cols):
                padx = 0.10 * screen_width
                pady = 0.10 * screen_height
                x = table_x + col * CELL_WIDTH
                y = table_y + row * CELL_HEIGHT

                # Draw the table cell outline using lines
                pygame.draw.line(screen, WHITE, (x, y), (x + CELL_WIDTH, y), 2)
                pygame.draw.line(screen, WHITE, (x, y), (x, y + CELL_HEIGHT), 2)
                pygame.draw.line(screen, WHITE, (x + CELL_WIDTH, y), (x + CELL_WIDTH, y + CELL_HEIGHT), 2)
                pygame.draw.line(screen, WHITE, (x, y + CELL_HEIGHT), (x + CELL_WIDTH, y + CELL_HEIGHT), 2)

                # Add text fields inside the cells
                if row == 0:
                    cell_text = f"Top scores"
                else: 
                    if col == 0:
                        cell_text = f"{row}"
                    else:
                        try:
                            cell_text = f"{self.scores[current][row-1]:.3f}"  # Modify this line to match your data source
                        except:
                            cell_text = f"999.999"

                font = pygame.font.SysFont("Arial", 24)
                text_surface = font.render(cell_text, True, WHITE)
                text_rect = text_surface.get_rect(center=(x + CELL_WIDTH // 2, y + CELL_HEIGHT // 2))
                screen.blit(text_surface, text_rect)
        pygame.display.update()
        return

    def greet(self,screen, className, best_time):
        pass