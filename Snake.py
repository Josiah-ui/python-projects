# Simple Snake game with pygame
# Move: arrow keys|   Restart: R
import random
import math
import struct
import pygame

pygame.init()
CELL, COLS, ROWS = 25, 24, 18                  # cell size, grid width, grid height
screen = pygame.display.set_mode((COLS * CELL, ROWS * CELL))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)


def make_tone(frequency, duration=0.12):
    """Create a short tone without requiring external sound files."""
    sample_rate = 22050
    samples = bytearray()
    for index in range(int(sample_rate * duration)):
        envelope = 1 - index / (sample_rate * duration)
        value = int(9000 * envelope * math.sin(2 * math.pi * frequency * index / sample_rate))
        samples.extend(struct.pack("<h", value))
    return pygame.mixer.Sound(buffer=bytes(samples))


eat_sound = pause_sound = game_over_sound = None
try:
    pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
    eat_sound = make_tone(880)
    pause_sound = make_tone(440, 0.08)
    game_over_sound = make_tone(180, 0.35)
    sound_enabled = True
except pygame.error:
    sound_enabled = False


def play_sound(sound):
    if sound_enabled and sound is not None:
        sound.play()

# Key -> (dx, dy) direction
KEYS = {
    pygame.K_UP: (0, -1), pygame.K_w: (0, -1),
    pygame.K_DOWN: (0, 1), pygame.K_s: (0, 1),
    pygame.K_LEFT: (-1, 0), pygame.K_a: (-1, 0),
    pygame.K_RIGHT: (1, 0), pygame.K_d: (1, 0),
}


def random_food(snake):
    """Pick a random cell that the snake is not on."""
    while True:
        food = (random.randrange(COLS), random.randrange(ROWS))
        if food not in snake:
            return food


def draw_cell(color, pos):
    x, y = pos
    pygame.draw.rect(screen, color, (x * CELL, y * CELL, CELL - 1, CELL - 1))


def new_game():
    snake = [(12, 9), (11, 9), (10, 9)]         # the head is the first item
    return snake, (1, 0), (1, 0), random_food(snake), 0, False


snake, direction, next_direction, food, score, game_over = new_game()
paused = False

running = True
while running:
    # 1. Handle input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                snake, direction, next_direction, food, score, game_over = new_game()
                paused = False
            elif event.key == pygame.K_p and not game_over:
                paused = not paused
                play_sound(pause_sound)
            elif event.key == pygame.K_m:
                if eat_sound is not None:
                    sound_enabled = not sound_enabled
            elif event.key in KEYS:
                dx, dy = KEYS[event.key]
                # Ignore turning straight back into ourselves
                if (dx, dy) != (-direction[0], -direction[1]):
                    next_direction = (dx, dy)

    # 2. Move the snake
    if not game_over and not paused:
        direction = next_direction
        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        hit_wall = not (0 <= head[0] < COLS and 0 <= head[1] < ROWS)
        hit_self = head in snake[:-1]           # the tail moves away, so skip it
        if hit_wall or hit_self:
            game_over = True
            play_sound(game_over_sound)
        else:
            snake.insert(0, head)               # add a new head
            if head == food:                    # ate food: keep the tail (grow)
                score += 1
                play_sound(eat_sound)
                if len(snake) == COLS * ROWS:   # board is full, nowhere for food
                    game_over = True
                else:
                    food = random_food(snake)
            else:
                snake.pop()                     # no food: remove the tail

    # 3. Draw everything
    screen.fill((17, 24, 39))
    for part in snake:
        draw_cell((52, 211, 153), part)
    draw_cell((248, 113, 113), food)
    message = f"Score: {score}"
    if game_over:
        message += "   Game over! Press R"
    screen.blit(font.render(message, True, (255, 255, 255)), (10, 10))
    if paused:
        paused_message = font.render("PAUSED - Press P to resume", True, (255, 255, 255))
        paused_rect = paused_message.get_rect(center=(COLS * CELL // 2, ROWS * CELL // 2))
        screen.blit(paused_message, paused_rect)
    sound_message = "Sound: On (M)" if sound_enabled else "Sound: Off (M)"
    screen.blit(font.render(sound_message, True, (203, 213, 225)), (10, 44))
    pygame.display.flip()

    clock.tick(8 + score // 5)                  # speeds up as you score

pygame.quit()


                                        
                                    
                                    
                            
                                
                            
                    