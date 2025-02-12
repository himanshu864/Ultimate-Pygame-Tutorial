import pygame
from sys import exit
from random import randint, choice

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 400
GROUND_LEVEL = 300
SCROLL_SPEED_SKY = 2
SCROLL_SPEED_GROUND = 4
HP_FULL = 150
JUMP_POWER = 18
PAR = 6  # Player Animation Rate
SAR = 10  # Snail
FAR = 4  # Fly
INITIAL_ENEMY_SPEED = 6

# Set up display and clock
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Dark Souls: Prepare to Cry")
clock = pygame.time.Clock()

# Load Assets
sky_surface = pygame.image.load("graphics/Sky.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()
player_stand = pygame.image.load("graphics/Player/player_stand.png").convert_alpha()
player_jump = pygame.image.load("graphics/Player/player_jump.png").convert_alpha()
player_walk_1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
snail_frame_1 = pygame.image.load("graphics/Snail/snail1.png").convert_alpha()
snail_frame_2 = pygame.image.load("graphics/Snail/snail2.png").convert_alpha()
fly_frame_1 = pygame.image.load("graphics/Fly/fly1.png").convert_alpha()
fly_frame_2 = pygame.image.load("graphics/Fly/fly2.png").convert_alpha()
font = pygame.font.Font("font/Pixeltype.ttf", 50)

# Game variables
game_active = False
start_time = 0
high_score = 0
last_score = -1
hp_left = HP_FULL
enemy_speed = INITIAL_ENEMY_SPEED

# Rectangles
sky_rect = sky_surface.get_rect(topleft=(0, 0))
ground_rect = ground_surface.get_rect(topleft=(0, GROUND_LEVEL))
player_bigger = pygame.transform.scale2x(player_stand)
menu_player_rect = player_bigger.get_rect(center=(WINDOW_WIDTH / 2, 180))
main_menu_text_surface = font.render("PRESS SPACE TO START GAME", False, "Black")
menu_text_rect = main_menu_text_surface.get_rect(center=(WINDOW_WIDTH // 2, 300))


# Create Sprite Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frames = [player_walk_1, player_walk_2]
        self.index = 0
        self.gravity = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect(bottomleft=(100, GROUND_LEVEL))

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom == GROUND_LEVEL:
            self.gravity = -JUMP_POWER

    def gravity_falls(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= GROUND_LEVEL:
            self.rect.bottom = GROUND_LEVEL

    def animation(self):
        if self.rect.bottom < GROUND_LEVEL:
            self.image = player_jump
        else:
            self.index = (self.index + 1) % (PAR * len(self.frames))
            self.image = self.frames[self.index // PAR]

    def update(self):
        self.player_input()
        self.gravity_falls()
        self.animation()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        self.type = type
        if type == "SNAIL":
            self.frames = [snail_frame_1, snail_frame_2]
            y_pos = GROUND_LEVEL
        else:
            self.frames = [fly_frame_1, fly_frame_2]
            y_pos = 125

        self.speed = enemy_speed
        self.index = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect(bottomleft=[WINDOW_WIDTH, y_pos])

    def animation(self):
        animation_rate = SAR if self.type == "SNAIL" else FAR
        self.index = (self.index + 1) % (animation_rate * len(self.frames))
        self.image = self.frames[self.index // animation_rate]

    def movement(self):
        self.rect.x -= self.speed

    def destroy(self):
        if self.rect.right < 0:
            self.kill()

    def update(self):
        self.animation()
        self.movement()
        self.destroy()


# Add to groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()


# Helper Functions
def get_current_score():
    return (pygame.time.get_ticks() - start_time) // 1000


def display_score():
    score_surface = font.render(f"SCORE: {get_current_score()}", False, "Black")
    score_rect = score_surface.get_rect(topright=(WINDOW_WIDTH - 20, 20))
    screen.blit(score_surface, score_rect)


def display_main_menu():
    screen.fill("#6CB4EE")
    screen.blit(player_bigger, menu_player_rect)
    if last_score == -1:
        screen.blit(main_menu_text_surface, menu_text_rect)
    else:
        # Display High Score and Last Score
        high_score_surface = font.render(f"HIGH SCORE: {high_score}", False, "Green")
        last_score_surface = font.render(f"YOUR SCORE: {last_score}", False, "Black")

        high_score_rect = high_score_surface.get_rect(center=(WINDOW_WIDTH // 2, 75))
        last_score_rect = last_score_surface.get_rect(center=(WINDOW_WIDTH // 2, 300))

        screen.blit(high_score_surface, high_score_rect)
        screen.blit(last_score_surface, last_score_rect)


def display_hp():
    pygame.draw.rect(screen, "Crimson", pygame.Rect(20, 20, hp_left, 20), 0, 5)
    pygame.draw.rect(screen, "Black", pygame.Rect(20, 20, HP_FULL, 20), 2, 5)


def scroll_background():
    sky_rect.x = (sky_rect.x - SCROLL_SPEED_SKY) % WINDOW_WIDTH
    screen.blit(sky_surface, (sky_rect.x - WINDOW_WIDTH, 0))
    screen.blit(sky_surface, sky_rect)

    ground_rect.x = (ground_rect.x - SCROLL_SPEED_GROUND) % WINDOW_WIDTH
    screen.blit(ground_surface, (ground_rect.x - WINDOW_WIDTH, GROUND_LEVEL))
    screen.blit(ground_surface, ground_rect)


def collision():
    global hp_left
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, True):
        hp_left -= 50
        if hp_left <= 0:
            game_over()


def game_start():
    global game_active, start_time, hp_left, enemy_speed

    game_active = True
    start_time = pygame.time.get_ticks()
    sky_rect.x = 0
    ground_rect.x = 0
    player.sprite.gravity = 0
    player.sprite.rect.bottom = GROUND_LEVEL
    hp_left = HP_FULL
    enemy_speed = INITIAL_ENEMY_SPEED
    obstacle_group.empty()


def game_over():
    global game_active, last_score, high_score
    game_active = False
    last_score = get_current_score()
    high_score = max(high_score, last_score)


# Timer to spawn enemies
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, randint(1200, 1800))

# Timer to increasing difficulty
level_timer = pygame.USEREVENT + 2
pygame.time.set_timer(level_timer, 8000)

# Main Game Loop
while True:
    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if not game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_start()
        else:
            if event.type == obstacle_timer:  # append enemy
                obstacle_group.add(Obstacle(choice(["SNAIL", "SNAIL", "FLY"])))

            if event.type == level_timer:  # increase difficulty
                enemy_speed += 1

    # Game State Handling
    if not game_active:
        display_main_menu()
    else:
        # Gameplay
        scroll_background()
        display_hp()
        display_score()
        player.draw(screen)
        player.update()
        obstacle_group.draw(screen)
        obstacle_group.update()
        collision()

    pygame.display.update()
    clock.tick(60)
