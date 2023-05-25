import random
import os
import time
import readchar

# Game constants
WIDTH = 20
HEIGHT = 10
SNAKE_HEAD = '@'
SNAKE_BODY = 'o'
BONUS = '*'
BIG_BONUS = '#'
EMPTY_SPACE = ' '

# Game variables
snake = [(0, 0)]
direction = 'right'
bonus = None
big_bonus = None
score = 0

# Function to generate a new bonus position
def generate_bonus():
    global bonus
    while True:
        x = random.randint(0, WIDTH - 1)
        y = random.randint(0, HEIGHT - 1)
        if (x, y) not in snake and (x, y) != big_bonus:
            bonus = (x, y)
            break

# Function to generate a new big bonus position
def generate_big_bonus():
    global big_bonus
    while True:
        x = random.randint(0, WIDTH - 1)
        y = random.randint(0, HEIGHT - 1)
        if (x, y) not in snake and (x, y) != bonus:
            big_bonus = (x, y)
            break

# Function to draw the game board
def draw_board():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('SCORE:', score)
    print('-' * (WIDTH + 2))
    for y in range(HEIGHT):
        print('|', end='')
        for x in range(WIDTH):
            if (x, y) == snake[0]:
                print(SNAKE_HEAD, end='')
            elif (x, y) in snake[1:]:
                print(SNAKE_BODY, end='')
            elif (x, y) == bonus:
                print(BONUS, end='')
            elif (x, y) == big_bonus:
                print(BIG_BONUS, end='')
            else:
                print(EMPTY_SPACE, end='')
        print('|')
    print('-' * (WIDTH + 2))

# Function to handle keyboard input
def get_key():
    key = readchar.readkey()
    if key == '\x1b[A':
        return 'up'
    elif key == '\x1b[B':
        return 'down'
    elif key == '\x1b[D':
        return 'left'
    elif key == '\x1b[C':
        return 'right'
    return None

# Function to update the game state
def update_game():
    global snake, direction, score

    # Get the new head position
    head = snake[0]
    if direction == 'up':
        new_head = (head[0], head[1] - 1)
    elif direction == 'down':
        new_head = (head[0], head[1] + 1)
    elif direction == 'left':
        new_head = (head[0] - 1, head[1])
    elif direction == 'right':
        new_head = (head[0] + 1, head[1])

    # Check for collision with the boundaries
    if (
        new_head[0] < 0 or new_head[0] >= WIDTH or
        new_head[1] < 0 or new_head[1] >= HEIGHT
    ):
        return False

    # Check for collision with the snake's body
    if new_head in snake[1:]:
        return False

    # Check if the snake eats the bonus
    if new_head == bonus:
        # Increase the snake's length
        snake.insert(0, new_head)
        score += 1
        generate_bonus()
    elif new_head == big_bonus:
        # Decrease the snake's length
        if len(snake) > 1:
            snake = snake[1:]
        generate_big_bonus()
    else:
        # Move the snake forward
        snake.insert(0, new_head)
        snake = snake[:-1]

    # Check if the snake's length is 0 to end the game
    if len(snake) == 0:
        return False

    return True

# Main game loop
def play_game():
    global direction, score

    # Initialize the game
    generate_bonus()
    generate_big_bonus()
    draw_board()

    while True:
        # Get the user input
        key = get_key()

        # Update the direction
        if key:
            if (
                (key == 'up' and direction != 'down') or
                (key == 'down' and direction != 'up') or
                (key == 'left' and direction != 'right') or
                (key == 'right' and direction != 'left')
            ):
                direction = key

        # Update the game state
        if not update_game():
            break

        # Draw the game board
        draw_board()

        # Delay for a short period
        time.sleep(0.2)

    print('GAME OVER')
    print('Final Score:', score)

# Start the game
play_game()


