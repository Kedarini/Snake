import pygame
import random
from sys import exit

pygame.init()

# Set up the display
screen_width = 1024
screen_height = 768
tilesize = 64
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake")
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

# Snake settings
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
snake_direction = "RIGHT"
snake_speed = 15

# Apple settings
apple_pos = None

# Background
ground1 = pygame.Surface((tilesize, tilesize))
ground1.fill(green1)
ground2 = pygame.Surface((tilesize, tilesize))
ground2.fill(green2)


# Load and scale images to tilesize
def load_scaled_image(path):
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, (tilesize, tilesize))


apple_img = load_scaled_image("Resources/apple.png")
snake_head_img = load_scaled_image("Resources/snakehead.png")
snake_body_img = load_scaled_image("Resources/snakebody.png")
snake_back_img = load_scaled_image("Resources/snakeback.png")

# Load and scale corner images
snake_corner_left_to_bottom = load_scaled_image("Resources/snakecorner_lb.png")
snake_corner_left_to_top = load_scaled_image("Resources/snakecorner_lt.png")
snake_corner_right_to_bottom = load_scaled_image("Resources/snakecorner_rb.png")
snake_corner_right_to_top = load_scaled_image("Resources/snakecorner_rt.png")


# Function to spawn an apple
def spawn_apple(snake_body):
    while True:
        pos = (
            random.randint(0, (screen_width // tilesize) - 1) * tilesize,
            random.randint(0, (screen_height // tilesize) - 1) * tilesize,
        )
        if pos not in snake_body:
            return pos


# Initialize apple position
apple_pos = spawn_apple(snake_body)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key in DIRECTIONS:
                snake_direction = DIRECTIONS[event.key]
            elif event.key == pygame.K_ESCAPE:
                exit()

    # Background
    for x in range(0, screen_width, tilesize):
        for y in range(0, screen_height, tilesize):
            if (x + y) % (tilesize * 2) == 0:
                screen.blit(ground1, (x, y))
            else:
                screen.blit(ground2, (x, y))

    # Draw the apple
    screen.blit(apple_img, apple_pos)

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(snake_speed)

# Quit pygame
pygame.quit()
exit()
