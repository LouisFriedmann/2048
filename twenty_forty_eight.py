# Simulation of the popular game 2048

# Imports
import pygame
import math
import random
import square

# Function makes a new blank board and 2 random squares with the number "2"
def make_new_board():
    # Draw grid
    line_x = 0
    line_y = 0
    for i in range(NUM_SQUARES_PER_ROW + 1):
        pygame.draw.rect(screen, "dark grey", (line_x, line_y, RIGHT_BORDER, GRID_THICKNESS))
        line_y += DISTANCE
    line_y = 0
    for i in range(NUM_SQUARES_PER_ROW + 1):
        pygame.draw.rect(screen, "dark grey", (line_x, line_y, GRID_THICKNESS, BOTTOM_BORDER))
        line_x += DISTANCE

    # Put default squares in grid
    square_x = GRID_THICKNESS
    square_y = GRID_THICKNESS
    for row in range(NUM_SQUARES_PER_ROW):
        for col in range(NUM_SQUARES_PER_ROW):
            square.Square(height=SQUARE_HEIGHT, screen=screen, start_pos=(square_x, square_y))
            square_x += DISTANCE
        square_x = GRID_THICKNESS
        square_y += DISTANCE

    # Add squares to the squares in the existing squares in the game IN SEPERATE PLACES
    global existing_square_positions
    existing_square_positions = dict()
    rand_pos_1_idx = random.randint(0, len(square_positions) - 1)
    square_1 = square.Square(height=SQUARE_HEIGHT ,screen=screen, start_pos=square_positions[rand_pos_1_idx][
                      random.randint(0, len(square_positions[0]) - 1)], num=2)
    existing_square_positions.update({(square_1.x, square_1.y) : square_1})
    rand_pos_2_idx = random.randint(0, len(square_positions) - 1)

    while rand_pos_2_idx == rand_pos_1_idx:
        rand_pos_2_idx = random.randint(0, len(square_positions) - 1)

    square_2 = square.Square(height=SQUARE_HEIGHT, screen=screen, start_pos=square_positions[rand_pos_2_idx][
                             random.randint(0, len(square_positions[0]) - 1)], num=2)
    existing_square_positions.update({(square_2.x, square_2.y): square_2})

# Main program
if __name__ == "__main__":

    # Set up pygame
    pygame.init()

    # CONSTANTS
    RIGHT_BORDER = 500
    BOTTOM_BORDER = 500
    DELAY = 100
    COLOR_SEP = 50
    NUM_SQUARES_PER_ROW = 4
    NUM_ROWS = 4
    GRID_THICKNESS = 10
    SQUARE_HEIGHT = RIGHT_BORDER / NUM_SQUARES_PER_ROW - GRID_THICKNESS - GRID_THICKNESS / 5
    DISTANCE = SQUARE_HEIGHT + GRID_THICKNESS # Distance to next square


    # Make screen and caption
    screen = pygame.display.set_mode((RIGHT_BORDER, BOTTOM_BORDER))
    pygame.display.set_caption("2048")

    # Make cube positions
    square_positions = [[None] * NUM_SQUARES_PER_ROW for i in range(NUM_SQUARES_PER_ROW)]

    cube_x = GRID_THICKNESS
    cube_y = GRID_THICKNESS
    for row in range(NUM_SQUARES_PER_ROW):
        for col in range(NUM_SQUARES_PER_ROW):
            square_positions[row][col] = (cube_x, cube_y)
            cube_x += GRID_THICKNESS + SQUARE_HEIGHT
        cube_x = GRID_THICKNESS
        cube_y += GRID_THICKNESS + SQUARE_HEIGHT

    # Main game loop
    make_new_board()
    game_over = False
    is_winner = False
    is_loser = False
    while not game_over:
        # Quit if the user wants to
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        # Check if the user lost by seeing if the board is full and no square has a number equal to it on all four sides
        is_board_full = len(existing_square_positions) >= NUM_ROWS * NUM_SQUARES_PER_ROW
        if is_board_full:
            no_squares_can_combine = False
            for pos in sorted(existing_square_positions):
                next_square = existing_square_positions[pos]

                if ((next_square.x + DISTANCE, next_square.y) in existing_square_positions and
                        next_square.num == existing_square_positions[(next_square.x + DISTANCE, next_square.y)].num):
                    break

                elif ((next_square.x - DISTANCE, next_square.y) in existing_square_positions and
                        next_square.num == existing_square_positions[(next_square.x - DISTANCE, next_square.y)].num):
                    break

                elif ((next_square.x, next_square.y + DISTANCE) in existing_square_positions and
                        next_square.num == existing_square_positions[(next_square.x, next_square.y + DISTANCE)].num):
                    break

                elif ((next_square.x, next_square.y - DISTANCE) in existing_square_positions and
                        next_square.num == existing_square_positions[(next_square.x, next_square.y - DISTANCE)].num):
                    break

                # If whole dictionary sorted dictionary by tuples is traversed, no two squares can combine
                if ((next_square.x, next_square.y) == ((GRID_THICKNESS + DISTANCE * (NUM_SQUARES_PER_ROW - 1)),
                                             GRID_THICKNESS + DISTANCE * (NUM_ROWS - 1))):
                    no_squares_can_combine = True

            if no_squares_can_combine:
                is_loser = True
                game_over = True


        # Allow the user to move the squares with the arrow keys, add squares to the board appropriately
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:

            # Move each individual square in sorted dictionary by tuples (dictionary is sorted so squares higher
            # up can move first). Squares can't go past top border
            has_any_square_moved = False

            for position in sorted(existing_square_positions):
                next_square = existing_square_positions[position]
                done_moving = False

                while not done_moving and next_square.y - DISTANCE > 0:

                    # Combining squares with same number by updating dictionary with new square and removing other two squares, then filling previous space with default square
                    if ((next_square.x, next_square.y - DISTANCE) in existing_square_positions and
                            existing_square_positions[
                                (next_square.x, next_square.y - DISTANCE)].num == next_square.num):

                        # Check if the user won
                        if next_square.num == 1024:
                            is_winner = True
                            game_over = True

                        square.Square(height=SQUARE_HEIGHT, screen=screen, start_pos=(next_square.x, next_square.y)) # Default square
                        new_square = square.Square(height=SQUARE_HEIGHT, screen=screen, start_pos=(next_square.x, next_square.y - DISTANCE),
                                            num=next_square.num * 2)
                        square_key = list(existing_square_positions.keys())[
                                     list(existing_square_positions.values()).index(next_square)]
                        existing_square_positions.pop(square_key)
                        existing_square_positions.pop(((next_square.x, next_square.y - DISTANCE)))
                        existing_square_positions.update({(new_square.x, new_square.y): new_square})
                        has_any_square_moved = True
                        done_moving = True

                    # Squares with different numbers can't be combined
                    elif ((next_square.x, next_square.y - DISTANCE) in existing_square_positions and
                          existing_square_positions[(next_square.x, next_square.y - DISTANCE)].num != next_square.num):
                        done_moving = True

                    # Move the square one space up and update its new position in the dictionary
                    else:
                        existing_square_positions.pop((next_square.x, next_square.y))
                        next_square.move_to(next_square.x, next_square.y - DISTANCE)
                        existing_square_positions.update({(next_square.x, next_square.y): next_square})
                        has_any_square_moved = True

                    pygame.display.update()

            # Add next square to the existing squares only if any square has moved
            if has_any_square_moved:
                rand_pos = (GRID_THICKNESS + DISTANCE * random.randint(0, NUM_SQUARES_PER_ROW - 1), GRID_THICKNESS + DISTANCE * random.randint(0, NUM_ROWS - 1))
                while rand_pos in existing_square_positions:
                     rand_pos = (GRID_THICKNESS + DISTANCE * random.randint(0, NUM_SQUARES_PER_ROW - 1),
                                 GRID_THICKNESS + DISTANCE * random.randint(0, NUM_ROWS - 1))
                existing_square_positions.update({rand_pos: square.Square(height=SQUARE_HEIGHT, screen=screen, start_pos=rand_pos, num=2)})

        elif keys[pygame.K_DOWN]:
            has_any_square_moved = False

            # Move each individual square in reversed-sorted dictionary by tuples (dictionary is sorted and reversed so squares lower
            # down can move first). Squares can't go past bottom border
            for position in reversed(sorted(existing_square_positions)):
                next_square = existing_square_positions[position]
                done_moving = False

                while not done_moving and next_square.y + DISTANCE < BOTTOM_BORDER:

                    # Combining squares with same number by updating dictionary with new square and removing other two squares, then filling previous space with default square
                    if ((next_square.x, next_square.y + DISTANCE) in existing_square_positions and
                            existing_square_positions[
                                (next_square.x, next_square.y + DISTANCE)].num == next_square.num):

                        # Check if the user won
                        if next_square.num == 1024:
                            is_winner = True
                            game_over = True

                        square.Square(height=SQUARE_HEIGHT, screen=screen, start_pos=(next_square.x, next_square.y)) # Default square
                        new_square = square.Square(height=SQUARE_HEIGHT, screen=screen, start_pos=(next_square.x, next_square.y + DISTANCE),
                                            num=next_square.num * 2)
                        square_key = list(existing_square_positions.keys())[
                            list(existing_square_positions.values()).index(next_square)]
                        existing_square_positions.pop(square_key)
                        existing_square_positions.pop(((next_square.x, next_square.y + DISTANCE)))
                        existing_square_positions.update({(new_square.x, new_square.y): new_square})
                        has_any_square_moved = True
                        done_moving = True

                    # Squares with different numbers can't be combined
                    elif ((next_square.x, next_square.y + DISTANCE) in existing_square_positions and
                          existing_square_positions[(next_square.x, next_square.y + DISTANCE)].num != next_square.num):
                        done_moving = True

                    # Move the square one space down and update its new position in the dictionary
                    else:
                        existing_square_positions.pop((next_square.x, next_square.y))
                        next_square.move_to(next_square.x, next_square.y + DISTANCE)
                        existing_square_positions.update({(next_square.x, next_square.y): next_square})
                        has_any_square_moved = True

                    pygame.display.update()

            # Add next square to the existing squares only if any square as moved
            if has_any_square_moved:
                rand_pos = (GRID_THICKNESS + DISTANCE * random.randint(0, NUM_SQUARES_PER_ROW - 1), GRID_THICKNESS + DISTANCE * random.randint(0, NUM_ROWS - 1))
                while rand_pos in existing_square_positions:
                    rand_pos = (GRID_THICKNESS + DISTANCE * random.randint(0, NUM_SQUARES_PER_ROW - 1),
                                GRID_THICKNESS + DISTANCE * random.randint(0, NUM_ROWS - 1))
                existing_square_positions.update({rand_pos: square.Square(height=SQUARE_HEIGHT, screen=screen, start_pos=rand_pos, num=2)})

        elif keys[pygame.K_LEFT]:
            has_any_square_moved = False

            # Move each individual square in sorted dictionary by tuples (dictionary is sorted so squares farther
            # left can move first). Squares can't go past left border
            for position in sorted(existing_square_positions):
                next_square = existing_square_positions[position]
                done_moving = False

                while not done_moving and next_square.x - DISTANCE > 0:

                    # Combining squares with same number by updating dictionary with new square and removing other two squares, then filling previous space with default square
                    if ((next_square.x - DISTANCE, next_square.y) in existing_square_positions and
                            existing_square_positions[
                                (next_square.x - DISTANCE, next_square.y)].num == next_square.num):

                        # Check if the user won
                        if next_square.num == 1024:
                            is_winner = True
                            game_over = True

                        square.Square(height=SQUARE_HEIGHT, screen=screen, start_pos=(next_square.x, next_square.y)) # Default square
                        new_square = square.Square(height=SQUARE_HEIGHT, screen=screen, start_pos=(next_square.x - DISTANCE, next_square.y),
                                            num=next_square.num * 2)
                        square_key = list(existing_square_positions.keys())[
                            list(existing_square_positions.values()).index(next_square)]
                        existing_square_positions.pop(square_key)
                        existing_square_positions.pop(((next_square.x - DISTANCE, next_square.y)))
                        existing_square_positions.update({(new_square.x, new_square.y): new_square})
                        has_any_square_moved = True
                        done_moving = True

                    # Squares with different numbers can't be combined
                    elif ((next_square.x - DISTANCE, next_square.y) in existing_square_positions and
                          existing_square_positions[(next_square.x - DISTANCE, next_square.y)].num != next_square.num):
                        done_moving = True

                    # Move the square one space left and update its new position in the dictionary
                    else:
                        existing_square_positions.pop((next_square.x, next_square.y))
                        next_square.move_to(next_square.x - DISTANCE, next_square.y)
                        existing_square_positions.update({(next_square.x, next_square.y): next_square})
                        has_any_square_moved = True

                    pygame.display.update()

            # Add next square to the existing squares only if any square has moved
            if has_any_square_moved:
                rand_pos = (GRID_THICKNESS + DISTANCE * random.randint(0, NUM_SQUARES_PER_ROW - 1), GRID_THICKNESS + DISTANCE * random.randint(0, NUM_ROWS - 1))
                while rand_pos in existing_square_positions:
                    rand_pos = (GRID_THICKNESS + DISTANCE * random.randint(0, NUM_SQUARES_PER_ROW - 1),
                                GRID_THICKNESS + DISTANCE * random.randint(0, NUM_ROWS - 1))
                existing_square_positions.update({rand_pos: square.Square(height=SQUARE_HEIGHT, screen=screen, start_pos=rand_pos, num=2)})

        elif keys[pygame.K_RIGHT]:
            has_any_square_moved = False

            # Move each individual square in reversed-sorted dictionary by tuples (dictionary is sorted and reversed so squares farther
            # right can move first). Squares can't go past right border border
            for position in reversed(sorted(existing_square_positions)):
                next_square = existing_square_positions[position]
                done_moving = False

                while not done_moving and next_square.x + DISTANCE < RIGHT_BORDER:

                    # Combining squares with same number by updating dictionary with new square and removing other two squares, then filling previous space with default square
                    if ((next_square.x + DISTANCE, next_square.y) in existing_square_positions and
                           existing_square_positions[(next_square.x + DISTANCE, next_square.y)].num == next_square.num):

                        # Check if the user won
                        if next_square.num == 1024:
                            is_winner = True
                            game_over = True

                        square.Square(height=SQUARE_HEIGHT, screen=screen, start_pos=(next_square.x, next_square.y))
                        new_square = square.Square(height=SQUARE_HEIGHT, screen=screen, start_pos=(next_square.x + DISTANCE, next_square.y), num=next_square.num * 2)
                        square_key = list(existing_square_positions.keys())[list(existing_square_positions.values()).index(next_square)]
                        existing_square_positions.pop(square_key)
                        existing_square_positions.pop(((next_square.x + DISTANCE, next_square.y)))
                        existing_square_positions.update({(new_square.x, new_square.y): new_square})
                        has_any_square_moved = True
                        done_moving = True

                    # Squares with different numbers can't be combined
                    elif ((next_square.x + DISTANCE, next_square.y) in existing_square_positions and
                          existing_square_positions[(next_square.x + DISTANCE, next_square.y)].num != next_square.num):
                        done_moving = True

                    # Move the square one space left and update its new position in the dictionary
                    else:
                        existing_square_positions.pop((next_square.x, next_square.y))
                        next_square.move_to(next_square.x + DISTANCE, next_square.y)
                        existing_square_positions.update({(next_square.x, next_square.y) : next_square})
                        has_any_square_moved = True

                    pygame.display.update()

            # Add next square to the existing squares only if any square has moved
            if has_any_square_moved:
                rand_pos = (GRID_THICKNESS + DISTANCE * random.randint(0, NUM_SQUARES_PER_ROW - 1), GRID_THICKNESS + DISTANCE * random.randint(0, NUM_ROWS - 1))
                while rand_pos in existing_square_positions:
                    rand_pos = (GRID_THICKNESS + DISTANCE * random.randint(0, NUM_SQUARES_PER_ROW - 1), GRID_THICKNESS + DISTANCE * random.randint(0, NUM_ROWS - 1))
                existing_square_positions.update({rand_pos : square.Square(height=SQUARE_HEIGHT, screen=screen, start_pos=rand_pos, num=2)})

        # Tell user they lost if they lost
        if is_loser:
            font = pygame.font.SysFont(None, int(BOTTOM_BORDER / 8))
            font_text = font.render("You Lost", True, "red")
            screen.blit(font_text, (RIGHT_BORDER / 2  - font_text.get_width() / 2,
                                    BOTTOM_BORDER / 2 - font_text.get_width() / 2))

        # Tell user they won if they won
        elif is_winner:
            font = pygame.font.SysFont(None, int(BOTTOM_BORDER / 8))
            font_text = font.render("You Won", True, "yellow")
            screen.blit(font_text, (RIGHT_BORDER / 2 - font_text.get_width() / 2,
                                    BOTTOM_BORDER / 2 - font_text.get_width() / 2))

        # Time delay and updating the screen
        pygame.time.delay(DELAY)
        pygame.display.update()

    pygame.time.delay(2000)
    pygame.quit()
