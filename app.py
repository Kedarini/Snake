import pygame
import random
from sys import exit

pygame.init()

# Set up the display
screen_width = 1024
screen_height = 768
tilesize = 64
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Colors
green1 = (145, 160, 121)
green2 = (129, 144, 103)

# Directions
DIRECTIONS = {
    pygame.K_UP: "UP",
    pygame.K_DOWN: "DOWN",
    pygame.K_LEFT: "LEFT",
    pygame.K_RIGHT: "RIGHT",
    pygame.K_w: "UP",
    pygame.K_s: "DOWN",
    pygame.K_a: "LEFT",
    pygame.K_d: "RIGHT",
}

# Scoreboard
apples_eaten = 0

# Snake settings
snake_pos = [128, 64]
snake_body = [[128, 64], [64, 64], [0, 64]]
snake_direction = "RIGHT"
snake_move_timer = 0
snake_move_interval = 200

# Background
ground1 = pygame.Surface((tilesize, tilesize))
ground1.fill(green1)
ground2 = pygame.Surface((tilesize, tilesize))
ground2.fill(green2)


# Load and scale images
def load_scaled_image(path):
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, (tilesize, tilesize))


apple_img = load_scaled_image("Resources/apple.png")
snake_head_img = load_scaled_image("Resources/snakehead.png")
snake_body_img = load_scaled_image("Resources/snakebody.png")
snake_back_img = load_scaled_image("Resources/snakeback.png")

# Initial rotated head
rotated_head = snake_head_img


# Function to spawn apple
def spawn_apple(snake_body):
    while True:
        pos = (
            random.randint(0, (screen_width // tilesize) - 1) * tilesize,
            random.randint(0, (screen_height // tilesize) - 1) * tilesize,
        )
        if list(pos) not in snake_body:
            return pos


apple_pos = spawn_apple(snake_body)


# Function to move snake
def move_snake():
    if snake_direction == "RIGHT":
        snake_pos[0] += tilesize
    elif snake_direction == "LEFT":
        snake_pos[0] -= tilesize
    elif snake_direction == "UP":
        snake_pos[1] -= tilesize
    elif snake_direction == "DOWN":
        snake_pos[1] += tilesize


# Rotate head based on direction
def rotate_head():
    global rotated_head
    if snake_direction == "RIGHT":
        rotated_head = snake_head_img
    elif snake_direction == "LEFT":
        rotated_head = pygame.transform.rotate(snake_head_img, 180)
    elif snake_direction == "UP":
        rotated_head = pygame.transform.rotate(snake_head_img, 90)
    elif snake_direction == "DOWN":
        rotated_head = pygame.transform.rotate(snake_head_img, 270)


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key in DIRECTIONS:
                new_direction = DIRECTIONS[event.key]
                # Prevent reversing
                if (snake_direction, new_direction) not in [
                    ("LEFT", "RIGHT"),
                    ("RIGHT", "LEFT"),
                    ("UP", "DOWN"),
                    ("DOWN", "UP"),
                ]:
                    snake_direction = new_direction
                    rotate_head()
            elif event.key == pygame.K_ESCAPE:
                exit()

    pygame.display.set_caption(f"Snake Score: {apples_eaten}")

    # Draw background
    for x in range(0, screen_width, tilesize):
        for y in range(0, screen_height, tilesize):
            if (x + y) % (tilesize * 2) == 0:
                screen.blit(ground1, (x, y))
            else:
                screen.blit(ground2, (x, y))

    # Move the snake at set intervals
    downtime = clock.tick(60)
    snake_move_timer += downtime
    if snake_move_timer >= snake_move_interval:
        snake_move_timer = 0

        move_snake()
        snake_body.insert(0, list(snake_pos))  # Add new head

        # If snake eats apple, don't remove tail
        if snake_pos == list(apple_pos):
            apples_eaten += 1
            apple_pos = spawn_apple(snake_body)
        else:
            snake_body.pop()  # Remove tail

    # Draw the full snake
    for i, part in enumerate(snake_body):
        if i == 0:
            screen.blit(rotated_head, part)  # Head
        elif i == len(snake_body) - 1:
            screen.blit(snake_back_img, part)  # Tail
        else:
            screen.blit(snake_body_img, part)  # Body

    # Draw apple
    screen.blit(apple_img, apple_pos)

    # Collision with walls
    if (
        snake_pos[0] < 0
        or snake_pos[0] >= screen_width
        or snake_pos[1] < 0
        or snake_pos[1] >= screen_height
    ):
        print("Game Over: You ran out of map")
        exit()

    # Collision with itself
    if snake_pos in snake_body[1:]:
        print("Game Over: You hit yourself")
        exit()

    pygame.display.flip()

pygame.quit()
exit()
