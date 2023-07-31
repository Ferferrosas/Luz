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
        # Constants for the table
        rows = 2
        cols = 3
        TABLE_WIDTH = screen.get_width() * 0.2
        TABLE_HEIGHT = screen.get_height() * 0.2
        CELL_WIDTH = TABLE_WIDTH // cols
        CELL_HEIGHT = TABLE_HEIGHT // rows
        table_x = screen.get_width() - TABLE_WIDTH
        table_y = screen.get_height() - TABLE_HEIGHT
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
                padx = 100
                pady = 100
                x = table_x + col * CELL_WIDTH  - padx
                y = table_y + row * CELL_HEIGHT - pady

                # Draw the table cell outline using lines
                pygame.draw.line(screen, WHITE, (x, y), (x + CELL_WIDTH, y), 2)
                pygame.draw.line(screen, WHITE, (x, y), (x, y + CELL_HEIGHT), 2)
                pygame.draw.line(screen, WHITE, (x + CELL_WIDTH, y), (x + CELL_WIDTH, y + CELL_HEIGHT), 2)
                pygame.draw.line(screen, WHITE, (x, y + CELL_HEIGHT), (x + CELL_WIDTH, y + CELL_HEIGHT), 2)

                # Add text fields inside the cells
                if row == 0:
                    cell_text = f"{col+1}"
                else:
                    try:
                        cell_text = f"{self.scores[current][col]:.3f}"
                    except:
                        cell_text = f"999.999"

                font = pygame.font.SysFont("Arial", 24)
                text_surface = font.render(cell_text, True, WHITE)
                text_rect = text_surface.get_rect(center=(x + CELL_WIDTH // 2, y + CELL_HEIGHT // 2))
                screen.blit(text_surface, text_rect)

    def greet(self,screen, className, best_time):
        pass