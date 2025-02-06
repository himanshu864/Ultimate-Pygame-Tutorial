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
    pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha(),
]
snail_frames = [
    pygame.image.load("graphics/Snail/snail1.png").convert_alpha(),
    pygame.image.load("graphics/Snail/snail2.png").convert_alpha(),
]

# GAME VARIABLES
game_over = True

# Load text
font = pygame.font.Font("font/Pixeltype.ttf", 50)
score_surf = font.render("SCORE: 100", False, "Black")
main_menu_text = font.render("PRESS SPACE TO START GAME", False, "Black")

# Ground position
GROUND_Y = 300

# HP
HP_FULL = 150
hp_left = HP_FULL

# Player properties
player_walk_index = 0
is_jumping = False
player_y_velocity = 0
JUMP_POWER = 11
GRAVITY = 0.5
INVINCIBILITY_FRAMES = 60
invincible = 0

# Snail enemy properties
snail_index = 0
SNAIL_SPEED = 5

# Create Rectangles
sky_rect = sky_surface.get_rect(topleft=(0, 0))
ground_rect = ground_surface.get_rect(topleft=(0, GROUND_Y))
score_rect = score_surf.get_rect(topleft=(600, 50))
main_menu_rect = main_menu_text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
player_rect = player_stand.get_rect(bottomleft=(100, GROUND_Y))
snail_rect = snail_frames[0].get_rect(bottomleft=(WINDOW_WIDTH, GROUND_Y))

# Game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # Handle game start and jumping
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if game_over:
                game_over = False
                hp_left = HP_FULL
                player_walk_index = 0
                is_jumping = False
                player_y_velocity = 0
                invincible = 0
                snail_index = 0
                snail_rect.left = WINDOW_WIDTH
                sky_rect.x = 0
                player_rect.bottom = GROUND_Y
            else:
                if not is_jumping:
                    is_jumping = True
                    player_y_velocity = -JUMP_POWER

    # Display main menu
    if game_over:
        screen.fill("SkyBlue")
        screen.blit(main_menu_text, (180, 180))
        pygame.display.update()
        continue

    # Draw scrolling sky background
    sky_rect.x = (sky_rect.x - 2) % WINDOW_WIDTH
    screen.blit(sky_surface, (sky_rect.x - WINDOW_WIDTH, 0))
    screen.blit(sky_surface, sky_rect)

    # Draw ground
    ground_rect.x = (ground_rect.x - 4) % WINDOW_WIDTH
    screen.blit(ground_surface, (ground_rect.x - WINDOW_WIDTH, ground_rect.y))
    screen.blit(ground_surface, ground_rect)

    # Display Score
    screen.blit(score_surf, score_rect)

    # Display Health Bar
    pygame.draw.rect(screen, "Crimson", pygame.Rect(30, 30, HP_FULL, 20), 1, 5)
    pygame.draw.rect(screen, "Crimson", pygame.Rect(30, 30, hp_left, 20), 0, 5)

    # Handle player jump movement
    if is_jumping:
        player_rect.bottom += player_y_velocity
        player_y_velocity += GRAVITY
        if player_rect.bottom >= GROUND_Y:
            player_rect.bottom = GROUND_Y
            is_jumping = False

    # Draw player animation
    if not is_jumping and not invincible:
        screen.blit(player_walk_frames[player_walk_index // 5], player_rect)
        player_walk_index = (player_walk_index + 1) % 10
    else:
        screen.blit(player_stand, player_rect)

    # Move and animate snail enemy
    screen.blit(snail_frames[snail_index // 5], snail_rect)
    snail_index = (snail_index + 1) % 10
    snail_rect.right -= SNAIL_SPEED
    if snail_rect.right < 0:
        snail_rect.left = WINDOW_WIDTH

    # Handle Collision and Invincibility
    snail_hitbox = pygame.Rect(
        snail_rect.left + 10,
        snail_rect.top + 5,
        snail_rect.width - 10,
        snail_rect.height,
    )
    if invincible:
        invincible -= 1
    else:
        if player_rect.colliderect(snail_hitbox):
            hp_left -= 50
            invincible = INVINCIBILITY_FRAMES

    # Handle GameOver
    if hp_left <= 0:
        game_over = True

    # Refresh display at 60 FPS
    pygame.display.update()
    clock.tick(60)
