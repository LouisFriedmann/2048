# Imports
import pygame
import twenty_forty_eight
import math

# Square class

# Create images for square class
loaded_img_files = [pygame.image.load('Image[1].jpeg'), pygame.image.load('Image[2].jpeg'),
                    pygame.image.load('Image[3].jpeg'), pygame.image.load('Image[4].jpeg'),
                    pygame.image.load('Image[5].jpeg'), pygame.image.load('Image[6].jpeg'),
                    pygame.image.load('Image[7].jpeg'), pygame.image.load('Image[8].jpeg'),
                    pygame.image.load('Image[9].jpeg'), pygame.image.load('Image[10].jpeg'),
                    pygame.image.load('Image[11].jpeg')]

default_loaded_img = pygame.image.load('Image.jpeg')

class Square:

    # Initializer
    def __init__(self, screen, height, start_pos, num=None):
        self.screen = screen

        # Number has to be an integer and a power of 2
        if not isinstance(num, int) and num != None:
            raise TypeError(f"{num} is not a number")
        if num != None and not is_power_of_2(num):
            raise ValueError(f"{num} must be a power of 2")
        self.num = num

        # Check for appropriate dimensions
        if not isinstance(height, int) and not isinstance(height, float):
            raise TypeError("Dimensions must be numbers")
        if height <= 0:
            raise ValueError("Dimensions must be greater than zero")
        self.height = height

        self.x, self.y = start_pos

        # When user doesn't specify square, make square default image, otherwise make square the image based on its specific number
        if num == None:
            img = pygame.transform.scale(default_loaded_img, (self.height, self.height))
            self.screen.blit(img, (self.x, self.y))

        else:
            img = pygame.transform.scale(loaded_img_files[int(math.log(self.num, 2))], (self.height, self.height))
            self.screen.blit(img, (self.x, self.y))

            # Display number on screen
            font = pygame.font.SysFont(None, int(self.height / 2))
            font_text = font.render(str(self.num), True, "gold")
            self.screen.blit(font_text, (self.x + self.height / 2 - font_text.get_width() / 2,
                                    self.y + self.height / 2 - font_text.get_height() / 2))


    # Methods

    # Method moves a square to a specific position, fills previous position with a default square
    def move_to(self, x, y):
        Square(height=self.height, screen=self.screen, start_pos=(self.x, self.y))
        self.x = x
        self.y = y
        Square(height=self.height, screen=self.screen, start_pos=(self.x, self.y), num=self.num)

# Functions

# Function determines if a number is a power of 2
def is_power_of_2(num):
    return num != 0 and (num & (num - 1)) == 0
