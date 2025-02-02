import pygame
from sys import exit

# Initialize Pygame
pygame.init()

# Set window resolution
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 400

# Set up display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Dark Souls: Prepare to Cry")
clock = pygame.time.Clock()

# Load images
sky_surface = pygame.image.load("graphics/Sky.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()
player_stand = pygame.image.load("graphics/Player/player_stand.png").convert_alpha()
player_walk_frames = [
    pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha(),
    pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
]
snail_frames = [
    pygame.image.load("graphics/Snail/snail1.png").convert_alpha(),
    pygame.image.load("graphics/Snail/snail2.png").convert_alpha()
]

# Load text
font = pygame.font.Font("font/Pixeltype.ttf", 50)
game_title = font.render("Dark Souls: Prepare to Cry", False, 'Black')

# Sky variables for infinite scrolling
sky_x = 0

# Ground position
GROUND_Y = 300

# Player properties
player_x = 100
player_y = GROUND_Y
player_walk_index = 0
is_jumping = False
player_y_velocity = 0
JUMP_POWER = 10
GRAVITY = 0.5

# Snail enemy properties
snail_width = snail_frames[0].get_width()
snail_x = WINDOW_WIDTH
snail_index = 0
SNAIL_SPEED = 5

# Game loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Jump action
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping:
                is_jumping = True
                player_y_velocity = -JUMP_POWER

    # Draw scrolling sky background
    screen.blit(sky_surface, (sky_x - WINDOW_WIDTH, 0))
    screen.blit(sky_surface, (sky_x, 0))
    sky_x = (sky_x - 2) % WINDOW_WIDTH 

    # Draw ground and text
    screen.blit(ground_surface, (0, GROUND_Y))
    screen.blit(game_title, (350, 50))

    # Handle player jump movement
    if is_jumping:
        player_y += player_y_velocity
        player_y_velocity += GRAVITY
        if player_y >= GROUND_Y:
            player_y = GROUND_Y
            is_jumping = False

    player_rect = player_stand.get_rect(bottomleft = (player_x, player_y))

    # Draw player animation
    if not is_jumping:
        screen.blit(player_walk_frames[player_walk_index // 5], player_rect)
        player_walk_index = (player_walk_index + 1) % 10
    else:
        screen.blit(player_stand, player_rect)

    # Move and animate snail enemy
    screen.blit(snail_frames[snail_index // 5], (snail_x, GROUND_Y - snail_frames[0].get_height()))
    snail_index = (snail_index + 1) % 10
    snail_x -= SNAIL_SPEED
    if snail_x < -snail_width:
        snail_x = WINDOW_WIDTH

    # Refresh display at 60 FPS
    pygame.display.update()
    clock.tick(60)
